import flet as ft
import os
import pandas as pd
from modules import ocr, gpt_refinement, excel_handler, word_generator
from modules.config import EXCEL_OUTPUT_FILE, CONSOLIDATED_FILE, SAVE_DIR

def main(Page: ft.Page):
    # Configurações da UI
    Page.title = "Processador de Documentos"
    Page.theme_mode = "dark"  # Dark Mode como padrão
    Page.window.width = 1200
    Page.window.min_width = 800
    Page.window.height = 800
    Page.window.min_height = 600
    Page.window.center()
    Page.padding = ft.padding.all(20)
    Page.spacing = 20
    Page.scroll = "adaptive"

    # Variáveis globais da interface
    selected_images = []
    selected_template = None
    processed_data = []
    copied_value = None
    editing_cell = None
    edited_data = {}

    # Função para alternar entre Dark e Light Mode
    def toggle_theme(e):
        if Page.theme_mode == "dark":
            Page.theme_mode = "light"
            theme_toggle.icon = ft.Icons.BRIGHTNESS_2  # Ícone para modo escuro
        else:
            Page.theme_mode = "dark"
            theme_toggle.icon = ft.Icons.WB_SUNNY  # Ícone para modo claro
        Page.update()

    # Função para abrir o explorador de arquivos para imagens
    def open_file_explorer_images(e):
        file_picker_images.pick_files(allow_multiple=True)

    # Função para abrir o explorador de arquivos para template
    def open_file_explorer_template(e):
        file_picker_template.pick_files()

    # Função para iniciar a edição de uma célula
    def start_edit(e, row_index, col_name, current_value):
        nonlocal editing_cell
        editing_cell = (row_index, col_name)
        # Criar um TextField para edição
        text_field = ft.TextField(
            value=str(current_value),
            on_submit=lambda e: save_edit(e, row_index, col_name),
            on_blur=lambda e: save_edit(e, row_index, col_name)
        )
        # Substituir o texto da célula pelo TextField
        for i, row in enumerate(data_table.rows):
            if i == row_index:
                for j, cell in enumerate(row.cells):
                    if data_table.columns[j].label.content.value == col_name:
                        cell.content = text_field
                        break
        Page.update()

    # Função para salvar a edição
    def save_edit(e, row_index, col_name):
        nonlocal editing_cell, processed_data, edited_data
        if editing_cell == (row_index, col_name):
            new_value = e.control.value
            # Atualizar o valor na tabela
            for i, row in enumerate(data_table.rows):
                if i == row_index:
                    for j, cell in enumerate(row.cells):
                        if data_table.columns[j].label.content.value == col_name:
                            cell.content = ft.Container(
                                content=ft.Text(
                                    new_value,
                                    color="#e0e0e0",
                                    size=13,
                                    text_align=ft.TextAlign.CENTER,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                width=150 if col_name not in ["Endereço", "Local Nascimento"] else 200,
                                padding=ft.padding.all(5),
                            )
                            break
            
            # Atualizar os dados processados
            processed_data[row_index][col_name] = new_value
            edited_data[row_index] = processed_data[row_index]
            
            # Salvar alterações no arquivo Excel
            df = pd.DataFrame(processed_data)
            df.to_excel(CONSOLIDATED_FILE, index=False)
            
            editing_cell = None
            Page.update()

    # Processar as imagens
    def process_images(e):
        nonlocal processed_data
        if not selected_images:
            Page.snack_bar = ft.SnackBar(ft.Text("Nenhuma imagem selecionada!"), open=True)
            return
        if not selected_template:
            Page.snack_bar = ft.SnackBar(ft.Text("Nenhum template selecionado!"), open=True)
            return

        # Mostrar indicador de carregamento
        loading_indicator.visible = True
        Page.update()

        # Processar as imagens
        extracted_data = {}
        for image_path in selected_images:
            raw_text = ocr.extract_text_from_image(image_path)
            if not raw_text.strip():  # Verifica se o OCR não extraiu nada 
                Page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao processar a imagem: {image_path}"), open=True)
                continue
            
            refined_text = gpt_refinement.refine_text_with_gpt(raw_text)
            extracted_data[os.path.basename(image_path)] = (raw_text, refined_text)

        # Salvar no Excel e consolidar
        excel_handler.save_text_to_excel(extracted_data, EXCEL_OUTPUT_FILE)
        
        try:
            excel_handler.consolidate_data(EXCEL_OUTPUT_FILE, CONSOLIDATED_FILE)
        except Exception as e:
            Page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao consolidar dados: {str(e)}"), open=True)
            Page.update()
            return

        # Carregar dados consolidados para exibição
        df = pd.read_excel(CONSOLIDATED_FILE)
        processed_data = df.to_dict(orient="records")

        # Atualizar a tabela de dados
        data_table.rows.clear()
        for row_idx, row in enumerate(processed_data):
            cells = [
                ft.DataCell(
                    ft.Container(
                        content=ft.Text(
                            str(row.get(col.label.content.value, "")),
                            color="#e0e0e0",
                            size=13,
                            text_align=ft.TextAlign.CENTER,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        width=150 if col.label.content.value not in ["Endereço", "Local Nascimento"] else 200,
                        padding=ft.padding.all(5),
                    ),
                    on_tap=lambda e, ri=row_idx, cn=col.label.content.value, cv=row.get(col.label.content.value, ""): start_edit(e, ri, cn, cv)
                )
                for col in data_table.columns
            ]
            data_table.rows.append(ft.DataRow(cells=cells))
        Page.update()

        # Ocultar o indicador de carregamento após o processamento
        loading_indicator.visible = False
        Page.update()

    # Função para gerar documentos Word
    def generate_documents(e):
        if not processed_data:
            Page.snack_bar = ft.SnackBar(ft.Text("Nenhum dado processado!"), open=True)
            return

        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        df = pd.read_excel(CONSOLIDATED_FILE)
        word_generator.update_word_form(selected_template, df, SAVE_DIR)
        Page.snack_bar = ft.SnackBar(ft.Text("Documentos gerados com sucesso!"), open=True)
        Page.update()

    # Função para processar o resultado da seleção de imagens
    def set_selected_images(e):
        nonlocal selected_images
        if e.files:
            selected_images = [file.path for file in e.files]
            image_list.value = "\n".join(os.path.basename(img) for img in selected_images)
            Page.update()
        else:
            Page.snack_bar = ft.SnackBar(ft.Text("Nenhuma imagem selecionada!"), open=True)
            Page.update()

    # Função para processar o resultado da seleção de template
    def set_selected_template(e):
        nonlocal selected_template
        selected_template = e.files[0].path if e.files else None
        template_label.value = f"Template selecionado: {os.path.basename(selected_template)}" if selected_template else "Nenhum template selecionado"
        Page.update()

    # Função para copiar o valor da célula
    def cell_clicked(e):
        nonlocal copied_value
        copied_value = e.control.value
        Page.set_clipboard(copied_value)
        Page.snack_bar = ft.SnackBar(ft.Text(f"Copiado: {copied_value}"), open=True)
        Page.update()

    # Criação do FilePicker para imagens e template
    file_picker_images = ft.FilePicker(on_result=set_selected_images)
    file_picker_template = ft.FilePicker(on_result=set_selected_template)

    # Adicionando os FilePickers à página
    Page.add(file_picker_images)
    Page.add(file_picker_template)

    # UI: Botão para alternar entre Dark e Light Mode
    theme_toggle = ft.IconButton(
        icon=ft.Icons.WB_SUNNY,  # Ícone de modo escuro como padrão
        on_click=toggle_theme,
        tooltip="Alternar tema"
    )

    # UI: Labels com estilo melhorado
    image_list = ft.Text(
        "Nenhuma imagem selecionada",
        size=14,
        color="grey",
        weight=ft.FontWeight.W_400
    )
    template_label = ft.Text(
        "Nenhum template selecionado",
        size=14,
        color="grey",
        weight=ft.FontWeight.W_400
    )

    # UI: Botões com estilo melhorado
    select_images_button = ft.ElevatedButton(
        "Selecionar Imagens",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=open_file_explorer_images,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        )
    )
    
    select_template_button = ft.ElevatedButton(
        "Selecionar Template",
        icon=ft.Icons.FILE_PRESENT,
        on_click=open_file_explorer_template,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        )
    )

    process_button = ft.ElevatedButton(
        "Processar Imagens",
        icon=ft.Icons.PLAY_ARROW_ROUNDED,
        on_click=process_images,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        )
    )

    generate_button = ft.ElevatedButton(
        "Gerar Documentos Word",
        icon=ft.Icons.DESCRIPTION,
        on_click=generate_documents,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        )
    )

    # UI: Tabela de resultados com scroll horizontal
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        col,
                        weight=ft.FontWeight.BOLD,
                        size=14,
                        color="#e0e0e0",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    width=150 if col not in ["Endereço", "Local Nascimento"] else 200,
                    padding=ft.padding.all(5),
                )
            ) 
            for col in ["Nome Completo", "CPF", "Data de Nascimento", "Local de Nascimento", "Documento de Identidade", "Órgão Emissor", "Data deEmissão", "Nacionalidade", "Nome do Pai", "Nome da Mãe", "Endereço Completo", "Rua", "Número", "Bairro", "Cidade", "Estado", "CEP"]
        ],
        rows=[],
        border=ft.border.all(2, "#424242"),
        horizontal_lines=ft.border.BorderSide(1, "#424242"),
        vertical_lines=ft.border.BorderSide(1, "#424242"),
        heading_row_height=70,
        data_row_min_height=60,
        column_spacing=10,
        heading_row_color="#1e1e1e",
        data_row_color="#2d2d2d",
        data_text_style=ft.TextStyle(color="#e0e0e0", size=13),
    )

    # Container para a tabela com scroll
    table_scroll = ft.Container(
        content=ft.Row(
            [data_table],
            scroll="always",
            expand=True,
        ),
        height=400,
        padding=10,
        border=ft.border.all(1, "#424242"),
        border_radius=10,
        bgcolor="#1e1e1e",
        expand=True,
    )

    # UI: Indicador de Carregamento
    loading_indicator = ft.ProgressBar(
        visible=False,
        color="primary",
        bgcolor="#1a1a1a"
    )

    # Layout da UI com responsividade
    Page.add(
        ft.Container(
            content=ft.Column(
                [
                    # Cabeçalho
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(
                                    "Processador de Documentos",
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    color="primary"
                                ),
                                theme_toggle,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        padding=ft.padding.only(bottom=20),
                    ),
                    
                    # Seção de Seleção
                    ft.Container(
                        content=ft.Column([
                            ft.Row(
                                [select_images_button, select_template_button],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([ft.Text("Imagens:", weight=ft.FontWeight.BOLD), image_list], spacing=10),
                                    ft.Row([ft.Text("Template:", weight=ft.FontWeight.BOLD), template_label], spacing=10),
                                ]),
                                padding=ft.padding.all(10),
                                border=ft.border.all(1, "grey400"),
                                border_radius=8,
                                bgcolor=ft.Colors.SURFACE_TINT,
                            ),
                        ]),
                        padding=ft.padding.only(bottom=20),
                    ),
                    
                    # Botão de Processamento
                    ft.Row([process_button], alignment=ft.MainAxisAlignment.CENTER),
                    
                    # Divisor
                    ft.Divider(height=1, color="grey400"),
                    
                    # Seção da Tabela
                    ft.Container(
                        content=ft.Column([
                            ft.Row(
                                [
                                    ft.Text(
                                        "Dados Processados",
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color="primary"
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            table_scroll,
                        ]),
                        padding=ft.padding.symmetric(vertical=20),
                    ),
                    
                    # Botão de Geração
                    ft.Row([generate_button], alignment=ft.MainAxisAlignment.CENTER),
                    loading_indicator
                ],
                spacing=10,
                expand=True,
            ),
            expand=True,
            padding=20,
        )
    )

# Executar o app Flet
if __name__ == "__main__":
    ft.app(target=main)
    #ft.app(target=main, view=ft.WEB_BROWSER)
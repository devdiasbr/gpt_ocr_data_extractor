import pandas as pd
from openpyxl import Workbook
import json
import os
import re

def save_text_to_excel(data, output_file):
    """Salva textos extraídos e refinados em um arquivo Excel."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Documentos Processados"

    # Definir cabeçalho
    headers = ["Arquivo", "Nome Completo", "CPF", "Data de Nascimento", "Local de Nascimento",
               "Documento de Identidade", "Órgão Emissor", "Data de Emissão", "Nacionalidade",
               "Nome do Pai", "Nome da Mãe", "Endereço Completo", "Rua", "Número", "Bairro", "Cidade", "Estado", "CEP"]
    ws.append(headers)

    # Adicionar dados
    for file, (raw_text, refined_text) in data.items():
        try:
            if not refined_text.strip():
                raise ValueError("Resposta vazia do GPT.")

            # Tentar carregar o JSON, se falhar, continuar com um valor vazio
            try:
                # Remover delimitadores Markdown se existirem
                refined_text_cleaned = re.sub(r"```json\s*|\s*```", "", refined_text)
                refined_data = json.loads(refined_text_cleaned)
            except json.JSONDecodeError:
                print(f"Erro ao decodificar JSON para o arquivo {file}. Resposta: {refined_text}")
                refined_data = {}


            # Processa o endereço corretamente
            endereco = refined_data.get("Endereço", {})
            if isinstance(endereco, dict):
                rua = endereco.get("Rua", "") or ""
                numero = endereco.get("Número", "") or ""
                bairro = endereco.get("Bairro", "") or ""
                cidade = endereco.get("Cidade", "") or ""
                estado = endereco.get("Estado", "") or ""
                cep = endereco.get("CEP", "") or ""
                endereco_completo = f"{rua}, {numero}, {bairro}, {cidade}, {estado}, {cep}".strip(", ")
            else:
                endereco_completo = endereco
                rua = numero = bairro = cidade = estado = cep = ""

            # Adicionar dados ao Excel
            ws.append([file,
                       refined_data.get("Nome Completo", ""),
                       refined_data.get("CPF", ""),
                       refined_data.get("Data de Nascimento", ""),
                       refined_data.get("Local de Nascimento", ""),
                       refined_data.get("Documento de Identidade (RG)", ""),
                       refined_data.get("Órgão Emissor", ""),
                       refined_data.get("Data de Emissão", ""),
                       refined_data.get("Nacionalidade", ""),
                       refined_data.get("Nome do Pai", ""),
                       refined_data.get("Nome da Mãe", ""),
                       endereco_completo,
                       rua,
                       numero,
                       bairro,
                       cidade,
                       estado,
                       cep
                       ])
        except Exception as e:
            print(f"Erro ao adicionar dados ao Excel: {e}, Resposta: {refined_text}")
            ws.append([file, "Erro"] + [""] * 16)  # Linha de fallback com erro

    # Salvar o arquivo
    wb.save(output_file)
    print(f"Dados salvos em '{output_file}' com sucesso!")


def consolidate_data(input_file, output_file):
    """Consolida dados duplicados pelo Nome Completo e salva em outro arquivo Excel."""
    try:
        df = pd.read_excel(input_file)

        def first_non_null(series):
            return series.dropna().iloc[0] if not series.dropna().empty else ""

        consolidated_df = df.groupby("Nome Completo", as_index=False).agg({
            "CPF": first_non_null,
            "Data de Nascimento": first_non_null,
            "Local de Nascimento": first_non_null,
            "Documento de Identidade": first_non_null,
            "Órgão Emissor": first_non_null,
            "Data de Emissão": first_non_null,
            "Nacionalidade": first_non_null,
            "Nome do Pai": first_non_null,
            "Nome da Mãe": first_non_null,
            "Endereço Completo": first_non_null,
            "Rua": first_non_null,
            "Número": first_non_null,
            "Bairro": first_non_null,
            "Cidade": first_non_null,
            "Estado": first_non_null,
            "CEP": first_non_null,
            "Arquivo": lambda x: ', '.join(sorted(set(x.dropna()))),
        })

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        consolidated_df.to_excel(output_file, index=False)
        print(f"Dados consolidados salvos em '{output_file}' com sucesso!")
    except Exception as e:
        print(f"Erro ao consolidar dados: {str(e)}")
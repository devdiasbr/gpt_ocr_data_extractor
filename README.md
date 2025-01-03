# **Processador de Documentos 📄**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/devdiasbr/gpt_ocr_data_extractor/graphs/commit-activity)  

Este projeto automatiza o processamento de documentos utilizando técnicas de **OCR**, refinamento de dados com **IA** e geração de relatórios em **Excel** e **Word**. Ideal para agilizar tarefas repetitivas de leitura e preenchimento de documentos.

---

## **📋 Índice**

- [Funcionalidades](#-funcionalidades)  
- [Demonstração](#-demonstração)  
- [Estrutura do Projeto](#-estrutura-do-projeto)  
- [Como Usar](#-como-usar)  
- [Requisitos de Sistema](#-requisitos-de-sistema)  
- [Troubleshooting](#-troubleshooting)  
- [Roadmap](#-roadmap)  
- [Testes](#-testes)  
- [Contribuindo](#-contribuindo)  
- [Licença](#-licença)  

---

## **🛠 Funcionalidades**

- **Leitura de Documentos via OCR**  
  Utiliza o Tesseract OCR para extrair dados de imagens e PDFs.

- **Refinamento dos Dados com IA**  
  Realiza o refinamento dos dados extraídos utilizando a API da OpenAI GPT.

- **Geração de Documentos Word**  
  Cria arquivos `.docx` a partir de templates, preenchendo automaticamente os campos necessários.

- **Consolidação em Planilhas Excel**  
  Une e organiza os dados processados em arquivos `.xlsx`.

---

## **🎯 Demonstração**

### Interface do Usuário
![Interface do Projeto](images/demo_interface.png)

### Exemplo de Uso em Código

```python
from modules.ocr import process_document
from modules.gpt_refinement import refine_data

# Processar um documento
resultado_ocr = process_document("images/exemplo.pdf")
dados_refinados = refine_data(resultado_ocr)

# Gerar relatório
from modules.word_generator import create_report
create_report(dados_refinados, "output/relatorio.docx")
```

---

## **📂 Estrutura do Projeto**

```plaintext
Processador-de-Documentos/
│
├── main.py                      # Script principal
│
├── images/                      # Imagens de entrada para OCR
│   ├── cnh_teste.jpeg
│   └── image.png
│
├── modules/                     # Módulos auxiliares
│   ├── config.py               # Configurações gerais
│   ├── excel_handler.py        # Manipulação de arquivos Excel
│   ├── gpt_refinement.py       # Integração com GPT para refinamento
│   ├── ocr.py                  # Processamento OCR com Tesseract
│   └── word_generator.py       # Geração de documentos Word
│
├── output/                     # Pasta de saída para documentos processados
│   ├── documentos_processados.xlsx
│   └── dados_unificados.xlsx
│
├── requirements.txt            # Dependências do projeto
└── LICENSE                     # Arquivo de licença
```

---

## **📋 Como Usar**

### Pré-requisitos

**Tesseract OCR**  
- **Windows**: Baixe o instalador em: [Tesseract OCR para Windows](https://github.com/UB-Mannheim/tesseract/wiki)  
- **macOS**:  
  ```bash
  brew install tesseract
  ```  
- **Linux (Ubuntu/Debian)**:  
  ```bash
  sudo apt-get update
  sudo apt-get install tesseract-ocr
  ```

**Python 3.8+**  
Verifique a versão instalada no sistema:
```bash
python --version
```

### Dependências Python

Instale as dependências do projeto:
```bash
pip install -r requirements.txt
```

### Configuração

Clone o repositório:
```bash
git clone https://github.com/devdiasbr/gpt_ocr_data_extractor.git
cd gpt_ocr_data_extractor
```

Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

Execute o projeto:
```bash
python main.py
```

---

## **📊 Requisitos de Sistema**

### Hardware
- CPU: 2+ cores
- RAM: 4GB+ (8GB recomendado)
- Espaço em Disco: 500MB

### Software
- Python 3.8 ou superior
- Tesseract OCR 4.0+

### Sistema Operacional
- Windows 10/11
- Ubuntu 20.04+
- macOS 10.15+

---

## **❓ Troubleshooting**

### Problemas Comuns

**Erro: TesseractNotFoundError**
```plaintext
TesseractNotFoundError: Tesseract is not installed or not in PATH
```
**Solução**:
- Verifique se o Tesseract está instalado.
- Adicione o caminho do Tesseract ao PATH do sistema.
- Configure o caminho manualmente no código:
  ```python
  import pytesseract
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

**Erro: OpenAI API**
```plaintext
OpenAIError: Authentication failed
```
**Solução**:
- Verifique se a chave API está correta no arquivo `.env`.
- Confirme se há créditos disponíveis na sua conta.
- Verifique a conectividade com a API.

---

## **🗺 Roadmap**

### Próximas Funcionalidades

- Interface gráfica aprimorada
- Suporte para mais formatos de documento
- Processamento em lote
- Integração com serviços em nuvem
- API REST para integração com outros sistemas
- Suporte para múltiplos idiomas
- Dashboard de análise de dados

---

## **🧪 Testes**

### Executando Testes

Instale as dependências de teste:
```bash
pip install pytest pytest-cov
```

Execute todos os testes:
```bash
pytest tests/
```

Verifique a cobertura de testes:
```bash
pytest --cov=modules tests/
```

---

## **🤝 Contribuindo**

1. Faça um fork do projeto.
2. Crie sua feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit suas mudanças:
   ```bash
   git commit -m 'Add: nova funcionalidade'
   ```
4. Push para a branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Abra um Pull Request.

---

## **📄 Licença**

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

---

## **📬 Contato**

Bruno Dias - @devdiasbr  
Repositório no GitHub: [github.com/devdiasbr/gpt_ocr_data_extractor](https://github.com/devdiasbr/gpt_ocr_data_extractor)
```
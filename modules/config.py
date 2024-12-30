import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configurações do OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("Please set OPENAI_API_KEY environment variable in .env file")

# Caminho para o Tesseract OCR
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Diretórios de entrada e saída
INPUT_FOLDER = "images"
OUTPUT_FOLDER = "output"
TEMPLATE_PATH = "templates"

# Arquivos gerados
EXCEL_OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "documentos_processados.xlsx")
CONSOLIDATED_FILE = os.path.join(OUTPUT_FOLDER, "dados_unificados.xlsx")
SAVE_DIR = os.path.join(OUTPUT_FOLDER, "generated_templates")
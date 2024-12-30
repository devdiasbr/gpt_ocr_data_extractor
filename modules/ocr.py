 
import pytesseract
from PIL import Image
from modules.config import TESSERACT_CMD

# Configuração do Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def extract_text_from_image(image_path):
    """Extrai texto de uma imagem usando Tesseract OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='por')
        return text.strip()
    except Exception as e:
        print(f"Erro ao processar {image_path}: {str(e)}")
        return ""
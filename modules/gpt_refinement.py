 
import openai
from modules.config import OPENAI_API_KEY

# Configuração da API OpenAI
openai.api_key = OPENAI_API_KEY

def refine_text_with_gpt(text):
    """Refina o texto extraído e organiza os dados usando a API OpenAI GPT."""
    prompt = f"""
Abaixo está um texto extraído de um documento.
Extraia os seguintes campos (se existirem):
- Nome Completo
- Data de Nascimento
- Local de Nascimento
- Documento de Identidade (RG)
- Órgão Emissor
- Data de Emissão
- Nacionalidade
- Nome do Pai
- Nome da Mãe
- Endereço (Rua, Número, Bairro, Cidade, Estado, CEP - se existirem separadamente)
- CEP
- CPF

Organize o resultado em formato JSON.
Se houver endereço, separe os campos como:
- Rua
- Número
- Bairro
- Cidade
- Estado
- CEP

Se algum campo estiver ausente, deixe vazio.

Texto extraído:
{text}
"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você organiza informações extraídas de documentos em JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Erro ao processar com GPT: {str(e)}")
        return "{}"  # Retorna JSON vazio em caso de erro

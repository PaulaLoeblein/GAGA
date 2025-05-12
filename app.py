"""
Chatbot: Guia de Apoio Gestacional Atencioso (GAGA)

Este script cria um chatbot baseado no modelo open source Mistral da Hugging Face,
usando a Inference API. Funciona via terminal.

Autor: Paula Loeblein
Data: Maio, 2025
"""

import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import traceback
import time
import PyPDF2
import glob

# Carrega a API key do arquivo .env
load_dotenv()
API_KEY = os.getenv("HF_TOKEN")

# Define o modelo Mistral para ser usado
MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
client = InferenceClient(model=MODEL, token=API_KEY)


def carregar_conteudo_de_arquivo(caminho):
    """Lê conteúdo de um arquivo .txt ou .pdf e retorna como string."""
    
    # Se o arquivo for .txt, abre com codificação UTF-8 e retorna o conteúdo como texto
    if caminho.endswith(".txt"):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    # Se o arquivo for .pdf, usa PyPDF2 para ler e extrair o texto de cada página
    elif caminho.endswith(".pdf"):
        texto = ""
        with open(caminho, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                texto += page.extract_text() + "\n"
        return texto
    # Caso o arquivo não seja .txt nem .pdf, levanta um erro
    else:
        raise ValueError("Formato de arquivo não suportado. Use .txt ou .pdf")


# Histórico do chat (adaptado para instruções do Mistral)
# Define as diretrizes do chat, o que pode ou não fazer e como deve agir de acordo com sua função
history = [
    {
        "role": "system",
        "content": """
     Você é um assistente virtual chamado GAGA, abreviação para Guia de Apoio Gestacional Atencioso; é gentil, empático e altamente especializado em fornecer informações e apoio emocional PARA GESTANTES DURANTE A GRAVIDEZ.
     Não responda perguntas que não tenham a ver com saúde emocional ou mental ou com gravidez.
     Responda APENAS E DIRETAMENTE a perguntas que sejam *estritamente* relacionadas à saúde emocional, bem-estar psicológico e aspectos emocionais da experiência da gravidez. Seja **objetivo e conciso**, fornecendo informações essenciais de forma clara e direta, sem se prolongar em detalhes excessivos inicialmente.
     Se a pergunta NÃO FOR sobre saúde emocional, bem-estar psicológico ou aspectos emocionais da gravidez, você DEVE responder de forma educada e concisa que NÃO PODE ajudar com esse tópico específico. Mencione brevemente sua área de especialização e sugira que a usuária procure fontes de informações especializadas para o tópico da pergunta. Não dê continuidade à resposta.
     Você não precisa mencionar seu nome a cada interação e deve tratar cada mensagem como uma conversa contínua.
     Não repita itens ao fornecer uma lista.
     Evite fornecer listas a não ser que seja importante.
     Ao fornecer listas, forneça SOMENTE 5 itens; só forneça mais se for solicitado um número específico.
     Ao fornecer listas, forneça também uma breve descrição do item.
     Mantenha um tom acolhedor e de apoio.
     Se uma pergunta for feita mais de uma vez, relembre o usuário de que a pergunta já foi feita e relembre a resposta.
     
     

     Considere as seguintes diretrizes ao responder:
     - Mantenha um tom acolhedor e de apoio.
     - Não se apresente no início nem se despeça ao final de cada mensagem; mantenha um fluxo natural de conversa, como em um diálogo comum.
     - Forneça informações precisas e relevantes PARA A SAÚDE EMOCIONAL DA GESTANTE de forma **objetiva e direta**.
     - Se a dúvida envolver questões médicas específicas (que não sejam puramente emocionais, como sintomas físicos), SEMPRE recomende a consulta com um profissional de saúde qualificado (médico, enfermeira obstétrica, etc.) de forma **clara e imediata**.
     - Evite dar conselhos médicos DIRETOS. Seu papel é de suporte e informação geral sobre bem-estar emocional, sendo **sucinto** ao fazê-lo.
     - Seja breve e objetiva.
     - RESPONDA APENAS SE A PERGUNTA FOR DIRETAMENTE RELACIONADA À SAÚDE EMOCIONAL NA GRAVIDEZ. Caso contrário, DECLINE educadamente.
     - Não responda o que não foi perguntado. Atenha-se estritamente à pergunta feita DENTRO DO ESCOPO DA SAÚDE EMOCIONAL NA GRAVIDEZ, sendo **direto ao ponto**.
     - Evite listar informações ou sugestões exaustivas. Forneça os pontos principais e ofereça-se para fornecer mais detalhes se solicitado.
     
     
     Aja de acordo com as situações descritas abaixo:
     verifique se essas perguntas/pedidos/frases fazem sentido para o contexto de um assistente de saúde emocional em gestantes e caso não faça, responda que você é um especialista somente na área apoio emocional PARA GESTANTES e que não pode ajudar com isso, e encerre a resposta. Se a pergunta fizer sentido dentro do seu escopo, responda normalmente:
     
     "cite 3 carros esportivos acima de 500 mil reais" -> não faz parte do escopo
     "a cor do céu é azul? por que?" -> não faz parte do escopo
     "me indique 3 filmes de comedia" -> não faz parte do escopo
     "qual o jogo mais vendido da história" -> não faz parte do escopo
     "posso trocar trigo por aveia ao fazer bolode cenoura?"-> não faz parte do escopo
     
     
     "estou grávida de 3 meses, descobri recentemente, meu noivo me deixou, estou muito triste o que devo fazer?" -> faz parte do escopo
     "estou pensando em ter um filho, mas meu marido é estéril, estou me sentindo péssima, quero muito ter um filho, o que posso fazer?" -> faz parte do escopo
     "acabei de perder o bebe, não sei liadr com a dor, me ajude por favor" -> faz parte do escopo
     "estou muito preocupada com minha gravidez, minha familia não me apoia e não sei o que fazer, me ajude" -> faz parte do escopo
     "me indique exercicios que podem me ajudar a aliviar minha ansiedade" -> faz parte do escopo
     
     """
    }
]

# Carregar conteúdo extra de um arquivo e adicionar ao prompt do sistema
PATH_EXTRA_FILES = "./documents/document.pdf"  

arquivos = glob.glob(PATH_EXTRA_FILES)
conteudo_total = ""

if os.path.exists(PATH_EXTRA_FILES):
    try:
        conteudo_extra = carregar_conteudo_de_arquivo(PATH_EXTRA_FILES)
        history[0]["content"] += "\n\nInformações complementares:\n" + conteudo_extra
    except Exception as e:
        print(f"Erro ao carregar conteúdo adicional: {e}")

# Função que envia a pergunta do usuário para o modelo de linguagem e retorna a resposta
def responder(pergunta):
    # Adiciona a pergunta do usuário ao histórico de mensagens
    history.append({"role": "user", "content": pergunta})
    try:
        # Exibe "Pensando..." com animação de três pontos
        print("Pensando...", end="", flush=True)
        for _ in range(3):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print("\r" + " " * 15 + "\r", end="", flush=True)
        
        # Faz a requisição ao modelo para gerar uma resposta baseada no histórico
        resposta = client.chat.completions.create(
            model=MODEL,
            messages=history,
            max_tokens=800
        )
        # Extrai o conteúdo da resposta gerada
        conteudo = resposta.choices[0].message.content
        # Adiciona a resposta ao histórico como se fosse do assistente
        history.append({"role": "assistant", "content": conteudo})
        return conteudo
    except Exception as e:
        return f"Ocorreu um erro: {e}"

# Função para limpar o terminal, compatível com Windows e Unix
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função que exibe o cabeçalho inicial do programa no terminal
def exibir_header():
    print("=" * 80)
    print(" " * 25 + "GAGA - Guia de Apoio Gestacional Atencioso")
    print("=" * 80)
    print("Este é o seu assistente virtual para apoio emocional durante a gravidez.")
    print("Digite 'sair' a qualquer momento para encerrar a conversa.")
    print("Digite 'limpar' para limpar o histórico de conversas.")
    print("-" * 80)

# Função para imprimir texto como se estivesse sendo digitado, com delay entre os caracteres
def imprimir_texto_progressivo(texto, delay=0.01):
    for char in texto:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# Função principal que executa o loop de conversa com o usuário
def chat():
    limpar_tela()
    exibir_header()
    print("\nGAGA iniciado. Digite 'sair' para encerrar ou 'limpar' para limpar o histórico.\n")
    while True:
        pergunta = input("Você: ")
        if pergunta.lower() in ['sair', 'exit', 'quit']:
            # Encerra o programa com uma mensagem de despedida
            imprimir_texto_progressivo("\nGAGA: Até mais! Espero ter ajudado. Cuide-se bem!")
            break
        elif pergunta.lower() in ['limpar', 'clear', 'reset']:
            # Limpa a tela, exibe o cabeçalho e reinicia o histórico
            limpar_tela()
            exibir_header()
            history[:] = [history[0]]
            print("\nGAGA: Histórico de conversa limpo.")
            continue
        try:
            # Envia a pergunta ao modelo e imprime a resposta com efeito de digitação
            resposta = responder(pergunta)
            print("\nGAGA: ", end="")
            imprimir_texto_progressivo(resposta, 0.01)
        except Exception as e:
            # Mostra erro completo no terminal caso algo dê errado
            print(f"\nOcorreu um erro: {e}")
            traceback.print_exc()

# Ponto de entrada do script: inicia o chat se o arquivo for executado diretamente
if __name__ == "__main__":
    chat()

# GAGA Chatbot: Guia de Apoio Gestacional Atencioso

Este script Python cria um chatbot interativo chamado GAGA (Guia de Apoio Gestacional Atencioso). Utilizando o modelo open source Mistral da Hugging Face Inference API, o GAGA oferece suporte e informações sobre saúde emocional e bem-estar psicológico para gestantes durante a gravidez, baseado na temática do meu TCC, funcionando diretamente no terminal.

## Funcionalidades

* **Foco em Saúde Emocional na Gravidez:** Especializado em responder perguntas estritamente relacionadas ao bem-estar emocional, sentimentos e aspectos psicológicos da gravidez.
* **Gentil e Empático:** Projetado para fornecer respostas de forma atenciosa e compreensiva.
* **Filtro de Escopo:** Identifica e se recusa educadamente a responder perguntas fora do escopo da saúde emocional durante a gravidez.
* **Interface de Terminal:** Funciona diretamente no terminal, facilitando a interação via linha de comando.
* **Encerramento Seguro:** Permite encerrar a conversa de forma simples com comandos como `sair`.

## Pré-requisitos

* **Python 3.6 ou superior**
* **Conta na Hugging Face e uma API key:** Você precisará de uma API key da Hugging Face para utilizar a Inference API.
* **Variável de ambiente `HF_TOKEN` configurada:** Sua API key deve ser salva como uma variável de ambiente chamada `HF_TOKEN` ou em um arquivo `.env` na mesma pasta do script.

## Instalação

1.  **Clone o repositório (opcional):**
    ```bash
    git clone [https://link-para-seu-repositorio](https://link-para-seu-repositorio)
    cd [nome-do-seu-repositorio]
    ```

2.  **Crie um arquivo `.env` (opcional):**
    Se você não configurou a variável de ambiente `HF_TOKEN`, crie um arquivo chamado `.env` na mesma pasta do script e adicione a sua API key:
    ```
    HF_TOKEN="sua_api_key_aqui"
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Como Usar

1.  **Execute o script Python:**
    ```bash
    python app.py
    ```

2.  **Interaja com o GAGA:** Faça suas perguntas sobre saúde emocional durante a gravidez no terminal.

3.  **Comandos:**
    * `sair`, `exit` ou `quit`: Encerra a conversa.

## Autor

Paula Loeblein
Maio, 2025

## Observações

* Este chatbot é uma ferramenta de apoio e não substitui a consulta com profissionais de saúde qualificados. Em caso de dúvidas médicas específicas, sempre procure orientação de um médico ou enfermeira obstétrica.
* O desempenho do chatbot depende da disponibilidade e da resposta da Hugging Face Inference API.

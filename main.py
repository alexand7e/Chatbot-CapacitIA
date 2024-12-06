import streamlit as st
import google.generativeai as genai

# Função para configurar o modelo Gemini com cache
@st.cache_resource
def setup_gemini_model(api_key):
    try:
        genai.configure(api_key=api_key)
        
        # Configurações de geração
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        
        # Modelo com instruções de sistema
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
            system_instruction="""#Assistente de correção de texto\n\nVocê é uma assistente de correção de texto humana, carismática para a melhoria de textos jornalísticos. Você vai atender os jornalistas da Coordenadoria de comunicação social do Piauí.\nOs textos contém a redação jornalística, mais a citação de fala de terceiros.\n\n#Objetivos\n- identique falas atribuídas a outras pessoas e use algum marcador (\u003c\u003e) para separar esse texto dos demais.\n- Para os textos separados por \u003c\u003e, mantenha o texto sem alterá-lo, mesmo com erros gramaticais.\n- Fazer a correção ortográfica em português do Brasil.\n- Fazer a revisão com estilo jornalístico dos textos, os deixando mais claros e concisos.\n- Não usar palavras rebuscadas, consideradas dificeis. Quando achar palavras rebuscadas, você deve trocar por uma mais simples.\n- criar um título para o texto.\n- gerar um relatório com as mudanças que foram feitas pela correção da assistente.\n\n#Exemplos de interação\n- Q: {documento com texto de uma notícia}\n- A: {correção do texto}"""
        )
        
        return model
    except Exception as e:
        st.error(f"Erro ao configurar o modelo: {e}")
        return None

# Função principal do Streamlit
def main():
    st.title("Assistente de Correção de Textos")
    
    # Input para a chave API
    api_key = st.text_input("Digite sua Chave API do Gemini", type="password")
    
    # Verifica se a chave API foi fornecida
    if api_key:
        # Configura o modelo Gemini usando cache
        model = setup_gemini_model(api_key)
        
        if model:
            # Inicializa a sessão de chat
            if 'chat_session' not in st.session_state:
                st.session_state.chat_session = model.start_chat(history=[])
            
            # Exibe o histórico de mensagens
            for message in st.session_state.chat_session.history:
                if message.role == "user":
                    st.chat_message("user").write(message.parts[0].text)
                else:
                    st.chat_message("assistant").write(message.parts[0].text)
            
            # Input de mensagem do usuário
            if prompt := st.chat_input("Digite sua mensagem"):
                # Exibe a mensagem do usuário
                st.chat_message("user").write(prompt)
                
                try:
                    # Envia a mensagem e obtém a resposta
                    response = st.session_state.chat_session.send_message(prompt)
                    
                    # Exibe a resposta do assistente
                    st.chat_message("assistant").write(response.text)
                
                except Exception as e:
                    st.error(f"Erro ao enviar mensagem: {e}")
    else:
        st.warning("Por favor, insira sua chave API do Gemini para começar.")

# Executa a aplicação
if __name__ == "__main__":
    main()

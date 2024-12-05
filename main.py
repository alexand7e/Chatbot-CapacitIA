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
            system_instruction="# Assistente Gerador de Relatórios \nVocê é um assistente carismático e sucinto para análise documental e geração de relatórios para o {Governo do Estado do Piauí}.\n\n# Objetivo\n- Receber documentos para analisar a respeito do estado.\n- Analisar a estrutura documental e as tabelas contidas no documento.\n- Fornecer um resumo sobre o {documento}.\n- Perguntar as características do relatório para o {usuário}.\n- Redigir um relatório conforme requisitado pelo {usuário}.\n\n# Exemplos de interação \n- user: {documento do Balanço de 2023} \n- assistente: {resumo do documento}\n- user: faça um relatório\n- assistente: descrevas as {características} do relatório.\n\n- user: que dia é hoje?\n- Desculpe, não posso ajudá-lo nessa tarefa\n\n# Informações adicionais \nQuando o {usuário} fugir do propósito do assistente, responda: \"Desculpe, não posso ajudá-lo nessa tarefa\""
        )
        
        return model
    except Exception as e:
        st.error(f"Erro ao configurar o modelo: {e}")
        return None

# Função principal do Streamlit
def main():
    st.title("Assistente de Relatórios | Governo do Estado do Piauí")
    
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

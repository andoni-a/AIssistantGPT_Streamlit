import streamlit as st
import gpt_helper
import json
from PIL import Image
import logging
import httpx


# Initialize the OpenAI client and retrieve the assistant
client, assistant_id = gpt_helper.initialize_client()
 # Create a new thread for the conversation
thread_id = gpt_helper.create_thread(client)


# Define a custom filter to exclude HTTP request log messages
class ExcludeHttpFilter(logging.Filter):
    def filter(self, record):
        # Exclude log messages related to HTTP requests
        return "httpx" not in record.name

# Configure the logger for the root logger only
logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level (e.g., INFO, DEBUG)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',  # Specify the log file name
)


# Create a logger for the Streamlit app (the root logger)
logger = logging.getLogger()

# Add the custom filter to exclude HTTP request log messages
logger.addFilter(ExcludeHttpFilter())



def ask_openai(question):
    # Add user's message to the thread
    gpt_helper.add_message_to_thread(client, thread_id, question)

    # Run the conversation through the assistant
    run_id = gpt_helper.run_conversation(client, thread_id, assistant_id)

    # Retrieve all messages from the conversation thread
    messages= gpt_helper.get_conversation_messages(client, thread_id)
    return messages

        



def main():
    st.set_option('deprecation.showfileUploaderEncoding', False)
    
    with st.sidebar:
        logo = Image.open("logo.png")
        st.image(logo, width=250)
        
        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "Hola soy AIssistant, un chatbot basado en el assistant_id creado en OpenAI."            
        )
        st.markdown(
            "Recuerda que la información generada por esta aplicación está sujeta a verificación "
            
        )
        st.markdown(
            "No compartas información confidencial o personal aquí."
        )
        st.markdown(
            "Tu feedback y contribuciones son fundamentales para mejorar el AIssistant "
        )
        


        st.markdown("---")
        st.markdown("# Selecciona Asistente")
        selected_assistant = st.radio("Elige un asistente", ["Documentacion técnica", "Documentación Gráfica"])
        st.markdown("---")
        st.markdown(
            "Contacto de soporte andoni@anire.es "
        )
    
    

    st.title("💬 AIssistant")
    st.caption("🚀 powered by andoni arrizabalaga")
    

    # Log an informational message from the root logger
    logger.info("User visited the homepage.")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hola!! soy AIssistant, selecciona un asistente para comenzar ¿En qué puedo ayudarte?"}]

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Escribe tu pregunta aquí:")
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        response = ask_openai(user_input)

        # Log user interactions from the root logger
        logger.info(f"User input: {user_input}")
        logger.info(f"Assistant response: {response}")

        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

if __name__ == "__main__":
    main()
import streamlit as st
import tempfile
from scripts.auto_caption import mp3_to_srt
from scripts.smart_cutting_tool import main

# Configurações gerais da página
st.set_page_config(
    page_title="Auto Legenda & Editor",
    page_icon="🎥",
    layout="wide",
)

# Interface Streamlit
st.title("🎥 Auto Legenda & Editor")

tab1, tab2 = st.tabs(["Auto Legenda", "Editor de Vídeo"])

# Aba 1: Auto Legendagem
with tab1:
    st.header("Legendas Automáticas")
    uploaded_mp3 = st.file_uploader("Faça o upload de um arquivo MP3", type=["mp3"])
    max_chars = st.slider("Máximo de caracteres por linha", min_value=20, max_value=80, value=42, step=1)
    
    if uploaded_mp3 is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3:
            temp_mp3.write(uploaded_mp3.read())
            temp_mp3_path = temp_mp3.name
            print(temp_mp3_path)

        st.success("Arquivo carregado com sucesso!")
        if st.button("Gerar Legenda"):
            with st.spinner("Gerando legenda..."):
                mp3_to_srt(temp_mp3_path, max_chars)

            st.success("Legenda gerada com sucesso!")
            # Ler o conteúdo do arquivo gerado
            with open('tmp/legenda.srt', "r", encoding="utf-8") as file:
                srt_content = file.read()

            st.download_button(
                label="Baixar Legenda (SRT)",
                data=srt_content,
                file_name="legenda.srt",
                mime="text/srt"
            )

# Aba 2: Editor de Vídeo
with tab2:
    st.header("Editor de Vídeo")
    video_file = st.file_uploader("Faça o upload de um vídeo", type=["mp4", "mov", "avi"])
    if video_file is not None:
        st.video(video_file)
        upload_button = st.button("Enviar vídeo para edição")

        if upload_button:
            output = main(video_file)
            st.success("Vídeo enviado com sucesso!")
            st.download_button("Baixar Vídeo Editado", data="video_editado.mp4", file_name=output)

# Instruções adicionais
st.sidebar.markdown("## 🛠️ Instruções")
st.sidebar.markdown(
    """
    - **Auto Legenda**: Gere legendas automáticas a partir de arquivos de audio.
    - **Editor de Vídeo**: Corta os videos baseado nos momentos onde há fala e retorna um arquivo sem silêncio.
    """
)



import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet



class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def create_pdf(self,summary_text):
        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        content = [Paragraph(summary_text.replace("\n", "<br/>"), styles["BodyText"])]

        doc.build(content)

        buffer.seek(0)
        return buffer   

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        if usecase == "AI News":
            frequency = self.user_message
            with st.spinner("Fetching and summarizing news... ⏳"):
                result = graph.invoke({"messages": frequency})
                try:
                    # Read the markdown file
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()
                        
                    # Display the markdown content in Streamlit
                    st.markdown(markdown_content, unsafe_allow_html=True)
                    pdf_file = self.create_pdf(markdown_content)
                    with st.sidebar:
                        st.download_button(
                            label="📄 Download PDF Report",
                            data=pdf_file,
                            file_name=f"{frequency.lower()}_summary.pdf",
                            mime="application/pdf"
                        )
                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
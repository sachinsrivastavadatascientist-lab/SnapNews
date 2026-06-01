import streamlit as st
from src.AI_NEWS.ui.streamlitui.loadui import LoadStreamlitUI
from src.AI_NEWS.LLMs.groqllm import GroqLLM
from src.AI_NEWS.graph.graph_builder import GraphBuilder
from src.AI_NEWS.ui.streamlitui.display_results import DisplayResultStreamlit

def load_langgrah_agenticai_app():
    '''Initate the UI'''

    #LOAD UI
    ui =LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    user_message = None

    if not user_input:
        st.error("Error: Failed to load nuser input from the UI")
        return
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe

    if user_message:
        try:
            ## Configure LLM
            obj_llm_config = GroqLLM(user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
               st.error("Error: model could not be intialized") 
               return
            
            ## Initalize and set up graph based on usecase
            usecase = user_input.get("selected_usecases")
            if not usecase:
                st.error("Error:No usecase selected.")
                return
            
            ## Graph builder

            graph_builder = GraphBuilder(model=model)
            try:
                graph=graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                 st.error(f"Error : Graph set up failed - {e}")
                 return
        except Exception as e:  
            st.error(f"Error :  {e}")  
            return
    
   

    
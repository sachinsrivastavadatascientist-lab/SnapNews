from langgraph.graph import StateGraph,END,START
from src.AI_NEWS.state.state import State
from src.AI_NEWS.nodes.AI_news_node import AINewsNode
#from src.langgraphagenticai.nodes.chatbot_with_tools_node import ChatbotWithToolNode



class GraphBuilder:
    def __init__(self,model):
        self.llm = model
        self.graph_builder = StateGraph(State)
       

    def ai_news_builder_graph(self):
         
         ai_news_node = AINewsNode(self.llm)
        # Added the node

         self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
         self.graph_builder.add_node("summarize_news",ai_news_node.summarize_news)
         self.graph_builder.add_node("save_result",ai_news_node.save_result)
         
         # Added the edges
         self.graph_builder.set_entry_point("fetch_news")
         self.graph_builder.add_edge("fetch_news","summarize_news")
         self.graph_builder.add_edge("summarize_news","save_result")
         self.graph_builder.add_edge("save_result",END)


    def setup_graph(self,usecase: str):
        '''Setups the graph for the selected usecases''' 

        if usecase == "AI News":
            self.ai_news_builder_graph()

        return self.graph_builder.compile()    
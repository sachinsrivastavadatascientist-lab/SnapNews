from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
import os 

class AINewsNode:
    def __init__(self,llm):
        '''
        Intialize the AINewsNode with API Keys for Tavily and GROQ
        '''
        self.tavily = TavilyClient()
        self.llm=llm

        # this is to capture various steps in this fi9le so that later can be use for steps shown
        self.state ={}

    def fetch_news(self,state:dict) :
        '''
        Fetch AI News based on the specified frequency
        
        Args:
          state(dict)->the state dictionary contaning 'frequency'.
          
        Returns:
          dict: Updated state with 'news data' key contaning fetched news  '''   
        
        frequency = state['messages'][0].content.lower()
        self.state['frequency'] = frequency
        time_range_map = {'daily':'d','weekly':'w','monthly':'m'}
        days_map = {'daily':1,'weekly':7,'monthly':30,'year':366}

        response = self.tavily.search(
            query = "Top AI News in India and globally",
            topic = 'news',
            time_range = time_range_map[frequency],
            include_answer='advanced',
            max_results = 10,
            days = days_map[frequency]
        )

        state['news_data'] = response.get('results',[])
        self.state['news_data'] = state['news_data']
        return state
    
    def summarize_news(self,state:dict):
        '''
        Summarizes the fetched news using LLM
        
        Args:
           state(dict):The state dictionary contaning 'news_datas'. 
           
        Returns:
           dict: updated state with summary key contaning the summarized news. '''
        
        news_items = self.state['news_data']

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize AI news articles into markdown format. For each item include:
        - Date in **YYYY-MM-DD** format in IST timezone
        - Concise sentences summary from latest news
        - Sort news by date wise (latest first)
        - Source URL as link
        Use format:
        ### [Date]
        - [Summary](URL)"""),
            ("user", "Articles:\n{articles}")
        ])

        article_str =  "\n\n".join(
    [
        f"Content: {item.get('content', '')[:400]}\n"
        f"URL: {item.get('url', '')}\n"
        f"Date: {item.get('published_date', '')}"
        for item in news_items
    ])
        chain = prompt_template | self.llm
        response = chain.invoke({"articles": article_str}) 
           
        #response = self.llm.invoke(prompt_template.format(articles =article_str))
        
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return self.state
    
  

    def save_result(self, state):
        frequency = self.state['frequency']
        summary = self.state['summary']

        os.makedirs("AINews", exist_ok=True)

        filename = f"AINews/{frequency}_summary.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)

        self.state["filename"] = filename
        return self.state

            
            
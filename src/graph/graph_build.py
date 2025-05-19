import os
from src.state.state import AgentState
from src.node.detect_tone import DetectTone
from src.node.extract_intent import ExtractIntent
from src.node.draft_reply import DraftReply
from src.node.refine_reply import RefineReply
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")


class ReplyPipeline:
    """
    Builds and runs the 4‑node LangGraph that generates
    a human‑like social‑media reply.
    """

    def __init__(self, llm):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=2000, groq_api_key=os.getenv("GROQ_API_KEY"))
        self.pipeline = self._build_graph()

    ## StateGraph Function and Compilation
    def _build_graph(self):
        g = StateGraph(AgentState)

        # Create Graph by adding nodes and edges 
        g.add_node("DetectTone",    DetectTone)
        g.add_node("ExtractIntent", ExtractIntent)
        g.add_node("DraftReply",    DraftReply)
        g.add_node("RefineReply",   RefineReply)

        # edges
        g.add_edge(START, "DetectTone")
        g.add_edge("DetectTone",    "ExtractIntent")
        g.add_edge("ExtractIntent", "DraftReply")
        g.add_edge("DraftReply",    "RefineReply")
        g.add_edge("RefineReply",   END)

        return g.compile()

    ## Run the pipeline where the user provides the platform and post text.
    ## The pipeline will return a dict with the generated reply and other info.    
    async def run_pipeline(self,platform:str, post_text:str) -> dict:
        init = AgentState(platform=platform, post_text=post_text)
        result = await self.pipeline.ainvoke(init)          # returns dict‑like
        return dict(result)   

import os
from langchain_groq import ChatGroq
from src.state.state import AgentState
from dotenv import load_dotenv
load_dotenv()

## Extract Intent Node
def ExtractIntent(state: AgentState) -> AgentState:
    """Extract the user's intent from their social media post."""
    GROQ_API_KEY    = os.getenv("GROQ_API_KEY") 
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=2000, groq_api_key=os.getenv("GROQ_API_KEY"))
    system_msg = (
        "You are an intent‑extraction microservice.\n"
        "• Goal: Summarize the PRIMARY intent or purpose of the user’s post in ≤ 15 words.\n"
        "• Output: ONE sentence, no bullet points, no hashtags, no emojis.\n"
        "Focus on what the poster is trying to achieve (announce news, ask for help, share opinion, etc.)."
    )
    res = llm.invoke([("system", system_msg), ("human", state.post_text)])
    state.intent = res.content.strip()
    return state
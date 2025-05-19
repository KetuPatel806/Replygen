import os
from langchain_groq import ChatGroq
from src.state.state import AgentState
from dotenv import load_dotenv
load_dotenv()

## Refine Reply Node
def RefineReply(state: AgentState) -> AgentState:
    """Refine the draft reply to the user's social media post."""
    GROQ_API_KEY    = os.getenv("GROQ_API_KEY") 
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=2000, groq_api_key=os.getenv("GROQ_API_KEY"))
    system_msg = (
            f"Improve the following draft for {state.platform}.\n"
            f"Keep the tone {state.tone}. Make it natural, under 50 words, no clichés.\n"
            f"Return only the final reply text."
        )
    res = llm.invoke([("system", system_msg), ("human", state.draft)])
    state.reply = res.content.strip()
    return state
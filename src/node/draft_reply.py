import os
from langchain_groq import ChatGroq
from src.state.state import AgentState
from dotenv import load_dotenv
load_dotenv()

## Draft Reply Node
def DraftReply(state: AgentState) -> AgentState:
    """Draft a reply to the user's social media post."""
    GROQ_API_KEY    = os.getenv("GROQ_API_KEY")  
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=2000, groq_api_key=os.getenv("GROQ_API_KEY"))
    system_msg = (
            f"You are an avid, authentic {state.platform} user.\n"
            f"Craft a first‑draft reply that:\n"
            f"• Matches the tone: {state.tone}.\n"
            f"• Directly addresses the poster’s intent: {state.intent}.\n"
            f"• Sounds human (no 'As an AI...' or stiff phrasing).\n"
            f"• Length guidelines — Twitter 20‑40 words, LinkedIn 30‑70, Instagram 10‑30.\n"
            f"• Twitter: ≤1 tasteful emoji, no links.  LinkedIn: professional, no emoji.  "
            f"Instagram: emojis allowed, keep it light.\n"
            f"Respond with the reply only."
        )
    res = llm.invoke([("system", system_msg), ("human", state.post_text)])
    state.draft = res.content.strip()
    return state
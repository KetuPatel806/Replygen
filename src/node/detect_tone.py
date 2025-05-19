import os
from langchain_groq import ChatGroq
from src.state.state import AgentState
from dotenv import load_dotenv
load_dotenv()

## Detect Tone Node
def DetectTone(state: AgentState) -> AgentState:
    """Detect the tone of the user's social media post."""
    GROQ_API_KEY    = os.getenv("GROQ_API_KEY")  
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=2000, groq_api_key=os.getenv("GROQ_API_KEY"))
    system_msg = (
        "You are a tone‑classification microservice.\n"
        "• Task: Read the user’s social‑media post and decide the single best‑fit tone.\n"
        "• Allowed output: EXACTLY ONE lower‑case word, no punctuation, no explanations.\n"
        "• Legal tone vocabulary (choose the closest match):\n"
        "  enthusiastic | celebratory | casual | humorous | professional | authoritative | "
        "critical | urgent | contemplative | grateful | humble | inspirational | formal | "
        "sarcastic | negative\n"
        "• If none fit perfectly, choose the nearest.\n"
        "• Do NOT output JSON, numbers, multiple words, or anything besides the tone word."
    )
    res = llm.invoke([("system", system_msg), ("human", state.post_text)])
    state.tone = res.content.strip().split()[0].lower()
    return state
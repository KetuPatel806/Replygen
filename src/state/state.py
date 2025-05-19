from datetime import datetime, timezone
from typing import Optional,TypedDict
from pydantic import Field
from pydantic import BaseModel,Field

## AgentState is a canonical state object carried through the LangGraph pipeline.
class AgentState(BaseModel):
    """Canonical state object carried through the LangGraph pipeline."""
    
    platform: str = Field(
        ...,
        description="Name of the social‑media platform (e.g., 'twitter', 'linkedin').",
    )
    post_text: str = Field(
        ...,
        description="Raw text of the original post the model will reply to.",
    )
    tone: Optional[str] = Field(
        None,
        description="Single lower‑case word representing the detected tone.",
    )
    intent: Optional[str] = Field(
        None,
        description="One‑sentence summary of the poster’s primary intent.",
    )
    draft: Optional[str] = Field(
        None,
        description="First‑pass reply before refinement.",
    )
    reply: Optional[str] = Field(
        None,
        description="Polished, final reply returned to the client.",
    )
    ts: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when this state instance was created.",
    )

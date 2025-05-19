import os, datetime, json, asyncio
import mysql.connector
from typing import Annotated
from dotenv import load_dotenv 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, constr, StringConstraints
from motor.motor_asyncio import AsyncIOMotorClient
from langchain_groq import ChatGroq
from src.graph.graph_build import ReplyPipeline
from src.state.state import AgentState

load_dotenv()

## TIDB connection
db_config = {
    "host": os.getenv("TIDB_HOST"),
    "user": os.getenv("TIDB_USER"),
    "password": os.getenv("TIDB_PASSWORD"),
    "database": os.getenv("TIDB_DATABASE")
}
## MySQL connection
def get_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to TiDB: {e}")
        return None


##MONGO_URI = os.getenv("MONGO_URI")   # atlas string
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=2000, groq_api_key=os.getenv("GROQ_API_KEY"))


app = FastAPI(title="ReplyGen API", version="0.1.0")
## Constaints on the input fields
PlatformStr = Annotated[str,
    str,
    StringConstraints(to_lower=True, min_length=1, max_length=20)
]
PostTextStr = Annotated[str, 
    StringConstraints(strip_whitespace=True,min_length=1, max_length=5000)
]
## Request Fields
class ReplyRequest(BaseModel):
    platform: PlatformStr
    post_text: PostTextStr

## Response Fields
class ReplyResponse(BaseModel):
    platform:str
    post_text:str
    tone:str
    intent:str
    draft:str
    reply:str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

## Endpoint to generate a reply 
@app.post("/reply", response_model=ReplyResponse)
async def generate_reply(req: ReplyRequest):
    try:
        builder = ReplyPipeline(llm)
        result = await builder.run_pipeline(req.platform, req.post_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

    doc = {
        "platform": result["platform"],
        "post_text": result["post_text"],
        "reply": result["reply"],
        "tone": result["tone"],
        "intent": result["intent"],
        "draft": result["draft"],
        ##"timestamp": result["ts"],
        "timestamp": datetime.datetime.utcnow()
    }
  
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        ## Create the table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_replies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        platform VARCHAR(50),
        post_text TEXT,
        reply TEXT,
        timestamp DATETIME);""")
        ## Insert the data into the table
        query = """
        INSERT INTO post_replies (platform, post_text, reply, timestamp)
        VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (doc.get("platform"), doc.get("post_text"), doc.get("reply"), doc.get("timestamp")))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        raise HTTPException(status_code=500, detail="Database connection failed.")

    return ReplyResponse(**doc)
    

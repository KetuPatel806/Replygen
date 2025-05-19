import os
from dotenv import load_dotenv

from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool

__all__ = [
    "get_vector_retriever_tool",
]

## Load the Hugging Face token from environment variables
def _load_env_token(var_name: str = "HF_TOKEN") -> str:
    """Load the Hugging Face token from environment variables.

    Raises a *RuntimeError* if the variable is not found so that the caller
    fails fast instead of silently creating an unauthenticated client.
    """
    load_dotenv()
    token = os.getenv(var_name)
    if token is None:
        raise RuntimeError(f"{var_name} not found in environment variables")
    os.environ[var_name] = token  
    return token

## load the Excel file and return documents
def _load_documents(file_path: str):
    """Read an Excel file with *UnstructuredExcelLoader* and return documents."""
    loader = UnstructuredExcelLoader(file_path=file_path)
    docs = loader.load()
    return docs

## Split the documents data into smaller chunks
def _split_documents(docs, *, chunk_size: int = 1000, chunk_overlap: int = 100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(docs)

## Vector store creation
def _build_vector_store(docs_split):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.from_documents(docs_split, embeddings)

## Create a retriever tool
def get_vector_retriever_tool(
    file_path: str,
    *,
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
):
    """Create and return a LangChain *retriever tool* backed by a FAISS index.

    Parameters
    ----------
    file_path : str
        Path to the Excel file to ingest.
    chunk_size : int, default 1000
        Max characters per chunk before embedding.
    chunk_overlap : int, default 100
        Overlap characters between chunks.
    """
    _load_env_token()

    docs = _load_documents(file_path)

    docs_split = _split_documents(
        docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    db = _build_vector_store(docs_split)
    retriever = db.as_retriever()

    return create_retriever_tool(
        retriever,
        name="retriever_vector_db",
        description="Search the information from the data",
    )

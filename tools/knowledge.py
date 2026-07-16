import os

from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS


def load_knowledge_base(base_url: str, knowledge_dir: str):
    """Load and index documents from the knowledge directory. Returns the retriever and search tool."""

    embeddings = OpenAIEmbeddings(
        base_url=base_url,
        api_key="lm-studio",
        model="text-embedding-nomic-embed-text-v1.5",
        check_embedding_ctx_length=False,
    )

    print("Loading knowledge base...")
    docs = []
    for filename in os.listdir(knowledge_dir):
        filepath = os.path.join(knowledge_dir, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            docs.extend(loader.load())
        elif filename.endswith(".txt"):
            loader = TextLoader(filepath)
            docs.extend(loader.load())
        elif filename.endswith(".md"):
            loader = TextLoader(filepath)
            docs.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    vector_store = FAISS.from_documents(splits, embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    print(f"Indexed {len(splits)} chunks from {len(docs)} pages.")

    @tool
    def search_knowledge(query: str) -> str:
        """Search the knowledge base for information about the user's work history, skills, accomplishments, and performance reviews."""
        results = retriever.invoke(query)
        if not results:
            return "No relevant information found in the knowledge base."
        chunks = []
        for doc in results:
            source = os.path.basename(doc.metadata.get("source", "unknown"))
            page = doc.metadata.get("page", "?")
            chunks.append(f"[Source: {source}, Page {page}]\n{doc.page_content}")
        return "\n\n---\n\n".join(chunks)

    return search_knowledge

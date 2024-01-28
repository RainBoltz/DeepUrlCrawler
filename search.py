from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class Search:
    def __init__(self, corpus_name):
        self.data_dir = "./data/chroma_db"
        self.corpus_name = corpus_name
    
    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def LLMChat(self, question):
        # Retrieve and generate using the relevant snippets of the blog.
        vectorstore = Chroma(persist_directory=f"{self.data_dir}/{self.corpus_name}", embedding_function=OpenAIEmbeddings())

        retriever = vectorstore.as_retriever()
        prompt = hub.pull("rlm/rag-prompt")
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        rag_chain = (
            {"context": retriever | self.format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        return rag_chain.invoke(question)

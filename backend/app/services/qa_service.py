from langchain_community.llms import HuggingFacePipeline
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class QAService:
    def __init__(self, vector_store):
        # Initialize the model and tokenizer
        model_name = "google/flan-t5-base"  # You can also try 'large' version if you have more RAM
        
        # Create the pipeline
        self.llm = HuggingFacePipeline.from_model_id(
            model_id=model_name,
            task="text2text-generation",
            model_kwargs={"device_map": "auto"},  # Will use GPU if available
            pipeline_kwargs={"max_length": 512}
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vector_store.as_retriever(),
            memory=self.memory,
            return_source_documents=True
        )

    async def generate_answer(self, question: str, chat_history: list):
        """
        Generates answer with citations using the RAG pipeline
        """
        result = self.qa_chain({"question": question})
        
        sources = []
        for doc in result["source_documents"]:
            sources.append({
                "page": doc.metadata["page_number"],
                "source": doc.metadata["source"]
            })
            
        return {
            "answer": result["answer"],
            "sources": sources
        } 
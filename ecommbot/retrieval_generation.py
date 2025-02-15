import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from ecommbot.ingest import ingestdata
from dotenv import load_dotenv


load_dotenv()
GEMINI_API_KEY= os.getenv('GOOGLE_API_KEY')

def generation(vstore):
    retriever = vstore.as_retriever(search_kwargs={"k": 3})

    PRODUCT_BOT_TEMPLATE = """
    Your ecommercebot bot is an expert in product recommendations and customer queries.
    It analyzes product titles and reviews to provide accurate and helpful responses.
    Ensure your answers are relevant to the product context and refrain from straying off-topic.
    Your responses should be precise and informative. If your getting any other question 
    which is not related to product, try to answer that question with your own knowledge.
    If you receive messages such as "hi," "hello," or "how are you," respond politely and 
    concisely without including any product-related information.

    CONTEXT:{context}
    QUESTION: {question}

    YOUR ANSWER:
    """

    prompt = ChatPromptTemplate.from_template(PRODUCT_BOT_TEMPLATE)

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)

    chain= ({"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser())
    
    return chain

if __name__=='__main__':
    vstore = ingestdata("done")
    chain  = generation(vstore)
    print(chain.invoke("can you tell me the best bluetooth buds?"))
    
    
    
    
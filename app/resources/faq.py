import pandas as pd
from  pathlib import Path ### we  are using this so that we can get the absolute path of our directory
import chromadb ### langchain api keeps on changing so i used chrom db
from groq import Groq
from dotenv import load_dotenv
from chromadb.utils import embedding_functions
import os

load_dotenv() ## it will create those two environment variables ,grok api key ,and grok model


# Path(__file__).parent ## it will give us the path till app

faqs_path=Path(__file__).parent /"faq_data.csv"
chroma_client=chromadb.Client()
collection_name_faq='faqs'


ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name='sentence-transformers/all-MiniLM-L6-v2' ### all-MiniLM is default model
        )

def ingest_faq_data(path): ## #####it will ingest the datainto chroma db
    if collection_name_faq  not in [c.name for c in chroma_client.list_collections()]:
        print("Ingesting FAQ data into  Chromadb...")
        collection=chroma_client.get_or_create_collection(## here we are creating collection
            name=collection_name_faq,
            embedding_function= ef
            )
        df=pd.read_csv(path)
        docs=df['question'].to_list() ## why we are storing the question and not the answer
        ## we are using  only the questions into the  document part of chromadb (you want to generate embedding for question),
        ##### because the user will ask question  we are doing similarity matching with the question and not with the answer
        ####### we can store the answer into meta data
        metadata=[{'answer': ans} for ans in df['answer'].to_list()] ## meta data are the list of dictonary or json object

        ids=[f"id_{i}" for i in range(len(docs))]
        collection.add(
            documents=docs,
            metadatas=metadata,
            ids=ids
        )
        print(f"FAQ Data sucessfully ingested into Chrom collection: {collection_name_faq}")
    else:
        print(f"Collection {collection_name_faq} already_exist")

def get_releveant_qa(query):
    collection=chroma_client.get_collection(name=collection_name_faq)
    result=collection.query(
        query_texts=[query],
        n_results=2
    )
    return result

def faq_chain(query): ## it will take query as as input and return you the final answer
    result=get_releveant_qa(query)### from this result we want to form an context and that context i want to give it to llm
    context=''.join([r.get('answer') for r in result['metadatas'][0]])
    answer=generate_answer(query,context)
    return answer
def generate_answer(query,context):
    prompt= f'''Given the question and context below,generate the answer based on the context only.
    If you don't find the answer inside the context then say "I don't know".
    Do not make things up.
    QUESTION:{query}
    CONTEXT:{context}
    '''
    groq_client=Groq()
    chat_completion = groq_client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": prompt
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": query,
        }
    ],

    # The language model which will generate the completion.
    model=os.environ['GROQ_MODEL']
)

# Print the completion returned by the LLM.
    return chat_completion.choices[0].message.content


    

if __name__=="__main__":
    
    ingest_faq_data(faqs_path)
    query="what's your policy on defective products?"
    # result=get_releveant_qa(query)
    # print(result)

    answer=faq_chain(query)
    print(answer)
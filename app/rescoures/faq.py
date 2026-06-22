import pandas as pd
from  pathlib import Path ### we  are using this so that we can get the absolute path of our directory
import chromadb ### langchain api keeps on changing so i used chrom db

from chromadb.utils import embedding_functions

# Path(__file__).parent ## it will give us the path till app

faqs_path=Path(__file__).parent /"/resources/faq_data.csv"
chroma_client=chromadb.Client()
collection_name_faq='faqs'


ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name='sentence-transformers/all-MiniLM-L6-v2' ### all-MiniLM is default model
        )

def ingest_faq_data(path): ## it will ingest the datainto chroma db
    if collection_name_faq in [c.name for c in chroma_client.list_collections()]:
        print("Ingesting FAQ data into  Chromadb...")
        collection=chroma_client.get_or_create_collection(name=collection_name_faq ,## here we are creating collection
            name=collection_name_faq, 
            embedding_function= ef
            )
        df=pd.read_csv(path),
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


if __name__=="__main__":
    
    ingest_faq_data(faqs_path)
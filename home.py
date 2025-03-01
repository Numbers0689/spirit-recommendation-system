import streamlit as st
import pymongo
import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from bson.binary import Binary
import pickle

user = st.secrets["USER"]
password = st.secrets["PASSWORD"]
uri_url = st.secrets["URI_URL"]

uri = f"mongodb+srv://{user}:{password}@{uri_url}/?retryWrites=true&w=majority&appName=Cluster0"

client = pymongo.MongoClient(uri)
db = client("spirit")
collection = db("recommendations")

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Spirit recommendation system")

st.divider()

st.image("https://i.pinimg.com/originals/b3/31/d6/b331d6d35d9de9cd10dc157d72f5c61b.jpg")
st.subheader("Fill the questionnaire to get your recommendation")

user_name = st.text_input("What's your name?")
fav_browser = st.text_input("what's your favorite browser?")
fav_editor = st.text_input("what's your favourite code editor?")
fav_lang = st.text_input("whats your preferred programming language?")
fav_movie = st.text_input("whats your favourite movie?")
fav_drink = st.text_input("whats your go to drink?")
user_desc = st.text_area("Tell us about yourself")

def get_embedding(text):
    resp = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return resp.data[0].embedding


def save_response_to_db(responses, embedding):
    result = collection.insert_one({
        "responses": responses,
        "embedding": Binary(pickle.dumps(embedding)) 
    })
    return result.inserted_id 


def find_match(current_embedding, current_user_id):
    all_responses = list(collection.find())
    similarities = []

    for doc in all_responses:
        if doc['_id'] == current_user_id:
            continue
        
        stored_embedding = pickle.loads(doc['embedding'])
        similarity = cosine_similarity([current_embedding], [stored_embedding])[0][0]
        similarities.append((similarity, doc['responses']))

    similarities.sort(reverse=True, key=lambda x: x[0])
    
    return similarities[0][1] if similarities else None


if st.button("submit"):
    if user_name and fav_browser and fav_editor and fav_lang and fav_movie and fav_drink and user_desc:
        responses = {
            "user_name": user_name,
            "fav_browser": fav_browser,
            "fav_editor": fav_editor,
            "fav_lang": fav_lang,
            "fav_movie": fav_movie,
            "fav_drink": fav_drink,
            "user_desc": user_desc
        }

        responses_text = " ".join(responses.values())
        current_embedding = get_embedding(responses_text)

        current_user_id = save_response_to_db(responses, current_embedding)

        match = find_match(current_embedding, current_user_id)
        if match:
            top_match_similarity, top_match_responses = match[0]
            st.success(f"Match found! : {match}")
            st.write(f"Similarity score: {top_match_similarity}")
        else:
            st.warning("No matches found. You are a first!")
    else:
        st.warning("Please fill all the fields")

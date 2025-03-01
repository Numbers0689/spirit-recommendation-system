import streamlit as st

user = st.secrets["USER"]
password = st.secrets["PASSWORD"]
uri_url = st.secrets["URI_URL"]

st.title("Spirit recommendation system")

st.divider()

st.image("https://i.pinimg.com/originals/b3/31/d6/b331d6d35d9de9cd10dc157d72f5c61b.jpg")
st.subheader("Fill the questionnaire to get your recommendation")

fav_browser = st.text_input("what's your favorite browser?")
fav_editor = st.text_input("what's your favourite code editor?")
fav_lang = st.text_input("whats your preferred programming language?")
fav_movie = st.text_input("whats your favourite movie?")
fav_drink = st.text_input("whats your go to drink?")

if st.button("submit"):
    #other stuff
    st.success("Match has been found!")
else:
    st.warning("Please answers all the questions.")

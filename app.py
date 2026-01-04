#Author - Jaimie Neilson
#Student no. - B01831071
#Project - GameSultan Predictor
#Version - 1.0
# Date - 02/11/2025
# 1.1 Update - 06/12/25
# 1.2 update - 04/01/26

#** Emojis are not AI generated. They were found here : https://www.webfx.com/tools/emoji-cheat-sheet/ **

# Using streamlit as my preferred method to display statistical information.
import streamlit as st

# because this project only requires a CSV, this imports it and saves the generated data to it.
# Calling the functions from the Functions.py file.
from pages.Functions import save_user_data, get_logo

st.set_page_config(
    page_title="🧞‍♂️ GameSultan - Game trend predictor",
    layout="centered"
)
#To display the Logo here.
logo = get_logo()
if logo:
    st.image(logo, width = 500)
else:
    st.warning("Logo not found!..")

#This is collecting the user's information.
with st.form("user_input"):
    name = st.text_input("📛 And you are?(Name)")
    age = st.text_input("🎂 Of how many years?(Age)")
    email = st.text_input("📨 Your digital postbox?(Email)")
    genre = st.selectbox("📚 What is your favourite genre?", ["Please select..", "Action", "Simulation", "RPG", "Sports", "Horror", "Puzzle", "Strategy"])
    hours = st.selectbox("🕑 How many hours do you play? (Average)", ["Please select..", "0-3", "4-6", "7-10", "10+"])
    console = st.selectbox("🎮 Which device do you use more?", ["Please select..", "PC", "Xbox series X", "Playstation 5", "Nintendo Switch", "Nintendo Wii", "Mobile"])
    submit = st.form_submit_button("Sultan thanks you!")

#Ensuring the correct fields are completed. Error handling!.
if submit:
    if(
        not name.strip() or not age.strip or not email.strip() or genre == "Please select.." or hours == "Please select.." or console == "Please select.."):
        st.error("The Sultan can't help you, If you can't help the Sultan!")
    else:
        user_data = {
            "name": name,
            "age": age,
            "email": email,
            " genre": genre,
            " hours": hours,
            " console": console,
        }
        save_user_data(user_data)
        st.success(f"The Sultan thanks you {name}! Your details are a kept secret now!")

        #Keeps the fields empty.
        for field in ["name", "age", "email", "genre", "hours", "console"]:
            if field in st.session_state:
                del st.session_state[field]

st.page_link("pages/Prediction.py", label = "Click to prophesise")


#streamlit run app.py

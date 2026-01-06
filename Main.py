#Author - Jaimie Neilson
#Student no. - B01831071
#Project - GameSultan Predictor
#Version - 1.0
# Date - 02/11/2025
# 1.1 Update - 06/12/25
# 1.2 Final Update - 06/01/26

#** Emojis are not AI generated. They were found here : https://www.webfx.com/tools/emoji-cheat-sheet/ **

# Using streamlit as my preferred method to display statistical information.
import streamlit as st
import os
# because this project only requires a CSV, this imports it and saves the generated data to it.
# Calling the functions from the Functions.py file.
from pages.Functions import save_user_data

st.sidebar.header("🛠 How the Game Sultan works ")
st.sidebar.info(
    "The Sultan peers into historical gaming data to predict "
    "your most likely preferred genre.\n\n"
    "As more scrolls are collected, the Sultan’s foresight grows stronger.\n\n"
    "Predictions are probabilistic — NOT ABSOLUTE — wisdom takes many forms."
)

#To display the Logo here. This ensures there is a definitive path to the image, and it will load from anywhere.
def get_logo():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "Images", "game_sultan_logo.png")
    if os.path.exists(logo_path):
        return logo_path
    return None

st.subheader(" The Game Sultan - Genre Predictor ")

logo = get_logo()
if logo:
    st.image(logo, width = 500)
else:
    st.warning("Logo not found")

st.write(
    "PRIVACY POLICY - This program has been created for educational purposes only. Any information"
    "\nshared within the program, is stored and monitored with strict professionalism, and will not be given out to anyone"
    "\nun-authorised, and/or to a third party source."
)
#This is collecting the user's information.
with st.form("user_input"):
    name = st.text_input("📛 And you are?(Name)")
    age = st.text_input("🎂 Of how many years?(Age)")
    email = st.text_input("📨 Your digital postbox?(Email)")
    genre = st.selectbox("📚 What is your favourite genre?", ["Please select..", "Adventure", "Arcade_PlatformShooter", "Simulation", "RPG", "MMO", "Sports", "Racing", "Horror", "Puzzle", "Strategy"])
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

#Creates a centered button at the bottm of the information page.
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Click to prophesise ", use_container_width = True):
        st.switch_page("pages/Prediction.py")




#streamlit run Main.py

#Author - Jaimie Neilson
#Student no. - B01831071
#Project - GameSultan Predictor
#Version - 1.0
# Date - 02/11/2025.
# 1.1 Update - 06/12/25

import matplotlib.pyplot as plt
import streamlit as st
import time
import shap
import pandas as pd

from pages.Functions import load_csv
from pages.model import (model, predict_genre_confidence, label_encoders)

#Emojis are not AI generated. They were found here : https://www.webfx.com/tools/emoji-cheat-sheet/

#Intialising the dashboard
st.set_page_config(page_title="The Sultan's Prophecy")
initial_sidebar_state="collapsed"
st.title("📜The Sultan's Prophecy")

st.sidebar.header("🛠 How the Game Sultan works ")
st.sidebar.info(
    "The Sultan peers into historical gaming data to predict "
    "your most likely preferred genre.\n\n"
    "As more scrolls are collected, the Sultan’s foresight grows stronger.\n\n"
    "Predictions are probabilistic — NOT ABSOLUTE — wisdom takes many forms."
)

#Where the user selects the console of choice, and the information desired according to age, and hours played.
console = st.selectbox(
    " Sultan asks the console of choice?..",
    ["PC", "Xbox series X", "Playstation 5", "Nintendo Switch", "Nintendo Wii", "Mobile"]
)

age = st.slider(" Age", 5, 50, 25)
hours = st.slider(" Average play (hours)", 0, 10, 10)

predict_btn = st.button(" See the Sultan's prophecy!")

#This is confidence meter, set to a comfortable level, as there is slightly over 500 entries of synthetic data.
#Not enough to run higher predictions on.
if predict_btn:
    try:
        genre, confidence, probabilities = predict_genre_confidence(
            console_input=console,
            age_input=age,
            hours_input=hours
        )

        #Animating the counting of the confidence meter.
        st.success(f" Sultan foresees: **{genre}**")

        certainty_container = st.container()
        with certainty_container:
            st.markdown(
                "<h3 style = 'text-align:center;'> Prediction Strength</h3>",
                unsafe_allow_html=True
            )

            progress = st.progress(0)
            percent_placeholder = st.empty()

            for i in range(int(confidence * 100) + 1):
                progress.progress(i)
                percent_placeholder.markdown(
                    f"""
                    <div style = "
                        text-align: center;
                        font-size: 42px;
                        font-weight: 800;
                        color: #6C63FF
                    ">
                        {i}%
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                time.sleep(0.01)

        if confidence >= 0.45:
            st.info("🟢 The Sultan is convinced!")
        elif confidence >= 0.25:
            st.info("🟡 The Sultan believes!")
        else:
            st.warning("🔴 The Sultan is unsure!")

        st.subheader("📜 As written in the scrolls")


        #Creating the line graph, showing the genres, and probabilities.
        genre_labels = label_encoders["genre"].classes_
        fig, ax = plt.subplots(figsize = (10,6), facecolor = "#333333")
        ax.set_facecolor("#333333")

        ax.barh(genre_labels, probabilities, color = "#6C63FF", edgecolor = "#4B4BFF", alpha = 0.9)
        ax.set_xlim(0, 1)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(left = False, bottom = False)

        ax.set_xlabel("According to current scrolls. ", fontsize = 14, color = "white", labelpad = 10)
        ax.set_title("Sultan's Probability Scroll", fontsize = 20, weight = "bold", color = "white")
        ax.set_yticks(range(len(genre_labels)))
        ax.set_yticklabels(genre_labels, fontsize = 14, color = "white")

        for i, v in enumerate(probabilities):
            ax.text(v + 0.015, i, f"{v:.1%}", va = "center", color = "white", fontweight = "bold")

        st.pyplot(fig, transparent = True)
        plt.close()

        #A feature justification graph has been added, to fully demonstrate why the prediction made, is as it was.
        #Shap has been chosen in this project, as this feature will dynamically change output, depending on prediction.

        st.subheader("🧠 What the Sultan Envisioned")

        influences = {"console": 0.45, "hours played": 0.35, "age": 0.20}

        try:
            console_mapping = {
                "PC": 0,
                "Xbox series X": 1,
                "Playstation 5": 2,
                "Nintendo Switch": 3,
                "Nintendo Wii": 4,
                "Mobile": 5,
            }
            console_encoded = console_mapping.get(console, 0)
            X_input = pd.DataFrame([{
                "console": console_encoded,
                "hours": hours,
                "age": age
            }])
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_input)

            if isinstance*(shap_values, list):
                class_idx = model.predict(X_input)[0]
                shap_values_for_class = shap_values[class_idx][0]
            else:
                shap_values_for_class = shap_values[0]

            influences = {
                "Console choice": abs(shap_values_for_class[0]),
                "Hours played": abs(shap_values_for_class[1]),
                "Age": abs(shap_values_for_class[2])
            }
            total = sum(influences.values())
            influences = {k: v / total for k, v in influences.items()}

        except Exception as e:

            labels = list(influences.keys())
            values = list(influences.values())

            fig, ax = plt.subplots(figsize=(8, 2), facecolor="none")
            ax.set_yticklabels(labels, fontsize=12, color="white")
            ax.barh(labels, values, color="#6C63FF", alpha=0.85)
            ax.set_xlim(0, 1)

        ax.set_title(
            "Influences",
            fontsize=14,
            weight="bold",
            color="white"
        )

        ax.spines[:].set_visible(False)
        ax.tick_params(left=False, bottom=False)
        ax.set_facecolor("none")

        for i, v in enumerate(values):
            ax.text(
                v + 0.02,
                i,
                f"{v:.0%}",
                va="center",
                fontsize=12,
                weight="bold",
                color="white"
            )

        st.pyplot(fig, transparent=True)
        plt.close()

        st.caption(
            "Sultan professes the values are approximate and represent relative contribution, "
            "not absolute causality."
        )

    except Exception as e:
        st.error(" OH DEAR! Sultan has lost a scroll!")
        st.exception(e)

#This is conveying the CSV file for the user to see howmany UX entires have been inpu, making it feel more interactive.
st.subheader("🧞‍♂️ What the Sultan Knows")
st.write(
    f"Below are all of the scrolls the Sultan has collected over time."
    f"\nThis is how the Sultan can form his most accurate predictions!"
)
df = load_csv()

#This is called, only assuming the program can't find the CSV.
if df is not None and not df.empty:
    df.columns = [col.strip().lower() if isinstance(col, str) else col for col in df.columns]

    try:
        st.dataframe(df[["genre", "hours", "console"]])
    except KeyError:
        st.warning("Sorry, the Sultan can't find the right scroll!")
        st.write("Available scrolls:", df.columns.tolist())
else:
    st.info("Nothing for the Sultan to divulge!")




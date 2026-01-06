#Author - Jaimie Neilson
#Student no. - B01831071
#Project - GameSultan Predictor
#Version - 1.0
# Date - 02/11/2025.
# 1.1 Update - 06/12/25
# 1.2 Final Update - 06/01/26

import os
import time
import matplotlib.pyplot as plt
import streamlit as st

from pages.Functions import load_csv
from pages.model import (predict_genre_confidence, label_encoders)

#Specifically important, as this helps to ensure the path to the images is visible, and correct.
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "Images"

#Emojis are NOT AI generated. They were found here : https://www.webfx.com/tools/emoji-cheat-sheet/

GENRE_FOLDER_MAP = {
    "Adventure": "Adventure",
    "Arcade_PlatformShooter": "Arcade_PlatformShooter",
    "Horror": "Horror",
    "Racing": "Racing",
    "RPG": "RPG",
    "MMO": "MMO",
    "Simulation": "Simulation",
    "Sports": "Sports",
    "Strategy": "Strategy",
    "Puzzle": "Puzzle",
}

#Ensuring that special characters are considered in the search. All variables included.
def prettify_genre(label: str) -> str:
    return (
        label
        .replace("/", " / ")
        .replace("_", " ")
        .replace("PlatformShooter", "Platform Shooter")
        .strip()
    )

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

#This is preparing the images for the recommendation feature towards the end of the experience.
# The function is trying to ensure an absolute path to the image folders, and corresponding images respectively.
def get_genre_recommendations(genre, base_path = "Images", limit = 4):
    genre_path = os.path.join(base_path, genre)
    if not os.path.exists(genre_path):
        return[]

    images = [
        img for img in os.listdir(genre_path)
        if img.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
    return images[:limit]
#Where the user selects the console of choice, and the information desired according to age, and hours played.
console = st.selectbox(
    " Sultan asks for the console of choice?..",
    ["PC", "Xbox series X", "Playstation 5", "Nintendo Switch", "Nintendo Wii", "Mobile"]
)

age = st.slider("The age of the gamer?", 5, 50, 25)
hours = st.slider("The average play duration? (hours)", 0, 10, 10)

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

        st.subheader("📜 As written in the Scrolls")
        st.write(
            "From the visions shown, the Sultan could see this genre as the true favorite, \n and why this scroll of probability"
            "\nis the wisest choice the Sultan could make!  "
        )

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

        ax.set_xlabel("Foretold in the Scrolls. ", fontsize = 14, color = "white", labelpad = 10)
        ax.set_title("Scroll of Probability ", fontsize = 20, weight = "bold", color = "white")
        ax.set_yticks(range(len(genre_labels)))
        ax.set_yticklabels(genre_labels, fontsize = 14, color = "white")

        for i, v in enumerate(probabilities):
            ax.text(v + 0.015, i, f"{v:.1%}", va = "center", color = "white", fontweight = "bold")

        st.pyplot(fig, transparent = True)
        plt.close()

        #A feature justification graph has been added, to fully demonstrate why the prediction made, is as it was.
        #It utilises weighting to dynamically interpret the results.
        st.subheader("🧠 The Sultans Visions")
        st.write(
            "Combined with the scroll of probability, comes the scroll of influence, The Sultan's prediction"
            "\n was influenced by these factors : "
        )
        base_importance = {"Console choice": 0.5, "Hours played": 0.3, "Age": 0.2}

        console_weight = 1.0
        hours_weight = min(hours / 10, 1) * 1.2
        age_weight = 1 - abs(age - 25) / 25

        dynamic_influences = {
            "Console choice": base_importance["Console choice"] * console_weight,
            "Hours played": base_importance["Hours played"] * hours_weight,
            "Age": base_importance["Age"] * age_weight,
        }

        #Converts to a normalised percentage
        total = sum(dynamic_influences.values())
        influences = {k: v / total for k, v in dynamic_influences.items()}

        labels = list(influences.keys())
        values = list(influences.values())

        fig, ax = plt.subplots(figsize=(8, 2), facecolor="none")
        ax.barh(labels, values, color = "#6c63ff", alpha = 0.9)
        ax.set_yticklabels(labels, fontsize=12, color="white")
        ax.set_xlim(0, 1)

        ax.set_title(
            "Scroll of Influence",
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

        st.subheader("🎮 The Sultan's Selection")
        st.write("With Sultan's visions, He could see many options. The Sultan has personally chosen this selection"
                 "\nof some exciting ideas for your next possible adventure. ")

        folder_name = GENRE_FOLDER_MAP.get(genre, genre)
        if not folder_name:
            st.warning("The Sultan has misplaced this scroll at present. ")
        else:
            genre_path = IMAGES_DIR / folder_name

            if not genre_path.exists():
                st.error("This scroll is not in the archive currently. ")
            else:
                images = [
                    img for img in genre_path.iterdir()
                    if img.suffix.lower()in [".jpg", ".jpeg", ".png"]
                ][:4]

                if not images:
                    st.warning(" The sultan has the scroll, but not vision of the games. ")
                else:
                    GAME_INFO = {
                        # Adventure Titles.
                        "eldenring_nightreign.jpg": {
                            "title": "Elden Ring - Nightreign", "released": 2025,
                            "story": "Become the Nightfayrer and defeat the eight dark overlords threatening the realm."},

                        "hollowknight_silksong.jpg": {
                            "title": "Hollow Knight - Silksong", "released": 2024,
                            "story": "Uncover the secrets of a mysterious kingdom plagued by corruption and strange creatures."},

                        "monsterhunter_wilds.jpg": {
                            "title": "Monster Hunter - Wilds", "released": 2025,
                            "story": "Embark on a thrilling hunt across dangerous landscapes to defeat legendary monsters."},

                        "ninjagaiden4.jpg": {
                            "title": "Ninja Gaiden 4", "released": 2023,
                            "story": "Master the way of the ninja and defeat powerful enemies to restore honor to your clan."},


                        #MMO Titles
                        "world_of_warcraft.jpg": {
                            "title": "World of Warcraft", "released": 2004,
                            "story": "Enter the vast world of Azeroth, where players embark on epic quests, battle powerful foes, and forge alliances in a living fantasy universe."},

                        "final_fantasy_xiv.jpg": {
                            "title": "Final Fantasy XIV", "released": 2013,
                            "story": "Experience a rich, story-driven MMORPG filled with stunning worlds, deep characters, and cooperative battles against legendary enemies."},

                        "elder_scrolls_online.jpg": {
                            "title": "The Elder Scrolls Online", "released": 2014,
                            "story": "Explore the continent of Tamriel with friends, uncover ancient secrets, and shape your own destiny in this expansive online RPG."},

                        "guild_wars_2.jpg": {
                            "title": "Guild Wars 2", "released": 2012,
                            "story": "Join a dynamic world where player choices shape events, featuring fast-paced combat and a strong focus on cooperative play."},


                        #Arcade_PlatformShooter Titles.
                        "cuphead.jpg": {
                            "title": "Cuphead", "released": 2017,
                             "story": "Battle bizarre bosses and survive hand-drawn levels in this challenging run-and-gun platform shooter inspired by 1930s cartoons."},

                        "metal_slug_x.jpg": {
                            "title": "Metal Slug X", "released": 1999,
                            "story": "Fight through chaotic battlefields packed with enemies, explosions, and classic arcade action in this fast-paced shooter."},

                        "contra_rogue_corps.jpg": {
                            "title": "Contra: Rogue Corps", "released": 2019,
                            "story": "Deliver intense twin-stick shooting action as you blast through alien-infested environments with relentless firepower."},

                        "broforce.jpg": {
                            "title": "Broforce", "released": 2015,
                            "story": "Unleash over-the-top explosive action as iconic heroes fight through destructible levels in this chaotic platform shooter."},


                        # Horror Titles
                        "amnesia_dark_descent.jpg": {
                            "title": "Amnesia: Dark Descent", "released": 2010,
                            "story": "Explore a dark, eerie castle while avoiding terrifying monsters and uncovering hidden secrets."},

                        "deadbydaylight.jpg": {
                            "title": "Dead by Daylight", "released": 2016,
                            "story": "Multiplayer survival horror—escape, survive, or face a gruesome end at the hands of the killer."},

                        "outlast.jpg": {
                            "title": "Outlast", "released": 2013,
                            "story": "Investigate a sinister asylum and document the horrors within while trying to survive."},

                        "residentevil_village.jpg": {
                            "title": "Resident Evil Village", "released": 2021,
                            "story": "Survive in a terrifying European village overrun by dark, demonic forces."},


                        # Racing Titles.
                        "formula1_2025.jpg": {
                            "title": "F1 2025", "released": 2025,
                            "story": "Step into the cockpit and compete for the championship in the high-speed world of Formula 1."},

                        "forza_horizon_5.jpg": {
                            "title": "Forza Horizon 5", "released": 2024,
                            "story": "Cruise through the vibrant landscapes of Mexico, complete races, and explore an open-world racing playground."},

                        "need_for_speed_unbound.jpg": {
                            "title": "Need for Speed: Unbound", "released": 2024,
                            "story": "Evade the police and dominate street races with style and precision in this high-octane racing adventure."},

                        "world_rally_championship.jpg": {
                            "title": "World Rally Championship", "released": 2025,
                            "story": "Test your driving skills across challenging rally tracks and compete to become a world rally champion."},


                        # RPG Titles.
                        "death_stranding_2.jpg": {
                            "title": "Death Stranding 2", "released": 2025,
                            "story": "Reconnect isolated communities as Sam Porter, navigating a fractured world filled with danger and mystery."},

                        "diablo_4.jpg": {
                            "title": "Diablo IV", "released": 2023,
                            "story": "Battle the dark forces of Lilith and her minions in a realm full of demons and peril."},

                        "expedition_33_clair_obscur.jpg": {
                            "title": "Expedition 33 - Clair Obscur", "released": 2025,
                            "story": "Lead a team on a perilous expedition to uncover secrets and defeat the mysterious Paintress."},

                        "kingdom_come_2_deliverance.jpg": {
                            "title": "Kingdom Come 2 - Deliverance", "released": 2025,
                            "story": "Ride through an open-world medieval Czech Republic, facing realistic challenges and epic battles."},


                        # Simulation Titles.
                        "city_skyline_2.jpg": {
                            "title": "Cities Skyline 2", "released": 2023,
                            "story": "Build and manage your dream city, balancing growth, resources, and citizens' happiness."},

                        "farming_simulator_25.jpg": {
                            "title": "Farming Simulator 25", "released": 2025,
                            "story": "Become a legendary farmer, grow crops, raise livestock, and manage your own farm empire."},

                        "microsoft_flight_simulator_2025.jpg": {
                            "title": "Microsoft Flight Simulator 2025", "released": 2025,
                            "story": "Take to the skies and experience realistic aviation adventures in the world's most iconic aircraft."},

                        "powerwash_simulator_2.jpg": {
                            "title": "Powerwash Simulator 2", "released": 2025,
                            "story": "Clean and restore the world one surface at a time with your trusty power washer."},


                        # Sport Titles.
                        "fc_25.jpg": {
                            "title": "FC 25", "released": 2025,
                            "story": "Lead your football club to glory, train your players, and conquer leagues worldwide."},

                        "nba_2k25.jpg": {
                            "title": "NBA 2K25", "released": 2025,
                            "story": "Take control of the court, build your MyPlayer, and compete against the world's best basketball stars."},

                        "pga_2k25.jpg": {
                            "title": "PGA 2K25", "released": 2025,
                            "story": "Compete on the world's most famous golf courses and aim for tournament victory."},

                        "rugby_25.jpg": {
                            "title": "Rugby 25", "released": 2025,
                            "story": "Lead your team to victory in the Six Nations or global championships."},


                        # Strategy Titles.
                        "civilization_7.jpg": {
                            "title": "Civilization 7", "released": 2025,
                            "story": "Lead your civilization from the ancient era to the future, making strategic decisions to dominate the world."},

                        "age_of_empires_5.jpg": {
                            "title": "Age of Empires 5", "released": 2025,
                            "story": "Build armies, expand your empire, and conquer rival civilizations in real-time strategy battles."},

                        "total_war_kingdoms.jpg": {
                            "title": "Total War: Kingdoms", "released": 2024,
                            "story": "Command mighty armies, manage kingdoms, and crush enemies in epic battles across vast lands."},

                        "stellaris_2.jpg": {
                            "title": "Stellaris 2", "released": 2025,
                            "story": "Explore galaxies, manage interstellar empires, and engage in diplomacy and warfare with alien civilizations."},

                        # Puzzle Titles.
                        "portal_3.jpg": {
                            "title": "Portal 3", "released": 2025,
                            "story": "Solve mind-bending puzzles using portals in a mysterious and challenging facility."},

                        "the_witness_2.jpg": {
                            "title": "The Witness 2", "released": 2025,
                            "story": "Explore a beautiful island filled with hundreds of intricate puzzles and hidden secrets."},

                        "tetris_modern.jpg": {
                            "title": "Tetris: Modern", "released": 2024,
                            "story": "Classic falling block puzzle gameplay with modern twists and multiplayer modes."},

                        "baba_is_you_2.jpg": {
                            "title": "Baba Is You 2", "released": 2025,
                            "story": "Manipulate the rules of the game itself to solve creative and challenging logic puzzles."},
                    }

                    #Creating the direct path to the Images, and ensures the file types mentioned have to be present.
                    #by using iterdir, this helps to correctly list all the files within the directory.
                    images = [img for img in genre_path.iterdir() if img.suffix.lower() in [".jpg", ".jpeg", ".png"]][:4]

                    #This statement is making sure the titles details are present and then proceeds to display the information in its position.
                    if not images:
                        st.warning("Sultan has the scroll, but can't envision the game")
                    else:
                        for i in range(0, len(images), 2):
                            cols = st.columns(2)
                            for col, img_path in zip(cols, images[i:i+2]):
                                img_name = img_path.name
                                info = GAME_INFO.get(img_name, {"title": img_name, "released": "", "story": "What prophecy is revealed?"})
                                with col:
                                    st.image(str(img_path), use_container_width = True)
                                    st.markdown(f"**{info['title']}**")
                                    st.markdown(f"*Released:* {info['released']}")
                                    st.markdown(f"*Story:* {info['story']}")

        # This is conveying the CSV file for the user to see how many user entries have been input, making it feel more interactive.
        st.subheader("🧞‍♂️ What the Sultan Knows")
        st.write(
            f"Below are all of the scrolls the Sultan has collected over time."
            f"\nThis is how the Sultan can form his most accurate predictions!"
            f"\nAs the Sultan obtains more user scrolls, his power of foresight will grow stronger. "
        )
        df = load_csv()

        # This is called, only assuming the program can't find the CSV.
        if df is not None and not df.empty:
            df.columns = [col.strip().lower() if isinstance(col, str) else col for col in df.columns]

            try:
                st.dataframe(df[["genre", "hours", "console"]])
            except KeyError:
                st.warning("Sorry, the Sultan can't find the right scroll!")
                st.write("Available scrolls:", df.columns.tolist())

    except Exception as e:
        st.error(" OH DEAR! Sultan has lost a scroll!")
        st.exception(e)



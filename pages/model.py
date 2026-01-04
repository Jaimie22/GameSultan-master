#Author - Jaimie Neilson
#Student no. - B01831071
#Project - GameSultan Predictor
#Version - 1.0
# Date - 02/11/2025
# 1.1 Update - 06/12/25

#Foundational elements of the ML model.
import pandas as pd
import numpy as np
from pages.Functions import load_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier


df = load_csv()
if df is None or df.empty:
    raise ValueError("That scroll appears to be missing!.. ")

# Matching the UI names of the consoles.
df["console"] = df["console"].str.strip().str.lower()

#The means to convert the average range of numbers into tangible results.
#For example, if it was between 0-3 hours, this would find the average between.
def convert_range(value):
    if isinstance(value, str) and '_' in value:
        try:
            low, high = value.split('_')
            return (float(low) + float(high)) / 2
        except ValueError:
            return np.nan

    try:
        return float(value)
    except ValueError:
        return np.nan

#Applying numerical columns to the targets.
for col in ["age", "hours"]:
    df[col] = df[col].apply(convert_range)

#Fills the NaNs if a conversion fails.
df[["age", "hours"]] = df[["age", "hours"]].fillna(0)

#This is where the ML model looks at the varied names of the columns
label_encoders = {}
for col in ["genre", "console"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

#This is where the model target the specifically chosen columns
x = df[["age", "hours", "console"]]
y = df["genre"]

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

def predict_genre(console_input, age_input=None, hours_input=None):

    if not console_input:
        raise ValueError("The Scrolls cannot be empty!")

    console_input = console_input.strip().lower()
    classes = label_encoders["console"].classes_
    classes_lower = [c.lower() for c in classes]

    if console_input not in classes_lower:
        raise ValueError(f"Device not found: {console_input}")

    console_encoded = label_encoders["console"].transform([classes[classes_lower.index(console_input)]])[0]

    if age_input is None:
        age_input = int(df["age"].mean())
    if hours_input is None:
        hours_input = int(df["hours"].mode()[0])

    features = [[age_input, hours_input, console_encoded]]

    pred = model.predict(features)[0]
    return label_encoders["genre"].inverse_transform([pred])[0]

def predict_genre_confidence(console_input, age_input=None, hours_input=None):

    if age_input is None:
        age_input = int(df["age"].mean())
    if hours_input is None:
        hours_input = int(df["hours"].mode()[0])

    console_input = console_input.strip().lower()
    classes = label_encoders["console"].classes_
    classes_lower = [c.lower() for c in classes]

    console_encoded = label_encoders["console"].transform([classes[classes_lower.index(console_input)]])[0]
    features = [[age_input, hours_input, console_encoded]]

    probabilities = model.predict_proba(features)[0]
    idx = np.argmax(probabilities)

    genre = label_encoders["genre"].inverse_transform([idx])[0]
    confidence = probabilities[idx]

    return genre, confidence, probabilities
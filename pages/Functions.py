#Author - Jaimie Neilson
#Student no. - B01831071
#Project - GameSultan Predictor
#Version - 1.0
# Date - 02/11/2025
# 1.1 Update - 06/12/25
# 1.2 Final Update - 06/01/26

import csv
import os
import pandas as pd
from PIL import Image


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_FILE = os.path.join(BASE_DIR, "csv_dataset", "UserDataNew.csv")
IMAGE_FILE = os.path.join(BASE_DIR, "Images", "game_sultan_logo.png")

def get_logo():
    if not os.path.exists(IMAGE_FILE):
        return None
    return Image.open(IMAGE_FILE)

def save_user_data(user_data: dict):
    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=user_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(user_data)

def load_csv():
    if not os.path.exists(CSV_FILE):
        return None
    return pd.read_csv(CSV_FILE)

def clean_csv(file_path: str = CSV_FILE):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found at: {file_path}")

    cleaned_rows = []

    with open(file_path, newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        for row in reader:
            if any(
                val.strip().lower() == "please select.."
                for val in [
                    row.get("genre", ""),
                    row.get("hours", ""),
                    row.get("console", "")
                ]
            ):
                continue
            cleaned_rows.append(row)

    with open(file_path, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

#Author - Jaimie Neilson
#Student no. - B01831071
#Project - GameSultan Predictor
#Version - 1.0
# Date - 02/11/2025
# 1.1 Update - 06/12/25
# 1.2 Final Update - 06/01/26

import csv
import os

# Creates the CSV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(BASE_DIR, 'Dataset', 'UserDataNew.csv')

#Finds the CSV, and saves new data to it under these constraints.
def save_UserData(UserData):
    file_exists = os.path.exists(CSV)
    with open(CSV, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=UserData.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(UserData)

#Loads of the data from the existing CSV (if any), and turns it into a list of dictionaries
def load_UserData():
    if not os.path.isfile(CSV):
        return[]
    with open(CSV, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)
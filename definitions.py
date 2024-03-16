#In this file, we define the functions that we will call in main.py

# definitions.py

import openai
import pandas as pd
import json

# Assuming your OpenAI API key is stored in a file named secret_key.py
from secret_key import openai_api_key

openai.api_key = openai_api_key

# This function will fetch the patient information needed 
def get_patient_info_from_excel(name, df):
    """Fetch patient data from an Excel-based DataFrame."""
    patient_info = df[df['Name'].str.contains(name, case=False, na=False)]
    if not patient_info.empty:
        info_dict = patient_info.iloc[0].to_dict()
        return json.dumps(info_dict)
    else:
        return "Patient not found."

# This function gives reccomendation for medication to the patient. We assume that 
# for patients with a positive genetic test, we reccomend medication alpha. 
    #for those that are taking medication A / D we reccomend beta. for those older than 
    #60, we reccomend medication sigma

def determine_medication(age, current_medications, genetic_test_result):
    """
    Determines the appropriate medication based on age, current medications, 
    and genetic test result.
    
    :param age: int - The age of the patient
    :param current_medications: list - A list of the patient's current medications
    :param genetic_test_result: str - The result of the patient's genetic test
    :return: str - The recommended medication or an appropriate message
    """
    # Only recommend medication if the genetic test result is positive
    if genetic_test_result != 'Positive':
        return "No medication recommendation due to genetic test result not being positive."

    problem_medications = ['Medication A', 'Medication D']
    age_threshold = 60
    recommended_medication = 'Medication ALPHA' if age <= age_threshold else 'Medication SIGMA'
    
    if any(med in current_medications for med in problem_medications):
        recommended_medication = 'Medication BETA'
    
    return recommended_medication

# This definition will help fetch patient summary when asked by user
def fetch_summary(prompt):
    """Fetches a summary from OpenAI based on the provided prompt."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred while fetching the patient summary: {e}"

#This functin helps the AI give a reccomendation on which lifestyle choices to change/lead given a positive genetic test result 
def fetch_recommendations(prompt):
    """Fetches lifestyle recommendations from OpenAI based on the provided prompt."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred while fetching lifestyle recommendations: {e}"

# The AI will perform the medication analusis as specified by the deterine medication function! 
def perform_medication_analysis(prompt):
    """Performs medication analysis using OpenAI based on the provided prompt."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred while performing medication analysis: {e}"

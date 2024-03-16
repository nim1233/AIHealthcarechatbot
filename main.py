# main.py

import pandas as pd
from definitions import (
    get_patient_info_from_excel,
    determine_medication,
    fetch_summary,
    fetch_recommendations,
    perform_medication_analysis,
)
import json
import openai

# make sure you have a file called secret_key where you store your API key for this to execute properly 
from secret_key import openai_api_key

# Set your OpenAI API key
openai.api_key = openai_api_key

def main():
    # Load the DataFrame from 'random_data.xlsx'
    df = pd.read_excel('random_data.xlsx')

    # Ask for the patient's name
    user_input = input("What is the patient's name? ")

    # Fetch patient info from Excel
    function_response = get_patient_info_from_excel(user_input, df)

    if function_response != "Patient not found.":
        patient_info_dict = json.loads(function_response)

        # Fetch and display patient summary
        summary_prompt = f"Summarize this patient's information: {json.dumps(patient_info_dict, indent=2)}"
        patient_summary = fetch_summary(summary_prompt)
        print("\nPatient Summary:\n", patient_summary)

        # Fetch and display lifestyle recommendations
        recommendations_prompt = """
        Given the patient's details, provide recommendations for lifestyle changes, preventative measures.
        """
        lifestyle_recommendations = fetch_recommendations(recommendations_prompt)
        print("\nLifestyle Recommendations:\n", lifestyle_recommendations)
        
        # Ensure we have a genetic test result and it's positive before proceeding with medication analysis
        if patient_info_dict.get('Genetic Test Result') == 'Positive':
            # Ask the user if they want medication analysis
            user_decision = input("\nWould you like to analyze medication compatibility? (yes/no): ").strip().lower()

            if user_decision == 'yes':
                patient_age = patient_info_dict['Age']
                patient_medications = patient_info_dict.get('Medications', '').split(', ')
                recommended_medication = determine_medication(patient_age, patient_medications, patient_info_dict.get('Genetic Test Result'))
                
                medication_analysis_prompt = f"""
                Based on the patient's age, current medications, and genetic test result being positive, our initial analysis recommends {recommended_medication}. Please provide any additional insights or concerns regarding this medication choice.
                """
                medication_analysis = perform_medication_analysis(medication_analysis_prompt)
                print("\nMedication Analysis:\n", medication_analysis)

            elif user_decision == 'no':
                print("\nNo medication analysis requested.")

            else:
                print("\nInvalid response. Please answer 'yes' or 'no'.")

        else:
            print("\nThis patient does not have a positive genetic test result. No medication analysis necessary.")

    else:
        print("\nPatient not found.")

if __name__ == "__main__":
    main()

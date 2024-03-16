# This file generates a random patient dataset that generates 10 names, 10 ages, Genetic test results and medications being currently taken into excel. These are generated randomly and any 
#similarity to a real person is purely coincedental. 

from faker import Faker
import random
import pandas as pd
import os

# Create a Faker object
faker = Faker()

# Generate 100 random names
random_names = [faker.name() for _ in range(10)]

# Generate 100 random ages between 18 and 80
random_ages = [random.randint(18, 80) for _ in range(10)]

# Generate random genders ('Male' or 'Female')
random_genders = [random.choice(['Male', 'Female']) for _ in range(10)]

# Generate random genetic test results (e.g., 'Positive' or 'Negative')
genetic_test_results = [random.choice(['Positive', 'Negative']) for _ in range(10)]

# Generate random interpretations of the genetic test results
genetic_test_interpretations = ['Increased risk of disease' if result == 'Positive' else 'Normal' for result in genetic_test_results]

# Generate random medications lists
# Example medication list

medications_list = ['Medication A', 'Medication B', 'Medication C', 'Medication D', 'Medication E']

def generate_medications():
    # Randomly choose how many medications to assign (up to 3 in this example)
    num_medications = random.randint(1, 3)
    # Randomly select medications and join them into a string
    return ', '.join(random.sample(medications_list, num_medications))

# Generate random medications for each patient
random_medications = [generate_medications() for _ in range(10)]

# Create a DataFrame with the generated data and specify data types
data = {
    'Name': random_names,
    'Age': random_ages,
    'Gender': random_genders,
    'Genetic Test Result': genetic_test_results,
    'Interpretation': genetic_test_interpretations,
    'Medications': random_medications  # Add the medications column
}

dtype = {
    'Name': 'str',
    'Age': 'int',
    'Gender': 'str',
    'Genetic Test Result': 'str',
    'Interpretation': 'str',
    'Medications': 'str'  # Specify the data type for the medications column
}

df = pd.DataFrame(data)
df = df.astype(dtype)

# Get the current directory path where the Python script is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the file path for saving the Excel file in the same directory
file_path = os.path.join(current_directory, 'random_data.xlsx')

# Write the DataFrame to an Excel file
df.to_excel(file_path, index=False)

print(f'Excel file "{file_path}" has been created successfully.')

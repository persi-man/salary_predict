import streamlit as st
import pandas as pd
from joblib import load
import json

# Chargement du modèle et du préprocesseur
with open('model/version.json', 'r') as f:
    version_info = json.load(f)
    version = version_info['version']

model = load(f'model/salary_prediction_model_v{version:.1f}.joblib')
preprocessor = load(f'model/preprocessor_v{version:.1f}.joblib')

# Chargement du CSV pour obtenir les options uniques
df = pd.read_csv('data/it_jobs_data.csv')

st.title('Prédiction de salaire en informatique')
st.write(f"Utilisation du modèle version {version:.1f}")

# Collecte des entrées utilisateur
work_year = st.number_input('Année de travail', min_value=2020, max_value=2030, value=2024)
experience_level = st.selectbox('Niveau d\'expérience', sorted(df['experience_level'].unique()))
employment_type = st.selectbox('Type d\'emploi', sorted(df['employment_type'].unique()))
job_title = st.selectbox('Titre du poste', sorted(df['job_title'].unique()))
employee_residence = st.selectbox('Pays de résidence de l\'employé', sorted(df['employee_residence'].unique()))
work_setting = st.selectbox('Cadre de travail', sorted(df['work_setting'].unique()))
company_location = st.selectbox('Pays de l\'entreprise', sorted(df['company_location'].unique()))
company_size = st.selectbox('Taille de l\'entreprise', sorted(df['company_size'].unique()))
job_category = st.selectbox('Catégorie du poste', sorted(df['job_category'].unique()))

# Création d'un DataFrame avec les entrées utilisateur
input_data = pd.DataFrame({
    'work_year': [work_year],
    'experience_level': [experience_level],
    'employment_type': [employment_type],
    'job_title': [job_title],
    'employee_residence': [employee_residence],
    'work_setting': [work_setting],
    'company_location': [company_location],
    'company_size': [company_size],
    'job_category': [job_category]
})

# Prétraitement des données d'entrée
input_preprocessed = preprocessor.transform(input_data)

# Prédiction
if st.button('Prédire le salaire'):
    prediction = model.predict(input_preprocessed)
    st.success(f'Le salaire prédit est de ${prediction[0]:,.2f} USD par an')

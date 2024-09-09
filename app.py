import streamlit as st
import pandas as pd
import numpy as np
from joblib import load, dump
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import os
import glob
from others_models import get_response

def get_available_versions():
    model_files = glob.glob('model/salary_prediction_model_v*.joblib')
    versions = [float(f.split('_v')[1].split('.joblib')[0]) for f in model_files]
    return sorted(versions, reverse=True)

def train_model():
    df = pd.read_csv('data/it_jobs_data.csv')

    X = df[['work_year', 'experience_level', 'employment_type', 'job_title', 'employee_residence', 'work_setting', 'company_location', 'company_size', 'job_category']]
    y = df['salary_in_usd']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    categorical_features = ['experience_level', 'employment_type', 'job_title', 'employee_residence', 'work_setting', 'company_location', 'company_size', 'job_category']
    numeric_features = ['work_year']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    X_train_preprocessed = preprocessor.fit_transform(X_train)
    X_test_preprocessed = preprocessor.transform(X_test)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_preprocessed, y_train)

    y_pred = model.predict(X_test_preprocessed)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    if not os.path.exists('model'):
        os.makedirs('model')

    existing_versions = [float(f.split('_v')[1].split('.joblib')[0]) for f in glob.glob('model/salary_prediction_model_v*.joblib')]
    new_version = max(existing_versions) + 0.1 if existing_versions else 1.0

    dump(model, f'model/salary_prediction_model_v{new_version:.1f}.joblib')
    dump(preprocessor, f'model/preprocessor_v{new_version:.1f}.joblib')

    return new_version, rmse, r2

# Chargement du CSV pour obtenir les options uniques
df = pd.read_csv('data/it_jobs_data.csv')

st.title('Prédiction de salaire en informatique')

# Création des onglets
tab1, tab2, tab3 = st.tabs(["Prédiction", "Entraînement du modèle", "Utiliser un modèle classique"])

with tab1:
    # Sélection de la version du modèle
    available_versions = get_available_versions()
    if not available_versions:
        st.warning("Aucun modèle trouvé. Veuillez entraîner un modèle dans l'onglet 'Entraînement du modèle'.")
    else:
        selected_version = st.selectbox('Choisissez la version du modèle à utiliser:', available_versions)

        if selected_version is not None:
            # Chargement du modèle et du préprocesseur sélectionnés
            model = load(f'model/salary_prediction_model_v{selected_version:.1f}.joblib')
            preprocessor = load(f'model/preprocessor_v{selected_version:.1f}.joblib')

            st.write(f"Utilisation du modèle version {selected_version:.1f}")

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
        else:
            st.warning("Veuillez sélectionner une version du modèle.")

with tab2:
    st.header("Entraînement d'un nouveau modèle")
    if st.button("Entraîner un nouveau modèle"):
        with st.spinner("Entraînement du modèle en cours..."):
            new_version, rmse, r2 = train_model()
        st.success(f"Nouveau modèle (version {new_version:.1f}) entraîné avec succès!")
        st.write(f"RMSE: ${rmse:.2f}")
        st.write(f"R2 Score: {r2:.4f}")

with tab3:
    st.header("Utilisation d'autres modèles")
    model_selection = st.selectbox('Sélectionnez un modèle:', ['ChatGPT', 'LLaMA', 'Claude'])
    user_input = st.text_input('Entrez votre question ou votre texte ici:')
    if st.button('Envoyer'):
        if user_input:
            response = get_response(model_selection, user_input)
            #st.write(response)
            st.subheader(f"Réponse de {model_selection}:")
            st.markdown(f"**Question:** {user_input}")
            st.markdown(f"**Réponse:** {response}")
        else:
            st.warning("Veuillez entrer une question")
    else:
        st.info("Veuillez sélectionner un modèle et poser une question pour obtenir une réponse.")
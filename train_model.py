import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from joblib import dump
import os
import json

# Chargement des données
df = pd.read_csv('data/it_jobs_data.csv')

# Préparation des données
X = df[['work_year', 'experience_level', 'employment_type', 'job_title', 'employee_residence', 'work_setting', 'company_location', 'company_size', 'job_category']]
y = df['salary_in_usd']

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Prétraitement des données
categorical_features = ['experience_level', 'employment_type', 'job_title', 'employee_residence', 'work_setting', 'company_location', 'company_size', 'job_category']
numeric_features = ['work_year']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

X_train_preprocessed = preprocessor.fit_transform(X_train)
X_test_preprocessed = preprocessor.transform(X_test)

# Création et entraînement du modèle
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_preprocessed, y_train)

# Évaluation du modèle
y_pred = model.predict(X_test_preprocessed)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: ${rmse:.2f}")
print(f"R2 Score: {r2:.2f}")

# Sauvegarde du modèle et du préprocesseur
if not os.path.exists('model'):
    os.makedirs('model')

version = 1.0
with open('model/version.json', 'w') as f:
    json.dump({'version': version}, f)

dump(model, f'model/salary_prediction_model_v{version:.1f}.joblib')
dump(preprocessor, f'model/preprocessor_v{version:.1f}.joblib')

print(f"Le modèle et le préprocesseur version {version:.1f} ont été sauvegardés dans le dossier 'model'.")

# Installation des dépendances
pip install -r requirements.txt

# Entraînement du modèle
python train_model.py

# Lancement de l'application Streamlit
streamlit run app.py --server.runOnSave true

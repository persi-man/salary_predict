# Création d'un environment virtuel
python3 -m venv venv

# Activation de l'environnement virtuel
source venv/bin/activate

# Installation des dépendances
pip install -r requirements.txt

# Entraînement du modèle
python3 train_model.py

# Lancement de l'application Streamlit
streamlit run app.py --server.runOnSave true

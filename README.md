# Salary Predict
***
Ce projet a pour but de prédire le salaire d'un employé en fonction de plusieurs critères.
***
## Owner

### Persi MANKITA

***

## Pre-requirements

Assure-vous que python soit bien installé sur votre machine:
```bash
python3 --version
```
Le cas échéant, l'installer:
```bash
# Linux 
sudo apt update && sudo apt install python3
```
Pour MacOS et Windows, le téléchargement se fait directement sur le site officiel de [Python](https://www.python.org/downloads/)


***
## Lancement de l'application
Pour lancer l'application, il suffit de lancer le fichier `app.py` avec la commande suivante:
```bash
# Windows
./run-windows.sh
```
```bash
# Linux et MacOS
./run-linux.sh
```
Cette commande va installer les dépendances nécessaires et lancer l'application.

Si les dépendances sont déjà installées, vous pouvez lancer l'application avec la commande suivante: 
```bash
streamlit run app.py
```

### Désactivation de l'envireonnement

Pour désactiver l'environnement virtuel créé, taper dans le terminal la commande:
```bash
deactivate
```
***
## Vous souhaitez utiliser d'autres modèles LLM

Si vous souhaitez utiliser d'autres LLM dans votre application( disponible dans l'onglet "Utiliser un modèle classique"), il vous suffit de créer un fichier ".env" en s'inspirant de [.env-example](.env-example) avec vos propres clé API des différentes plateformes.

Touvez ou créez vos clés api sur:
- ChatGPT : [OPENAI Console](https://platform.openai.com/)
    - [Guide API](https://help.openai.com/en/collections/3675931-api) 
- Claude : [ANTROPIC Console](https://console.anthropic.com/)
    - [Guide API](https://www.anthropic.com/api)
- Llama : [META Llama Plateform](llama.com)
    - [Documentation](https://www.llama.com/docs/overview/)

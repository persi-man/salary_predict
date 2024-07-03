import threading
import requests
from bs4 import BeautifulSoup
import pandas as pd
from queue import Queue
import time
import re

# Liste des sites à scraper
sites = [
    'https://www.linkedin.com/jobs/search/',
    'https://www.indeed.com/jobs',
    'https://www.glassdoor.com/Job/index.htm'
]

result_queue = Queue()


def extract_annual_salary(salary_text):
    # Fonction pour extraire et annualiser le salaire
    salary = re.findall(r'\d+[,\d]*', salary_text)
    if salary:
        salary = float(salary[0].replace(',', ''))
        if 'per hour' in salary_text.lower():
            return salary * 40 * 52
        elif 'per month' in salary_text.lower():
            return salary * 12
        else:
            return salary
    return None


def scrape_site(url):
    try:
        print(f"Scraping {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        jobs = []
        if 'linkedin.com' in url:
            job_cards = soup.find_all('div', class_='base-card')
            for card in job_cards:
                try:
                    title = card.find('h3', class_='base-search-card__title').text.strip()
                    company = card.find('h4', class_='base-search-card__subtitle').text.strip()
                    location = card.find('span', class_='job-search-card__location').text.strip()
                    salary = card.find('span', class_='job-search-card__salary-info')
                    salary = extract_annual_salary(salary.text.strip()) if salary else None
                    experience = "N/A"
                    degree = "N/A"
                    jobs.append({'Title': title, 'Company': company, 'Location': location, 'Salary': salary,
                                 'Experience': experience, 'Degree': degree, 'Source': 'LinkedIn'})
                except AttributeError as e:
                    print(f"Erreur lors de l'extraction d'une offre LinkedIn: {e}")

        elif 'indeed.com' in url:
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            for card in job_cards:
                try:
                    title = card.find('h2', class_='jobTitle').text.strip()
                    company = card.find('span', class_='companyName').text.strip()
                    location = card.find('div', class_='companyLocation').text.strip()
                    salary = card.find('div', class_='salary-snippet')
                    salary = extract_annual_salary(salary.text.strip()) if salary else None
                    experience = card.find('div', class_='experienceRemaining')
                    experience = experience.text.strip() if experience else "N/A"
                    degree = "N/A"
                    jobs.append({'Title': title, 'Company': company, 'Location': location, 'Salary': salary,
                                 'Experience': experience, 'Degree': degree, 'Source': 'Indeed'})
                except AttributeError as e:
                    print(f"Erreur lors de l'extraction d'une offre Indeed: {e}")

        elif 'glassdoor.com' in url:
            job_cards = soup.find_all('li', class_='react-job-listing')
            for card in job_cards:
                try:
                    title = card.find('a', class_='jobLink').text.strip()
                    company = card.find('div', class_='employer-name').text.strip()
                    location = card.find('span', class_='loc').text.strip()
                    salary = card.find('span', class_='salary-estimate')
                    salary = extract_annual_salary(salary.text.strip()) if salary else None
                    experience = "N/A"
                    degree = "N/A"
                    jobs.append({'Title': title, 'Company': company, 'Location': location, 'Salary': salary,
                                 'Experience': experience, 'Degree': degree, 'Source': 'Glassdoor'})
                except AttributeError as e:
                    print(f"Erreur lors de l'extraction d'une offre Glassdoor: {e}")

        result_queue.put(jobs)
        print(f"Nombre total d'offres récupérées de {url}: {len(jobs)}")
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")


# Créer et démarrer les threads
threads = []
for site in sites:
    thread = threading.Thread(target=scrape_site, args=(site,))
    threads.append(thread)
    thread.start()
    time.sleep(2)  # Pause de 2 secondes entre chaque démarrage de thread

# Attendre que tous les threads soient terminés
for thread in threads:
    thread.join()

# Récupérer tous les résultats de la file d'attente
all_jobs = []
while not result_queue.empty():
    all_jobs.extend(result_queue.get())

# Créer un DataFrame avec tous les jobs
df = pd.DataFrame(all_jobs)

# Vérifier si le DataFrame est vide
if df.empty:
    print("Aucune donnée n'a été récupérée. Vérifiez les sélecteurs HTML et les URLs.")
else:
    # Afficher les colonnes existantes
    print("Colonnes existantes:", df.columns.tolist())

    # Nettoyer et formater les données si nécessaire
    if 'Title' in df.columns:
        df['Title'] = df['Title'].str.lower()
        df['Title'] = df['Title'].replace({
            'software engineer': 'Software Engineer',
            'data scientist': 'Data Scientist',
            'ai engineer': 'AI Engineer',
            'cybersecurity analyst': 'Cybersecurity Analyst',
            'database administrator': 'Database Administrator',
            'devops engineer': 'DevOps Engineer'
        })

    # Convertir le salaire en numérique
    if 'Salary' in df.columns:
        df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')

    # Sauvegarder les données dans un fichier CSV
    df.to_csv('data/it_jobs_data.csv', index=False)

    print(f"Scraping terminé. {len(df)} offres d'emploi ont été récupérées et sauvegardées dans 'it_jobs_data.csv'.")

# Afficher les premières lignes du DataFrame pour vérification
print(df.head())

import requests
from bs4 import BeautifulSoup
import csv

url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
page = requests.get(url)
if page.ok:
    soup = BeautifulSoup(page.content, 'html.parser')
    # Créer un nouveau fichier pour écrire dans le fichier appelé « data.csv »
    # Créer une liste pour les en-têtes
    with open('Metro_Quentin_2_data_032023.csv', 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        en_tete = ["categorie", "valeur"]
        writer.writerow(en_tete)
        ligne_url = ["URL Produit", url]
        writer.writerow(ligne_url)
        # Récupération du titre d'un produit
        titre = ["titre", soup.find(class_="active").string]
        writer.writerow(titre)

        # recuperation imageURL
        images = soup.find_all('img')
        for image in images:
            ligne_image = ["image", image['src']]
            writer.writerow(ligne_image)

        # recuperation desc
        desc = ["Description", soup.find('p', class_='').string]
        writer.writerow(desc)
        # Recuperation UPC,prices, availability, type, score
        tableau = soup.find_all('tr')
        for ligne in tableau:
            if ligne.find('th').string != "Tax":
                ligne_valeur = [ligne.find('th').string, ligne.find('td').string]
                writer.writerow(ligne_valeur)

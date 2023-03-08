import requests
from bs4 import BeautifulSoup
import csv

# Récupérer la page d'un produit et la 'parser'
url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
page = requests.get(url)
if page.ok:
    soup = BeautifulSoup(page.content, 'html.parser')

    # Organisation du CSV
    with open('Metro_Quentin_2_data_032023.csv', 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        en_tete = []
        data_livre = []

        # Récupération du titre d'un produit
        en_tete.append("Titre")
        titre = soup.find(class_="active")
        data_livre.append(titre.string)

        # Récupération url
        en_tete.append("URL")
        data_livre.append(url)

        # recuperation imageURL
        en_tete.append("Image")
        images = soup.find_all('img')
        for image in images:
            data_livre.append(image['src'])

        # recuperation desc
        en_tete.append("Product Description")
        desc = soup.find('p', class_='')
        data_livre.append(desc.string)

        # Recuperation UPC,prices, availability, type, score
        tableau = soup.find_all('tr')
        for ligne in tableau:
            if ligne.find('th').string != "Tax":
                en_tete.append(ligne.find('th').string)
                data_livre.append(ligne.find('td').string)

        writer.writerow(en_tete)
        writer.writerow(data_livre)

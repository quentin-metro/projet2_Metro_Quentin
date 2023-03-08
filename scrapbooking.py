import requests
from bs4 import BeautifulSoup
import csv

# Récupérer la page d'un produit et la 'parser'
url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
page = requests.get(url)
if page.ok:
    soup = BeautifulSoup(page.content, 'html.parser')

    # Organisation du CSV
    with open('Metro_Quentin_2_data_032023.csv', 'w', newline='') as fichier_csv:
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

        # Recuperation reviews_rating
        en_tete.append("Rating")
        if soup.find_all('p', class_="star-rating Zero"):
            rating = "0/5"
        elif soup.find_all('p', class_="star-rating One"):
            rating = "1/5"
        elif soup.find_all('p', class_="star-rating Two"):
            rating = "2/5"
        elif soup.find_all('p', class_="star-rating Three"):
            rating = "3/5"
        elif soup.find_all('p', class_="star-rating Four"):
            rating = "4/5"
        elif soup.find_all('p', class_="star-rating Five"):
            rating = "5/5"
        data_livre.append(rating)

        # recuperation type du livre
        lignes = soup.find_all('li')
        en_tete.append("category")
        skip_inutile = 0
        for ligne in lignes:
            if skip_inutile == 2:
                data_livre.append(ligne.find('a').string)
                break
            skip_inutile +=  1

        # recuperation desc
        en_tete.append("Product Description")
        desc = soup.find('p', class_='')
        data_livre.append(desc.string)

        # Recuperation UPC,prices, availability, type, score
        ligne_exclu = ["Product Type", "Tax", "Number of reviews"]
        tableau = soup.find_all('tr')
        for ligne in tableau:
            ligne_categorie = ligne.find('th').string
            if ligne_categorie not in ligne_exclu:
                en_tete.append(ligne_categorie)
                data_livre.append(ligne.find('td').string)

        writer.writerow(en_tete)
        writer.writerow(data_livre)

import requests
from bs4 import BeautifulSoup
import csv


def scrap_product_page(url_product):
    # Récupérer la page d'un produit et la 'parser'
    page_product = requests.get(url_product)
    soup_product = BeautifulSoup(page_product.content, 'html.parser')

    data_livre = []
    # Récupération du titre d'un produit
    titre = soup_product.find(class_="active")
    data_livre.append(titre.string)

    # Récupération url
    data_livre.append(url_product)

    # recuperation imageURL
    image = soup_product.find('img')
    data_livre.append(image['src'])

    # Recuperation reviews_rating
    rating = "inconnu"
    if soup_product.find_all('p', class_="star-rating Zero"):
        rating = "0/5"
    elif soup_product.find_all('p', class_="star-rating One"):
        rating = "1/5"
    elif soup_product.find_all('p', class_="star-rating Two"):
        rating = "2/5"
    elif soup_product.find_all('p', class_="star-rating Three"):
        rating = "3/5"
    elif soup_product.find_all('p', class_="star-rating Four"):
        rating = "4/5"
    elif soup_product.find_all('p', class_="star-rating Five"):
        rating = "5/5"
    data_livre.append(rating)

    # recuperation type du livre
    lignes = soup_product.find_all('li')
    skip_inutile = 0
    for ligne in lignes:
        if skip_inutile == 2:
            data_livre.append(ligne.find('a').string)
            break
        skip_inutile += 1

    # recuperation desc
    desc = soup_product.find('p', class_='')
    data_livre.append(desc.string)

    # Recuperation UPC,prices, availability, type, score
    ligne_exclu = ["Product Type", "Tax", "Number of reviews"]
    tableau = soup_product.find_all('tr')
    for ligne in tableau:
        ligne_categorie = ligne.find('th').string
        if ligne_categorie not in ligne_exclu:
            data_livre.append(ligne.find('td').string)

    # Ecris les données recuperées pour 1 livre
    writer.writerow(data_livre)


url_category = 'http://books.toscrape.com/catalogue/category/books/romance_8/index.html'
page_category = requests.get(url_category)

with open('Metro_Quentin_2_data_032023.csv', 'w', newline='') as fichier_csv:
    # Config CSV
    writer = csv.writer(fichier_csv, delimiter=',')
    en_tete = ['Titre', 'URL', 'Image', 'Rating', 'Category', 'Product_Description', 'UPC', 'Price(excl. tax)',
               'Price(incl. tax)', 'Availability']
    writer.writerow(en_tete)

    has_next = True
    while has_next:
        has_next = False

        # Récupérer la page d'une categorie et la 'parser'
        page_category = requests.get(url_category)
        soup_category = BeautifulSoup(page_category.content,'html.parser')

        # Parcours les items possible
        books = soup_category.find_all(class_="product_pod")
        for book in books:
            new_url_product = book.find('h3').find('a').get('href')
            new_url_product = url_category[:36] + new_url_product[9:]
            scrap_product_page(new_url_product)

        # changement de page
        if soup_category.find(class_="next"):
            next_page = soup_category.find(class_="next")
            new_url_partiel = next_page.find('a').get('href')
            url_category = url_category[:url_category.rfind("/")]
            url_category = url_category + '/' + new_url_partiel
            has_next = True

import requests
from bs4 import BeautifulSoup
import csv
import os


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
    image_ligne = soup_product.find('img')
    image_url = url_product[:26] + image_ligne['src'][6:]
    data_livre.append(image_url)
    keep_characters = (' ', '.', '_')
    titre_name_compatible = "".join(c for c in titre.string if c.isalnum() or c in keep_characters).rstrip()
    # telechargement de l'image
    img_data = requests.get(image_url).content
    with open('./data_scrapped/images/' + titre_name_compatible[:50] + '.jpg', 'wb') as fichier_image:
        fichier_image.write(img_data)
    fichier_image.close()

    # Recuperation reviews_rating
    product_main = soup_product.find(class_="col-sm-6 product_main")
    if product_main.find('p', class_="star-rating Zero"):
        rating = "0/5"
    elif product_main.find('p', class_="star-rating Five"):
        rating = "5/5"
    elif product_main.find('p', class_="star-rating Four"):
        rating = "4/5"
    elif product_main.find('p', class_="star-rating Three"):
        rating = "3/5"
    elif product_main.find('p', class_="star-rating Two"):
        rating = "2/5"
    elif product_main.find('p', class_="star-rating One"):
        rating = "1/5"
    else:
        rating = "inconnu"
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
    if desc:
        data_livre.append(desc.string)
    else:
        data_livre.append('')

    # Recuperation UPC,prices, availability, type, score
    ligne_exclu = ["Product Type", "Tax", "Number of reviews"]
    tableau = soup_product.find_all('tr')
    for ligne in tableau:
        ligne_categorie = ligne.find('th').string
        if ligne_categorie not in ligne_exclu:
            if ligne_categorie == "Availability":
                number_availability = ''
                for character in ligne.find('td').string:
                    if character.isdigit():
                        number_availability = number_availability + character
                data_livre.append(number_availability)
            else:
                data_livre.append(ligne.find('td').string)

    return data_livre


def scrap_category_page(url_category):
    # Config CSV
    category_name = url_category[51:-13]
    with open('./data_scrapped/CSVs/books_' + category_name + '_032023.csv',
              'w', encoding="utf-8", newline='') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        en_tete = ['Titre', 'URL', 'Image', 'Rating', 'Category', 'Product_Description', 'UPC', 'Price(excl. tax)',
                   'Price(incl. tax)', 'Availability']
        writer.writerow(en_tete)

        # scrapper sur plusieurs pages
        has_next = True
        while has_next:
            has_next = False

            # Récupérer la page d'une categorie et la 'parser'
            page_category = requests.get(url_category)
            soup_category = BeautifulSoup(page_category.content, 'html.parser')

            # Parcours les items possible
            books = soup_category.find_all(class_="product_pod")
            for book in books:
                new_url_product = book.find('h3').find('a').get('href')
                new_url_product = url_category[:36] + new_url_product[9:]
                data_to_write = scrap_product_page(new_url_product)

                # Ecris les données recuperées pour 1 livre
                writer.writerow(data_to_write)

            # changement de page
            if soup_category.find(class_="next"):
                next_page = soup_category.find(class_="next")
                new_url_partiel = next_page.find('a').get('href')
                url_category = url_category[:url_category.rfind("/")]
                url_category = url_category + '/' + new_url_partiel
                has_next = True

    fichier_csv.close()


def make_a_dir(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        pass


url_home = 'http://books.toscrape.com/index.html'
# Création des dossiers pour récupérer les data/images
make_a_dir('./data_scrapped/')
make_a_dir('./data_scrapped/CSVs/')
make_a_dir('./data_scrapped/images/')

# Récupérer la page d'une categorie et la 'parser'
page_home = requests.get(url_home)
soup_home = BeautifulSoup(page_home.content, 'html.parser')
categories = soup_home.find(class_='side_categories').find('ul').find('ul').find_all('a')
for categorie in categories:
    new_categorie_url = categorie.get('href')
    url_category_toscrap = url_home[:26] + new_categorie_url
    scrap_category_page(url_category_toscrap)

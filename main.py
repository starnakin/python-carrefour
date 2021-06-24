from bs4 import BeautifulSoup
import urllib.request
from fold_to_ascii import fold
import json

def get_all_categories():
    html_content = urllib.request.urlopen("https://www.carrefour.fr/").read()
    soup = BeautifulSoup(html_content, 'html.parser')
    categories = soup.find_all("li", {"class": "nav-item"})
    e={"mode-et-bagagerie":"__remove__","maison-et-decoration":"__remove__","commandes-traiteur": "__remove__", "services":"__remove__", "informatique-et-bureau":"informatique-bureau","smartphones-et-objets-connectes":"smartphones-objets-connectes","jeux-videos-et-culture":"jeux-videos-culture","jouets,-sports-et-loisirs": "jouets-sports-loisirs","jardin,-bricolage-et-auto-moto": "__remove__", "promotions": "__remove__", "deal-de-la-semaine": "__remove__", "vive-l'ete": "__remove__", "en-ce-moment-:-le-jardin": "__remove__", "produits-du-monde-et-de-nos-regions": "__remove__", "regimes-alimentaires": "__remove__", "commandes-traiteur": "__remove__", "services":"__remove__", "nos-commercants-partenaires": "vendeurs-partenaires-carrefour"}
    categories_edited=[]
    for category in categories:
        category = fold(category.text.replace("\n", "").replace(" ", "-").lower())
        if category in e.keys():
            if e.get(category) == "__remove__":
                pass
            else:
                categories_edited.append(e.get(category))
        else:
            categories_edited.append(category)

    rayons={}

    for category in categories_edited:

        print(category)
        url="https://www.carrefour.fr/r/"+category
        html_content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html_content, 'html.parser')

        last_page=int(soup.find('div', {"class": "product-list-header__bottom"}).find("span").text.replace("\n", "").replace(" ", "").replace("résultats", ""))//60

        rayon=[]

        for page in range(1, last_page):
            url="https://www.carrefour.fr/r/"+category+"?page="+str(page)
            html_content = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html_content, 'html.parser')
            products=soup.find_all("a", {"class":"product-card-title product-card-title__reduced-line-clamp"})
            for product in products:
                rayon.append(product.text.replace("\n", ""))
        rayons.update({category: rayon})
    return rayons

def rayons_to_json(rayons):
    json.dump(rayons, open("./carrefour.json", "w"), indent=4)

def get_category_by_product_name(product_name):
    html_content = urllib.request.urlopen("https://www.carrefour.fr/s?q="+product_name).read()
    soup = BeautifulSoup(html_content, 'html.parser')

    product_url="https://www.carrefour.fr"+soup.find_all("a", {"class":"product-card-image"})[0]["href"]

    html_content = urllib.request.urlopen(product_url).read()
    soup = BeautifulSoup(html_content, 'html.parser')

    rayon=soup.find_all("li", {"class":"breadcrumb-trail__item"})[2].text

    return rayon

print(get_category_by_product_name("lait"))
from bs4 import BeautifulSoup
import urllib.request
from fold_to_ascii import fold
import json

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
        print(category)
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
        print(url)
        html_content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html_content, 'html.parser')
        products=soup.find_all("a", {"class":"product-card-title product-card-title__reduced-line-clamp"})
        for product in products:
            rayon.append(product.text.replace("\n", ""))
    rayons.update({category: rayon})
    print(rayons)
    json.dump(rayons, open("./carrefour.json", "w"), indent=4)
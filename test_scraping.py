import requests
from bs4 import BeautifulSoup

url = "https://trouverunlogement.lescrous.fr/tools/41/search"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
cards = soup.find_all("div", class_="fr-card svelte-12dfls6")

print(f"Nombre de logements trouvés : {len(cards)}")

# Afficher les titres pour vérification
for card in cards:
    title = card.find("a").text.strip()
    print("-", title)

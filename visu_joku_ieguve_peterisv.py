import requests
import csv
import json

kategoriju_atbilde = requests.get("https://api.chucknorris.io/jokes/categories")
kategorijas = kategoriju_atbilde.json()
kategorijas.append("random")

unikalie_joki = {}

for kategorija in kategorijas:
    print(f"Apstrādā kategoriju: {kategorija}")
    mekletie_joki = 0
    neveiksmju_skaits = 0

    while neveiksmju_skaits < 20:
        if kategorija == "random":
            atbilde = requests.get("https://api.chucknorris.io/jokes/random")
        else:
            atbilde = requests.get(f"https://api.chucknorris.io/jokes/random?category={kategorija}")

        joks = atbilde.json()

        if joks["id"] not in unikalie_joki:
            unikalie_joki[joks["id"]] = joks
            mekletie_joki += 1
            neveiksmju_skaits = 0
        else:
            neveiksmju_skaits += 1

    print(f" -> Atrasti {mekletie_joki} unikāli joki šai kategorijai.")

with open("visi_chuck_norris_joki.csv", "w", newline="", encoding="utf-8") as csv_fails:
    rakstitajs = csv.writer(csv_fails, delimiter=";")
    rakstitajs.writerow(["joks"])
    for joks in unikalie_joki.values():
        rakstitajs.writerow([joks])
        
print(f"\nKopā saglabāti {len(unikalie_joki)} unikāli joki.")

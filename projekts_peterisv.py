import requests

joku_saraksts = []
atstarpe = "----------------"*5+"\n"
beigas = "\n"+"----------------"*5

def main():
    print(f"{atstarpe}Laipni lūgti Čaka Norisa faktu ieguves lietotnē. (vietās kur rakstīts '[+ / -]', ievadīt '+', ja atbilde ir 'jā', vai '-', ja atbilde ir 'nē')")
    kategorija = get_category()

    while True:
        try:
            daudzums = int(input(f"{atstarpe}Cik jokus vēlies? "))
            if daudzums <= 0:
                print(f"{atstarpe}Lūdzu ievadiet skaitli, kas ir lielāks par 0.")
            else:
                break
        except:
            print(f"{atstarpe}Lūdzu ievadiet skaitli.")
    max_meginajumi = daudzums * 10
    temp_joki = []
    meginajumi = 0

    while len(temp_joki) < daudzums and meginajumi < max_meginajumi:
        if kategorija == "random":
            req_joks = requests.get("https://api.chucknorris.io/jokes/random")
        else:
            req_joks = requests.get(f"https://api.chucknorris.io/jokes/random?category={kategorija}")

        new_joks = req_joks.json()
        meginajumi += 1

        if new_joks["value"] not in joku_saraksts and new_joks["value"] not in temp_joki:
            temp_joki.append(new_joks["value"])

    if len(temp_joki) == 0:
        print(f"{atstarpe}Neizdevās atrast nevienu unikālu joku.")
    elif len(temp_joki) < daudzums:
        print(f"{atstarpe}Iespējams, ka kategorijā '{kategorija}' nav pietiekami daudz unikālu joku.")
        print(f"Izdevās atrast tikai {len(temp_joki)} no {daudzums} pieprasītajiem.")
        while True:
            izvele = input(f"{atstarpe}Vai vēlaties tos pievienot? [+ / -]: ").strip().lower()
            if izvele == "-":
                print(f"{atstarpe}Joki netika pievienoti.")
                break
            elif izvele == "+":
                with open("joku_saraksts.txt", "w", encoding="utf-8-sig") as file:
                    for joks in temp_joki:
                        joku_saraksts.append(joks)
                        file.write(f"{len(joku_saraksts)}: {joks}\n")
                break
            else:
                print(f"{atstarpe}Lūdzu ievadiet '+' vai '-'.")
    else:
        with open("joku_saraksts.txt", "w", encoding="utf-8-sig") as file:
            for joks in temp_joki:
                joku_saraksts.append(joks)
                file.write(f"{len(joku_saraksts)}: {joks}\n")

    while True:
        atkartot = input(f"{atstarpe}Vai vēlies vēl citus jokus? [+ / -]: ").strip().lower()

        if atkartot == "-":
            print(f"{atstarpe}Tika saglabāti {len(temp_joki)} joki.")
            print(f"Izbaudiet jokus :){beigas}")
            break
        elif atkartot == "+":
            get_more_joki()
        else:
            print(f"{atstarpe}Lūdzu ievadi '+' lai turpinātu vai '-' lai beigtu.")


def get_more_joki():
    try:
        kategorija = get_category()

        while True:
            try:
                pievienojums = int(input(f"{atstarpe}Cik jokus vēlies pievienot? "))
                if pievienojums > 0:
                    break
                else:
                    print(f"{atstarpe}Lūdzu ievadiet skaitli, kas ir lielāks par 0.")
            except ValueError:
                print(f"{atstarpe}Lūdzu ievadiet derīgu veselu skaitli.")

        max_meginajumi = pievienojums * 10
        temp_joki = []
        meginajumi = 0

        while len(temp_joki) < pievienojums and meginajumi < max_meginajumi:
            if kategorija == "random":
                req_joks = requests.get("https://api.chucknorris.io/jokes/random")
            else:
                req_joks = requests.get(f"https://api.chucknorris.io/jokes/random?category={kategorija}")

            new_joks = req_joks.json()
            meginajumi += 1

            if new_joks["value"] not in joku_saraksts and new_joks["value"] not in temp_joki:
                temp_joki.append(new_joks["value"])

        if len(temp_joki) == 0:
            print(f"{atstarpe}Neizdevās atrast nevienu jaunu joku.")
            return

        elif len(temp_joki) < pievienojums:
            print(f"{atstarpe}Iespējams, ka kategorijā '{kategorija}' nav pietiekami daudz unikālu joku.")
            print(f"Izdevās atrast tikai {len(temp_joki)} no {pievienojums} pieprasītajiem.")

            while True:
                izvele = input(f"Vai vēlaties tos pievienot? [+ / -]: ").strip()
                if izvele == "+":
                    break
                elif izvele == "-":
                    print(f"{atstarpe}Joki netika pievienoti.")
                    return
                else:
                    print(f"{atstarpe}Lūdzu ievadiet '+' vai '-'.{atstarpe}")

        with open("joku_saraksts.txt", "a", encoding="utf-8-sig") as file:
            for joks in temp_joki:
                joku_saraksts.append(joks)
                file.write(f"{len(joku_saraksts)}: {joks}\n")

    except:
        print(f"{atstarpe}Lūdzu ievadiet skaitli, kas ir lielāks par 0.")


def get_category():
    while True:
        try:
            req_cat = requests.get("https://api.chucknorris.io/jokes/categories")
            categories = req_cat.json()
            categories.append("random")

            jautajums = input(f"{atstarpe}Vai vēlaties redzēt kategoriju sarakstu? [+ / -]: ")

            if jautajums == "+":
                print(f"{atstarpe}Pieejamās kategorijas:")
                for i in categories:
                    print(i)

            if jautajums in ["+", "-"]:
                while True:
                    kategorija = input(f"{atstarpe}Ievadi kategoriju: ").lower()
                    if kategorija in categories:
                        return kategorija
                    else:
                        print(f"{atstarpe}Ievadīta nederīga kategorija!")
                        print(f"{atstarpe}Lūdzu ievadīt kategoriju no šī saraksta:")
                        for i in categories:
                            print(i)
            else:
                print(f"{atstarpe}Lūdzu atbildēt ar '+' vai '-' ")

        except Exception:
            print(f"{atstarpe}Radās kļūda iegūstot kategorijas. Lūdzu mēģiniet vēlreiz.")


main()

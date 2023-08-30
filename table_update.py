import json

# corrige os valores das tabelas de acordo com o fator de correção


def update_values(file, factor):
    with open(file, "r", encoding='utf8') as j:
        data = json.load(j)

    for i in data["CIRURGIAS_EQUIPE"].keys():
        data["CIRURGIAS_EQUIPE"][i]["valor"] = int(round(
            data["CIRURGIAS_EQUIPE"][i]["valor"] * factor, -1))
        print(data["CIRURGIAS_EQUIPE"][i]["valor"])

    with open(f"up_{file}", "w+", encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)


update_values("202209tabelas.json", 1.1)

def valor_anestesia_renata(nome_cirurgia, anestesia_renata, renata_cons_menos):
    nome_cirurgia.sort()
    cirurgias = ', '.join(nome_cirurgia)
    valor = anestesia_renata.get(cirurgias) or 0
    if cirurgias in renata_cons_menos:
        valor += anestesia_renata["Consulta-"]
    else:
        valor += anestesia_renata["Consulta"]
    return valor


def valor_equipe(nome_cirurgia, equipe_cirurgias, ajuste_q, tempo_lipo):
    valor = 0

    for i in nome_cirurgia:
        cirurgia = i
        if i == "Lipoaspiração":
            valor += equipe_cirurgias[cirurgia]["valor"] * tempo_lipo
        else:
            valor += equipe_cirurgias[cirurgia]["valor"]
    valor_ajustado = ajuste_func(ajuste_q, valor)
    return round(valor_ajustado, 2)


def ajuste_func(ajuste_q, valor):
    if not ajuste_q:
        ajuste_q = "0"
    if "," in ajuste_q:
        ajuste_q = ajuste_q.replace(",", ".")
    if "%" in ajuste_q:
        ajuste_q = float(ajuste_q[:-1]) / 100
        return valor * (ajuste_q + 1)
    else:
        ajuste_q = float(ajuste_q)
        return valor + ajuste_q


def valor_anestesia_foz(nome_cirurgia, tempo_lipo, anestesia_foz):
    dict_valores = {}
    for i in nome_cirurgia:
        dict_valores[i] = anestesia_foz[i]
    sorted_dict = dict(
        sorted(dict_valores.items(), key=lambda item: item[1], reverse=True)
    )
    lista_cir = list(sorted_dict.keys())
    lista_valores = list(sorted_dict.values())
    if (
        lista_cir[0] == "Lipoescultura(2,5h)"
        or lista_cir[0] == "Lipoaspiração"
        or lista_cir[0] == "Lipoescultura(3h)"
    ):
        lista_valores[0] = lista_valores[0] + (
            (lista_valores[0] / 2) * (tempo_lipo - 1)
        )
    elif "Lipoaspiração" in sorted_dict:
        sorted_dict["Lipoaspiração"] = sorted_dict["Lipoaspiração"] * tempo_lipo
        lista_valores = list(sorted_dict.values())
    elif "Lipoescultura(2,5h)" in sorted_dict:
        sorted_dict["Lipoescultura(2,5h)"] = (
            sorted_dict["Lipoescultura(2,5h)"] * tempo_lipo
        )
        lista_valores = list(sorted_dict.values())
    elif "Lipoescultura(3h)" in sorted_dict:
        sorted_dict["Lipoescultura(3h)"] = sorted_dict["Lipoescultura(3h)"] * tempo_lipo
        lista_valores = list(sorted_dict.values())
    valor = lista_valores[0]
    lista_valores.pop(0)
    for i in lista_valores:
        valor += i / 2
    return valor


def valor_hmcc(tempo, diaria, hmcc):
    return hmcc[str(tempo)][str(diaria)]


def valor_unimed(tempo, diaria, unimed):
    return unimed[str(tempo)][str(diaria)]


def valor_hmd(tempo, diaria, hmd):
    return hmd[str(tempo)][str(diaria)]


def tempo_diaria(nome_cirurgia, equipe_cirurgias, lipo_menos_1h, tempo_lipo):
    tempo = 0
    diaria = 0
    for i in nome_cirurgia:
        tempo += equipe_cirurgias[i]["tempo"]
        diaria += equipe_cirurgias[i]["diaria"]
    if tempo >= 6:
        tempo = 6
    if diaria >= 2:
        diaria = 1
    if "Lipoescultura(2,5h)" in nome_cirurgia or "Lipoescultura(3h)" in nome_cirurgia:
        if len(nome_cirurgia) == 2:
            if any(x in nome_cirurgia for x in lipo_menos_1h):
                tempo -= 1
    if "Lipoaspiração" in nome_cirurgia:
        tempo += int(tempo_lipo - 1)
    return tempo, diaria

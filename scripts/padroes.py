import re

meses_regex = re.compile(r"(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)", re.I)

palavras_proibidas = re.compile(r"\b(?:anos|reclusão|multa|salários?-mínimos|Art(?:igo)?\.?|§|fls\.?|processos?)\b", re.I)

padroes_leitura = [
    re.compile(r"Leituras\s*de\s*(\d+)\s+(?:livros|obras|obras\s+literarias)", re.I),
    re.compile(r"leu\s+(\d+)\s+(?:obras|livros)", re.I),
    re.compile(r"(\d+)\s+(?:livros|obras|obras\s+literarias)\s+(?:lidos|lidas)", re.I),
    re.compile(r"leitura\s*(?:de|:)?\s*(\d+)\s*(?:livros|obras)", re.I),
    re.compile(r"leu\s*(?:mais\s*de\s*)?(\d+)\s*(?:livros|obras)", re.I),
    re.compile(r"(\d+)\s*(?:livros|obras)\s*(?:lidos|lidas|registrados)", re.I),
    re.compile(r"obras?\s*lidas?\s*:?\s*(\d+)", re.I),
    re.compile(r"leu\s+(\d+|[a-zçáéíóú ]+)\s+(?:obras|livros)", re.I),
    re.compile(r"(\d+|[a-zçáéíóú ]+)\s+(?:livros|obras)\s+(?:lidos|lidas)", re.I),
    re.compile(r"Leituras\s*de\s*(\d+|[a-zçáéíóú ]+)\s+(?:livros|obras)", re.I)
]

padroes_trabalho = [
    re.compile(r"(\d+|[a-zçãé ]+)\s+dias\s+de\s+trabalho", re.I),
    re.compile(r"exercendo\s+trabalho\s+há\s+mais\s+de\s+(\d+|[a-zçãé ]+)", re.I),
    re.compile(r"registra\s+(\d+|[a-zçãé ]+)\s+dias\s+de\s+trabalho", re.I),
    re.compile(r"(?:" + meses_regex.pattern + r")\s*\d{4}\s*=?\s*(\d+)\s*dias", re.I)
]

padroes_estudo = [
    re.compile(r"carga\s+horária\s+de\s+(\d+)\s+horas", re.I),
    re.compile(r"carga\s+hor[aá]ria\s+(?:de\s+)?(?:total\s+de\s+)?(\d+)\s+horas", re.I),
    re.compile(r"(\d+)\s+horas\s+estudadas?", re.I),
]

padroes_pena = [
    re.compile(r"(\d+)\s*anos?(?:[,\s]*e?\s*(\d+)\s*meses?)?(?:[,\s]*e?\s*(\d+)\s*dias?)?\s*de\s*(?:prisão|detenção|reclusão|condenação)", re.I),
    re.compile(r"(?:pena(?:\s+definitiva|\s+unificada|\s+base)?|totalizada)\s*(?::|de|em)?\s*(\d+)\s*anos?(?:[,\s]*e?\s*(\d+)\s*meses?)?(?:[,\s]*e?\s*(\d+)\s*dias?)?", re.I),
    re.compile(r"([a-zçáéíóú]+)\s*anos?(?:[,\s]*e?\s*([a-zçáéíóú]+)\s*meses?)?(?:[,\s]*e?\s*([a-zçáéíóú]+)\s*dias?)?", re.I),
    re.compile(r"(?:conden\w+|fix\w+|reclusão|detenção)\s+(?:a|em|de)\s+(\d+)\s*anos?", re.I),
    re.compile(r"(\d+)\s*(?:\([^)]+\))?\s*anos?(?:[,\s]*e?\s*(\d+)\s*(?:\([^)]+\))?\s*meses?)?", re.I),
    re.compile(r"([a-zçáéíóú]+)\s*(?:\([^)]+\))?\s*anos?", re.I)
]
from deep_translator import GoogleTranslator
import re, pdfplumber, numerize

NOME_ARQUIVO = "moraes-remicao-daniel-silveira.pdf"

def extensotonum(texto):
    if not texto: return None
    group = {
        "um": 1, "dois": 2, "três": 3, "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10, 
        "onze": 11, "doze": 12, "quatorze":14, "quinze": 15, "dezesseis":16, "dezessete":17, "dezoito": 18, "dezenove":19,
        "vinte": 20, "trinta": 30, "quarenta": 40, "cinquenta": 50, "sessenta": 60, "setenta":70, "oitenta": 80, "noventa": 90,
        "cento": 100
    }
    palavras = texto.lower().replace(" e ", " ").split()
    total = sum(group.get(p, 0) for p in palavras)
    return total if total > 0 else None

meses_pt = r"(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)"

padroes_leitura = [
    re.compile(r"Leituras\s*de\s*(\d+)\s+(?:livros|obras|obras\s+literarias)", re.I),
    re.compile(r"leu\s+(\d+)\s+(?:obras|livros)", re.I),
    re.compile(r"(\d+)\s+(?:livros|obras|obras\s+literarias)\s+(?:lidos|lidas)", re.I)
]

padroes_trabalho = [
    re.compile(r"(\d+|[a-zçãé ]+)\s+dias\s+de\s+trabalho", re.I),
    re.compile(r"exercendo\s+trabalho\s+há\s+mais\s+de\s+(\d+|[a-zçãé ]+)", re.I),
    re.compile(r"registra\s+(\d+|[a-zçãé ]+)\s+dias\s+de\s+trabalho", re.I),
    re.compile(r"(?:" + meses_pt + r")\s*\d{4}\s*=?\s*(\d+)\s*dias", re.I)
]

padroes_estudo = [
    re.compile(r"(\d+)\s+horas", re.I),
    re.compile(r"carga\s+horária\s+de\s+(\d+)\s+horas", re.I),
    re.compile(r"(\d+)\s+horas\s+estudadas?", re.I)
]

texto_total = ''
try:
    with pdfplumber.open(NOME_ARQUIVO) as arquivo:
        for pagina in arquivo.pages:
            texto_total += pagina.extract_text() + '\n'
except Exception as e:
    print(f"Erro: {e}")

contagem__meses = len(re.findall(meses_pt, texto_total, re.I))
MODO_LISTA = True if contagem__meses > 3 else False

LISTA_DIAS_TRABALHADOS = []
HORAS_ESTUDO = []
OBRAS_LIDAS = 0

palavras_proibidas = ["anos", "reclusão", "multa", "salários-mínimos", "Art."]

for item in padroes_trabalho:
    for match in item.finditer(texto_total):
        contexto_trabalho = texto_total[max(0, match.start()-50) : min(len(texto_total), match.end()+50)].lower()
        if not any(proibida in contexto_trabalho for proibida in palavras_proibidas):
            valor_texto = match.group(1)
            valor = int(valor_texto) if valor_texto.isdigit() else extensotonum(valor_texto)
            if valor: LISTA_DIAS_TRABALHADOS.append(valor)

if MODO_LISTA:
    total_dias_trabalho = sum(LISTA_DIAS_TRABALHADOS)
else:
    total_dias_trabalho = max(LISTA_DIAS_TRABALHADOS) if LISTA_DIAS_TRABALHADOS else 0

for item in padroes_estudo:
    contexto_estudo = item.findall(texto_total)
    HORAS_ESTUDO.extend([int(h) for h in contexto_estudo])

total_horas_estudo = sum(set(HORAS_ESTUDO)) 

for item in padroes_leitura:
    matches = list(item.finditer(texto_total))
    if matches:
        for m in matches:
            valor_texto = m.group(1)
            valor = int(valor_texto) if valor_texto.isdigit() else extensotonum(valor_texto)
            if valor: OBRAS_LIDAS = valor
        break

remicao_trabalho = total_dias_trabalho // 3
remicao_estudo = total_horas_estudo // 12
remicao_leitura = min(OBRAS_LIDAS, 12) * 4

print(f"--- RELATÓRIO DE REMIÇÃO (ARQUIVO: {NOME_ARQUIVO}) ---")
print(f"Modo: {'Lista Mensal' if MODO_LISTA else 'Resumo de Decisão'}")
print(f"🛠️ TRABALHO: {total_dias_trabalho} dias -> {remicao_trabalho} dias remidos")
print(f"📚 ESTUDO: {total_horas_estudo} horas -> {remicao_estudo} dias remidos")
print(f"📖 LEITURA: {OBRAS_LIDAS} obras -> {remicao_leitura} dias remidos")
print(f"✅ TOTAL HOMOLOGADO: {remicao_trabalho + remicao_estudo + remicao_leitura} dias")

def remicao_trabalho(dias_trabalhados):
    return dias_trabalhados // 3


def remicao_estudo(total_horas_estudo):
    return total_horas_estudo // 12


def remicao_obras_lidas(qtd_obras_lidas):
    return min(qtd_obras_lidas, 12)*4


def calcular_remicao(remicao_t, remicao_e, remicao_l):
    return (remicao_t + remicao_e + remicao_l)


def converter_txt_num(texto):
    if not texto: return None
    group = {
        "zero":0, "um": 1, "dois": 2, "três": 3, "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10, 
        "onze": 11, "doze": 12, "treze": 13, "quatorze":14, "quinze": 15, "dezesseis":16, "dezessete":17, "dezoito": 18, "dezenove":19,
        "vinte": 20, "trinta": 30, "quarenta": 40, "cinquenta": 50, "sessenta": 60, "setenta":70, "oitenta": 80, "noventa": 90,
        "cento": 100
    }
    palavras = texto.lower().replace(" e ", " ").split()
    total = sum(group.get(p, 0) for p in palavras)
    return total if total > 0 else None


def converter_dias(total_dias):
    anos = int(total_dias//365)
    meses = int((total_dias%365)//30.4375)
    dias = int((total_dias%365)%30.4375)
    return anos, meses, dias
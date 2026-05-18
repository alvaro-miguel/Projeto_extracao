from auxiliares import converter_txt_num
from padroes import meses_regex
import re

def contabilizar(texto, padrao, palavras_proibidas):
    meses = re.findall(meses_regex, texto)
    modo_lista = len(set(meses)) > 3
    itens_encontrados = []
    evidencias = []

    for item in padrao:
        for match in item.finditer(texto):
            start = max(0, match.start()-50)
            end = min(len(texto), match.end()+50)
            contexto = texto[start:end].lower()
            if not palavras_proibidas.search(contexto):
                valor_texto = match.group(1)
                valor = int(valor_texto) if valor_texto.isdigit() else converter_txt_num(valor_texto)
                if valor:
                    itens_encontrados.append(valor)
                    evidencias.append((match.start(), match.end()))

    if not itens_encontrados:
        return 0, []
    
    if modo_lista:
        return sum(itens_encontrados), evidencias
    else:
        return max(itens_encontrados), evidencias


def obter_pena(texto, padroes):
    itens_encontrados = []
    posicoes = []

    try:
        for item in padroes:
            for match in item.finditer(texto):
                grupos = match.groups()
                grupos_completos = grupos + (None,) * (3 - len(grupos))

                anos_previa = grupos_completos[0]
                anos = int(anos_previa) if anos_previa and str(anos_previa).isdigit() else (converter_txt_num(anos_previa) or 0)

                meses_previa = grupos_completos[1]
                meses = int(meses_previa) if meses_previa and str(meses_previa).isdigit() else (converter_txt_num(meses_previa) or 0)
                
                dias_previa = grupos_completos[2]
                dias = int(dias_previa) if dias_previa and str(dias_previa).isdigit() else (converter_txt_num(dias_previa) or 0 )

                pena = (anos, meses, dias)
                if pena not in itens_encontrados:
                    itens_encontrados.append(pena)
                    posicoes.append((match.start(), match.end()))

        if itens_encontrados:
            pena_anos, pena_meses, pena_dias = max(itens_encontrados)
            pena_final = {
                "anos": pena_anos,
                "meses": pena_meses,
                "dias": pena_dias,
                "pena_dias_totais": round((pena_anos*365) + (pena_meses*30.4375) + pena_dias)
            }
            return pena_final, posicoes
        else:
            return None
    except Exception as e:
        print(f'Error: {e}')
        return None, []
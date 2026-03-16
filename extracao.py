import pdfplumber, os, pandas, re
'''a razão de usar cada biblioteca:
pdfplumber: acessar o arquivo pdf e extrair as tabelas
pandas: converter as tabelas encontradas em DataFrame(estrutura semelhante a tabela, porém melhor indicada para python)
re: usada para encontrar dados nos textos'''

def converter_lista_inteiro(lista):
    lista_inteiro = []
    for item in lista:
        lista_inteiro.append(int(item))
    return lista_inteiro


def dias_totais_pena(dados_conenado):
    anos = int(dados_conenado.get('pena_anos', 0))
    meses = int(dados_conenado.get('pena_meses', 0))
    dias = int(dados_conenado.get('pena_dias', 0))
    pena_total_dias = (anos*365) + (meses*30) + dias

    return pena_total_dias


def extrair(arquivo):
    if not os.path.exists(arquivo):
        print("Arquivo não encontrado")     
        return None, None
    
    tabelas_totais = {}

    dados_condenado = {
        'nome': '',
        'matricula_penal': '',
        'idade': 0,
        'data_nascimento': '',
        'crime_condenatorio': '',
        'pena_total': '',
        'data_ingresso': '',
        'regime_atual': '',
        'instituiacao_penal': '',
        'data_relatorio': '',
        'pena_anos': '',
        'pena_meses': '',
        'pena_dias': '',
        'pena_numero':''
        }

    texto_arquivo = ""
    
    with pdfplumber.open(arquivo) as pdf:
        for i, pagina in enumerate(pdf.pages):
            i += 1

            # -> extracao das tabelas da pagina 
            tabelas_pagina_atual = pagina.extract_tables()
            dataFrame_paginas = [] # a principio uma lista para guardar as tabelas de cada pagina caso haja mais de uma tabela no documento

            for tabela in tabelas_pagina_atual:
                nomes_corretos = ['atividade', 'periodo', 'tempo_dedicado', 'tipo_atividade']
                data_frame = pandas.DataFrame(tabela[1:], columns=nomes_corretos)
                '''converte a tabela atual em um dataframe, começando pela segunda linha(tabela[1:]), e determina que a primeira linha
                é usada para determinar o nome das colunas'''
                dataFrame_paginas.append(data_frame) #salva o dataframe na lista de tabelas
            tabelas_totais[i] = dataFrame_paginas #salva as tabelas da pagina no dicionario

            # -> extracao do texto da pagina
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_arquivo += texto_pagina + "\n"

    for linha in (texto_arquivo.splitlines()):
        linha = linha.lower()
        
        if 'nome:' in linha:
            nome = linha.split(": ")[1]
            dados_condenado['nome'] = nome

        elif 'matrícula penal:' in linha:
            matricula = linha.split(": ")[1]
            dados_condenado['matricula_penal'] = matricula

        elif 'idade:' in linha:
            idade = linha.split(": ")[1]
            dados_condenado['idade'] = idade

        elif 'data de nascimento:' in linha:
            nascimento = linha.split(": ")[1]
            dados_condenado['data_nascimento'] = nascimento

        elif 'crime condenatório:' in linha:
            crime = linha.split(": ")[1]
            dados_condenado['crime_condenatorio'] = crime

        elif 'pena total:' in linha:
            pena = linha.split(": ")[1]
            dados_condenado['pena_total'] = pena

        elif 'data de ingresso:' in linha:
            ingresso = linha.split(": ")[1]
            dados_condenado['data_ingresso'] = ingresso

        elif 'regime atual:' in linha:
            regime = linha.split(": ")[1]
            dados_condenado['regime_atual'] = regime

        elif 'instituição penal:' in linha:
            instituicao = linha.split(": ")[1]
            dados_condenado['instituiacao_penal'] = instituicao

        elif 'data deste relatório:' in linha:
            data_relatorio = linha.split(": ")[1]
            dados_condenado['data_relatorio'] = data_relatorio

    #transformando os valores da pena de string para numero para que seja possivel calcular uma possível redução penal
    pena_numeros = re.findall(r"\d+", dados_condenado['pena_total'])
    pena_numeros = converter_lista_inteiro(pena_numeros)
    dados_condenado['pena_anos'] = pena_numeros[0]
    dados_condenado['pena_meses'] = pena_numeros[1]
    dados_condenado['pena_dias'] = pena_numeros[2]

    return dados_condenado, tabelas_totais


def atividades_condenado(tabelas): #função para retornar as atividades do condenado e o tempo(dias/horas) dedicado a cada atividade
    tempo_atividades = {}
    lista_atividades = tabelas[1][0].to_dict('records') # -> com isso consigo percorrer o dataframe das atividades como se fosse uma lista

    for item in lista_atividades:
        nome = item['atividade']
        texto_bruto = str(item['tempo_dedicado']).lower()#encontro todo o texto referente a atividade
        tempo_encontrado = re.findall(r'\d+', texto_bruto)#extraio a string que contém o tempo em si

        if tempo_encontrado:
            valor_tempo = int(tempo_encontrado[0])

            if 'hora' in texto_bruto:
                unidade = 'horas'
            else:
                unidade = 'dias'

            if nome in tempo_atividades:
                tempo_atividades[nome]['tempo'] += valor_tempo
            else:
                tempo_atividades[nome] = {'tempo': valor_tempo, 'unidade': unidade}

    return tempo_atividades


def calcular_desconto_penal(atividades):
    desconto = 0

    for atividade, valor in atividades.items():
        tempo = valor['tempo']
        unidade = valor['unidade']

        if unidade == 'horas':
            desconto += (tempo//12)
        else:
            desconto += (tempo//3)

    return desconto


def formatar_pena(pena):
    anos = pena//365
    meses = (pena%365)//30
    dias = (pena%365) % 30

    return f'{anos} anos, {meses} meses e {dias} dias' 


def main():
    NOME_ARQUIVO = input('Nome do documento: ')
    dados, tabelas = extrair(NOME_ARQUIVO)

    atividades = atividades_condenado(tabelas)
    pena_original_dias = dias_totais_pena(dados)
    desconto = calcular_desconto_penal(atividades)
    nova_pena_dias = pena_original_dias - desconto
    nova_pena_formatada = formatar_pena(nova_pena_dias)

    print(f'Nova pena de {dados['nome']}: {nova_pena_formatada}')


main()

'''
#TESTE
NOME_ARQUIVO = input("Informe o nome do documento(o caminho deve estar correto): ")
dados, tabelas = extrair(NOME_ARQUIVO)
print(f'Nome condenado: {dados['nome']}')
print(f'Condenação: {dados['pena-anos']} anos, {dados['pena_meses']} meses, {dados['pena_dias']} dias')
atividades = atividades_condenado(tabelas)
pena_total_dias = dias_totais_pena(dados)
print(atividades)
print(pena_total_dias)
'''

#df_atividades.columns[0] -> dessa forma consigo determinar qual coluna quero acessar

'''
Artigo 126 da Lei de Execução Penal (LEP - Lei nº 7.210/1984). A legislação brasileira estabelece critérios distintos para o abatimento de 1 dia de pena,
dependendo da atividade realizada pelo condenado:

De acordo com a legislação e resoluções vigentes em janeiro de 2026:

- Trabalho: São necessários 3 dias de trabalho para remir 1 dia de pena.(jornada normal 6/8h diárias)
- Estudo: São necessárias 12 horas de frequência escolar para remir 1 dia de pena.(essas 12h devem ser divididas em 3 dias)
- Leitura: A leitura de 1 obra literária possibilita a remição de 4 dias de pena.(máximo: 12 livros por ano)
'''
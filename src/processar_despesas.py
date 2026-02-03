import pandas as pd
import os
import re

# Diretório onde os arquivos extraídos estão localizados
BASE_DIR = "data_extracted"

# Lista para armazenar os registros consolidados
resultado = []

def extrair_ano_trimestre(data_str):

    """
    Recebe uma data no formato YYYY-MM-DD e retorna
    o ano e o trimestre correspondente.
    Ex: 2025-03-31 -> ("2025", "1")
    """

    ano = data_str[:4]
    mes = int(data_str[5:7])

    if mes <= 3:
        tri = "1"
    elif mes <= 6:
        tri = "2"
    elif mes <= 9:
        tri = "3"
    else:
        tri = "4"

    return ano, tri

# Percorrer todos os arquivos extraídos
for file in os.listdir(BASE_DIR):
    if file.endswith(".csv"):
        caminho = os.path.join(BASE_DIR, file)

        # Ler o arquivo CSV no padrão utilizado pela ANS (separado por ";", encoding latin1)
        df = pd.read_csv(caminho, sep=";", encoding="latin1")

        # Filtrar apenas as linhas que representam despesas
        #(eventos relacionados a DESPESA, SINISTRO ou EVENTO)
        despesas = df[df["DESCRICAO"].str.contains("DESPESA|SINISTRO|EVENTO", case=False, na=False)]

        # Processar cada linha de despesa individualmente
        for _, row in despesas.iterrows():
            ano, tri = extrair_ano_trimestre(row["DATA"])

            # Adicionar o registro normalizado ao resultado final
            resultado.append({
                "REG_ANS": row["REG_ANS"],
                "Ano": ano,
                "Trimestre": tri,
                "ValorDespesas": row["VL_SALDO_FINAL"]
            })

# Converter a lista de registros em um DataFrame
consolidado = pd.DataFrame(resultado)

# Salvar o CSV consolidado que será usado nas próximas etapas
consolidado.to_csv("consolidado_despesas.csv", index=False)

print("Arquivo consolidado_despesas.csv gerado!")

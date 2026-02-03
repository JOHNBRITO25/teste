import pandas as pd

# Ler os dados de despesas
despesas = pd.read_csv("consolidado_despesas.csv")

# Ler o cadastro oficial de operadoras
cadastro = pd.read_csv("Relatorio_cadop.csv", sep=";", encoding="latin1")

# Normalizar o nome da coluna de registro
cadastro = cadastro.rename(columns={"REGISTRO_OPERADORA": "REG_ANS", "Razao_Social": "RazaoSocial"})

# Converter REG_ANS para string para evitar erros de join
despesas["REG_ANS"] = despesas["REG_ANS"].astype(str)
cadastro["REG_ANS"] = cadastro["REG_ANS"].astype(str)

# Fazer o join entre despesas e cadastro
base = despesas.merge(cadastro, on="REG_ANS", how="left")

# Remover registros sem CNPJ (operadoras inválidas ou descontinuadas)
base = base[base["CNPJ"].notna()]

# Converter ValorDespesas para número
base["ValorDespesas"] = pd.to_numeric(base["ValorDespesas"], errors="coerce")

# Remover valores zerados ou negativos
base = base[base["ValorDespesas"] > 0]

# Selecionar apenas as colunas exigidas no PDF
final = base[[
    "CNPJ",
    "RazaoSocial",
    "Trimestre",
    "Ano",
    "ValorDespesas"
]]

# Salvar o CSV final
final.to_csv("consolidado_despesas_final.csv", index=False)

print("Arquivo consolidado_despesas_final.csv gerado!")

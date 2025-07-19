import pulp

# Dados
dias_semana = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
demanda_diaria = [400, 350, 375, 380, 450, 350, 250]
num_dias = len(dias_semana)
capacidade_diaria_producao = 400
capacidade_max_estoque = 100

# Custos
custo_preparacao_fixo = 150
custo_unitario_producao = 1
custo_unitario_estoque = 0.5

modelo_lot_sizing = pulp.LpProblem("Dimensionamento_Produção_Bolos", pulp.LpMinimize)
qtd_produzida = pulp.LpVariable.dicts("Qtd_Produzida", dias_semana, lowBound=0, cat="Integer")
estoque_final = pulp.LpVariable.dicts("Estoque_Final", dias_semana, lowBound=0, upBound=capacidade_max_estoque, cat="Integer")
houve_producao = pulp.LpVariable.dicts("Houve_Producao", dias_semana, cat="Binary")

#Função objetivo
modelo_lot_sizing += pulp.lpSum([
    custo_preparacao_fixo * houve_producao[dia] +
    custo_unitario_producao * qtd_produzida[dia] +
    custo_unitario_estoque * estoque_final[dia]
    for dia in dias_semana
])

# Restrições
for i in range(num_dias):
    dia = dias_semana[i]
    demanda_dia = demanda_diaria[i]
    estoque_anterior = estoque_final[dias_semana[i - 1]] if i > 0 else 0
    modelo_lot_sizing += (
        qtd_produzida[dia] + estoque_anterior == demanda_dia + estoque_final[dia],
        f"Balanço_Estoque_{dia}"
    )
for dia in dias_semana:
    modelo_lot_sizing += (
        qtd_produzida[dia] <= capacidade_diaria_producao * houve_producao[dia],
        f"Capacidade_Produção_{dia}"
    )

modelo_lot_sizing.solve()

print("Status:", pulp.LpStatus[modelo_lot_sizing.status])
print("Custo total mínimo: R$", pulp.value(modelo_lot_sizing.objective))
print()

for dia in dias_semana:
    print(f"{dia}: Produzidos = {qtd_produzida[dia].varValue:.0f}, "
          f"Estoque final = {estoque_final[dia].varValue:.0f}")

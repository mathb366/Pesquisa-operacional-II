import pulp

# Dados
dias = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
sabores = ["Chocolate", "Ninho", "Morango", "Creme"]
unidades = ["Matriz", "Filial1", "Filial2"]
confeiteiros = ["Ana", "Bruno", "Carla", "Daniel"]

# Especialização de cada confeiteiro
especializacao = {
    "Ana": "Chocolate",
    "Bruno": "Ninho",
    "Carla": "Morango",
    "Daniel": "Creme"
}

demanda = {
    "Matriz": {
        "Chocolate": [400, 350, 375, 380, 450, 350, 250],
        "Ninho": [325, 350, 325, 350, 375, 350, 325],
        "Morango": [300, 325, 500, 450, 400, 375, 300],
        "Creme": [397, 387, 378, 287, 214, 268, 277]
    },
    "Filial1": {
        "Chocolate": [164, 297, 182, 397, 396, 277, 267],
        "Ninho": [266, 205, 179, 163, 281, 335, 161],
        "Morango": [257, 356, 391, 366, 381, 265, 160],
        "Creme": [280, 245, 228, 296, 358, 324, 354]
    },
    "Filial2": {
        "Chocolate": [191, 266, 286, 343, 167, 287, 208],
        "Ninho": [384, 283, 324, 381, 233, 307, 354],
        "Morango": [339, 311, 319, 201, 326, 177, 387],
        "Creme": [337, 398, 338, 290, 260, 266, 304]
    }
}

# Custos
custo_preparacao = {"Chocolate": 150, "Ninho": 175, "Morango": 160, "Creme": 125}
custo_unitario = {"Chocolate": 1, "Ninho": 2, "Morango": 3, "Creme": 4}
custo_estoque = {"Matriz": 0.50, "Filial1": 0.75, "Filial2": 1.00}
capacidade_estoque = {"Matriz": 150, "Filial1": 150, "Filial2": 150}

# Modelo
model = pulp.LpProblem("Dimensionamento_de_Lotes", pulp.LpMinimize)

# Variáveis
x = pulp.LpVariable.dicts("Produz", (unidades, sabores, dias), lowBound=0, cat='Integer')
s = pulp.LpVariable.dicts("Estoque", (unidades, sabores, dias), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("Setup", (unidades, sabores, dias), cat='Binary')

trabalha = pulp.LpVariable.dicts("Trabalha", (confeiteiros, dias), cat='Binary')

# Função objetivo
model += pulp.lpSum([
    x[u][sabor][d] * custo_unitario[sabor] +
    y[u][sabor][d] * custo_preparacao[sabor] +
    s[u][sabor][d] * custo_estoque[u]
    for u in unidades for sabor in sabores for d in dias
])

# Restrições
for u in unidades:
    for sabor in sabores:
        for i, d in enumerate(dias):
            demanda_dia = demanda[u][sabor][i]
            if i == 0:
                model += x[u][sabor][d] == demanda_dia + s[u][sabor][d]
            else:
                dia_anterior = dias[i - 1]
                model += x[u][sabor][d] + s[u][sabor][dia_anterior] == demanda_dia + s[u][sabor][d]

            model += s[u][sabor][d] <= capacidade_estoque[u]
            model += x[u][sabor][d] <= 1000 * y[u][sabor][d]

# Cada confeiteiro trabalha apenas 2 dias por semana
for c in confeiteiros:
    model += pulp.lpSum([trabalha[c][d] for d in dias]) == 2

for c in confeiteiros:
    sabor = especializacao[c]
    for d in dias:
        for u in unidades:
            model += x[u][sabor][d] <= 10000 * trabalha[c][d]

for d in dias:
    model += pulp.lpSum([trabalha[c][d] for c in confeiteiros]) <= 2 

model.solve()
print(f"Custo total mínimo: R$ {pulp.value(model.objective):,.2f}")
for c in confeiteiros:
    dias_trabalho = [d for d in dias if round(pulp.value(trabalha[c][d])) == 1]
    print(f"{c} (especialista em {especializacao[c]}): trabalha em {dias_trabalho}")

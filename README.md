# Dimensionamento de Lotes na Produção de Bolos

Este repositório contém três projetos de otimização desenvolvidos em Python com a biblioteca `PuLP`, aplicados à produção e distribuição de bolos em uma rede de padarias.

## 📁 Arquivos

- `TP1.py`: Modelo básico de dimensionamento de lotes (Lot Sizing) para uma única fábrica.
- `TP2.py`: Extensão do modelo para múltiplas unidades (Matriz, Filial1 e Filial2) e múltiplos sabores.
- `TP3.py`: Modelo completo com alocação de confeiteiros especializados, respeitando restrições de trabalho.

---

## 📌 Descrição dos Modelos

### 🧮 TP1 - Modelo Básico

Neste primeiro modelo:
- Considera apenas uma unidade produtiva.
- A demanda diária é fixa e conhecida.
- A produção diária tem custo fixo e variável.
- O estoque é limitado a 100 unidades.
- Utiliza variáveis binárias para modelar o custo de preparação (setup) quando há produção.

**Objetivo:** Minimizar o custo total de produção e estoque durante os sete dias da semana.

---

### 🏭 TP2 - Múltiplas Unidades e Sabores

Este modelo amplia o escopo:
- Três unidades produtivas: Matriz, Filial1 e Filial2.
- Quatro sabores de bolo: Chocolate, Ninho, Morango e Creme.
- Cada unidade tem demanda diária específica para cada sabor.
- Considera custos diferentes de estoque por unidade.
- Inclui custo de preparação por sabor e unidade de produção.
- Estoques têm capacidade máxima.

**Objetivo:** Minimizar o custo total de produção, preparação e estoque, atendendo todas as demandas.

---

### 👩‍🍳 TP3 - Modelo com Confeiteiros Especializados

Este é o modelo mais completo:
- Herda a estrutura do TP2.
- Adiciona confeiteiros especializados, cada um em um sabor.
- Cada confeiteiro pode trabalhar apenas dois dias por semana.
- No máximo dois confeiteiros podem trabalhar em um mesmo dia.
- Um sabor só pode ser produzido em um dia, se o confeiteiro correspondente estiver presente.

**Objetivo:** Minimizar os custos totais, considerando também a alocação eficiente dos confeiteiros.

---

## 📦 Dependências

Instale os pacotes necessários com:

```bash
pip install pulp

# Agin2025 (ATGK)

Ferramenta CLI simples para anonimizar **qualquer CSV** via k-anonimato usando Gorilla Optimization + Fuzzy C-Means.

## ✅ Principais Pontos
- Funciona com qualquer CSV (numérico, categórico ou misto)
- Garante k-anonimato (cada linha pertence a um grupo ≥ k)
- Generaliza apenas as colunas que você indicar (quasi-identificadores)
- Saída mantém utilidade estatística básica

## 🚀 Uso Rápido
```powershell
python src/main.py -i data/heart.csv -o output/test.csv -q Age,Sex -k 3
```
Resultado em `output/test.csv`.

## 📦 Instalação
```powershell
python -m venv .venv; .\.venv\Scripts\activate
pip install -r requirements.txt  # (se existir) OU:
pip install numpy pandas scikit-learn
```
Ou instale como pacote (após adicionar dependências ao pyproject):
```powershell
pip install .
atgk -i data/heart.csv -o output/test.csv -q Age,Sex -k 3
```

## 🔧 Sintaxe
```powershell
python src/main.py -i <input.csv> -o <saida.csv> -q col1,col2,... -k <valor_k>
```
Principais parâmetros:
- -i / --input: CSV de entrada
- -o / --output: CSV de saída
- -q / --quasi-identifiers: colunas a anonimizar (separadas por vírgula)
- -k / --k-anonymity: tamanho mínimo de cada grupo
Opcionais:
- --gorillas (40) | --iterations (75) | --clusters (max(5,k))
- --separator "," | --encoding utf-8 | --no-header
- --preview 5 | --quiet

## 🎯 Escolha dos Quasi-Identificadores
Inclua apenas colunas que, combinadas, possam identificar indivíduos:
- Demográficos: idade, sexo, raça
- Geográficos: cep, cidade, bairro
- Socioeconômicos: renda, escolaridade
- Temporais: ano_nasc, data_admissao
Não inclua: IDs diretos (CPF, email), nomes próprios, campos que deseja manter intactos.

## 💡 Exemplo
Entrada (`clientes.csv`):
```csv
id,nome,idade,cidade,renda,compras
1,João,34,São Paulo,5000,12
2,Maria,35,São Paulo,5200,15
3,Pedro,33,Rio de Janeiro,4800,10
```
Comando:
```powershell
python src/main.py -i clientes.csv -o clientes_anon.csv -q idade,cidade,renda -k 3
```
Saída simplificada:
```csv
id,nome,idade,cidade,renda,compras
1,João,[33.00-35.00],[Rio de Janeiro-São Paulo],[4800.00-5200.00],12
2,Maria,[33.00-35.00],[Rio de Janeiro-São Paulo],[4800.00-5200.00],15
3,Pedro,[33.00-35.00],[Rio de Janeiro-São Paulo],[4800.00-5200.00],10
```

## ⚙️ Ajustes Rápidos
- Execução mais rápida: `--gorillas 20 --iterations 30`
- Mais qualidade: aumentar `--gorillas` e `--iterations`
- k muito alto => intervalos mais largos (perda de detalhe)

## � Interpretação da Saída
Intervalos representam o grupo; todos os registros do grupo compartilham o mesmo intervalo por coluna marcada como QI.

## 🐛 Problemas Comuns
- Coluna não encontrada: verifique nome exato / use `--preview`
- Grupo menor que k: reduza k ou aumente clusters
- Lento: diminua gorillas / iterations

## 🤝 Contribuição
Pull requests e Issues são bem-vindos.

## 📄 Licença
Ver arquivo `LICENSE`.

## 🔗 Algoritmos
GOA (Gorilla Optimization), Fuzzy C-Means, k-Anonymity.

## ⭐ Resumo Final
Comece agora:
```powershell
python src/main.py -i seu.csv -o anon.csv -q colA,colB -k 5
```

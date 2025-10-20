# 🚀 Quick Start Guide - ATGK

## Para Qualquer Dataset CSV

O ATGK funciona com **QUALQUER dataset CSV**. Não importa o domínio - saúde, finanças, educação, e-commerce, etc.

## 📋 Checklist Rápido

### 1️⃣ Prepare seu CSV
- ✅ Certifique-se de que é um arquivo CSV válido
- ✅ Primeira linha deve conter os nomes das colunas
- ✅ Dados podem ser numéricos, categóricos ou mistos

### 2️⃣ Identifique seus Quasi-identificadores
Pergunte-se: "Quais colunas, quando combinadas, poderiam identificar uma pessoa?"

**Exemplos comuns:**
- 👤 Demográficos: `age`, `gender`, `race`, `birth_year`
- 📍 Geográficos: `zipcode`, `city`, `state`, `neighborhood`
- 💰 Socioeconômicos: `income`, `salary`, `education`, `occupation`
- 🕐 Temporais: `admission_date`, `purchase_date`, `enrollment_year`

**❌ NÃO incluir:**
- IDs únicos (CPF, email, nome)
- Dados sensíveis que você quer preservar
- Colunas que não contribuem para identificação

### 3️⃣ Escolha seu k
- **k=3-5**: Para datasets pequenos ou quando você quer manter mais detalhes
- **k=5-10**: Recomendado para a maioria dos casos (bom equilíbrio)
- **k=10-20**: Alta privacidade, mas mais generalização
- **k>20**: Máxima privacidade (pode perder muitos detalhes)

### 4️⃣ Execute o comando

```bash
python src/main.py -i seu_arquivo.csv -o output.csv -q col1,col2,col3 -k 5
```

## 🎯 Exemplo Passo a Passo

### Cenário: Você tem dados de clientes

**Arquivo:** `clientes.csv`
```csv
id,nome,idade,cidade,renda,compras
1,João,34,São Paulo,5000,12
2,Maria,35,São Paulo,5200,15
3,Pedro,33,Rio de Janeiro,4800,10
```

### Passo 1: Identifique QIs
- ❌ `id` - identificador único, não incluir
- ❌ `nome` - nome próprio, não incluir
- ✅ `idade` - pode identificar quando combinado
- ✅ `cidade` - pode identificar quando combinado
- ✅ `renda` - pode identificar quando combinado
- ❓ `compras` - geralmente não é QI (mas depende do contexto)

**QIs escolhidos:** `idade,cidade,renda`

### Passo 2: Execute

```bash
python src/main.py -i clientes.csv -o clientes_anon.csv -q idade,cidade,renda -k 3
```

### Passo 3: Resultado

```csv
id,nome,idade,cidade,renda,compras
1,João,[33.00-35.00],[Rio de Janeiro-São Paulo],[4800.00-5200.00],12
2,Maria,[33.00-35.00],[Rio de Janeiro-São Paulo],[4800.00-5200.00],15
3,Pedro,[33.00-35.00],[Rio de Janeiro-São Paulo],[4800.00-5200.00],10
```

✅ `id`, `nome`, `compras` **preservados**  
✅ `idade`, `cidade`, `renda` **anonimizados**  
✅ Cada registro agora é indistinguível de pelo menos 2 outros (k=3)

## 📊 Casos de Uso por Domínio

### 🏥 Saúde
```bash
python src/main.py -i hospital.csv -o hospital_anon.csv -q idade,sexo,cep,data_admissao -k 5
```

### 💼 RH/Empresa
```bash
python src/main.py -i funcionarios.csv -o func_anon.csv -q idade,departamento,cidade,faixa_salarial -k 8
```

### 🎓 Educação
```bash
python src/main.py -i alunos.csv -o alunos_anon.csv -q idade,escola,cep,ano_ingresso -k 5
```

### 🛒 E-commerce
```bash
python src/main.py -i clientes.csv -o clientes_anon.csv -q idade,cidade,faixa_renda,categoria -k 10
```

### 📱 Tecnologia/Apps
```bash
python src/main.py -i usuarios.csv -o usuarios_anon.csv -q idade,pais,tipo_dispositivo,data_cadastro -k 7
```

## ⚙️ Ajuste Fino

### Dataset Pequeno (< 1000 linhas)
```bash
python src/main.py -i small.csv -o anon.csv -q col1,col2 -k 3 --clusters 3 --iterations 50
```

### Dataset Médio (1000-10000 linhas)
```bash
python src/main.py -i medium.csv -o anon.csv -q col1,col2,col3 -k 5 --clusters 8 --iterations 75
```

### Dataset Grande (> 10000 linhas)
```bash
python src/main.py -i large.csv -o anon.csv -q col1,col2,col3,col4 -k 10 --clusters 15 --gorillas 60 --iterations 100
```

### Execução Rápida (teste)
```bash
python src/main.py -i test.csv -o test_anon.csv -q col1,col2 -k 3 --gorillas 20 --iterations 30
```

### Alta Qualidade (produção)
```bash
python src/main.py -i prod.csv -o prod_anon.csv -q col1,col2,col3 -k 8 --gorillas 80 --iterations 150
```

## 🔍 Verificando o Resultado

Após executar, o programa mostra:

```
============================================================
ATGK Anonymization
============================================================
Dataset: 1000 records, 8 columns
Quasi-identifiers: age, city, income
k-anonymity: 5
Parameters: gorillas=40, iterations=75, clusters=5
============================================================

Optimizing with ATGK (iterations: 75)...
  Iteration 10/75 - Best fitness: 2.1234
  Iteration 20/75 - Best fitness: 1.8765
  ...
Anonymization complete: 5/5 clusters anonymized

============================================================
Anonymization completed successfully!
============================================================
```

✅ **"5/5 clusters anonymized"** = Sucesso total!  
⚠️ **"4/5 clusters anonymized"** = Alguns clusters têm < k registros (aumente `--clusters` ou reduza `k`)

## 💡 Dicas Importantes

1. **Comece simples**: Use poucos QIs primeiro, depois adicione mais se necessário
2. **Teste com k pequeno**: Comece com k=3 ou k=5 para ver como funciona
3. **Verifique os resultados**: Use `--preview 10` para ver antes/depois
4. **Não exagere no k**: k muito alto = muita generalização = perda de utilidade
5. **Use --quiet para produção**: Remove mensagens verbosas

## ❓ Problemas Comuns

### "Quasi-identifiers not found in dataset"
**Solução:** Verifique os nomes exatos das colunas. Use:
```bash
python src/main.py -i seu_arquivo.csv -o output.csv -q col1,col2 -k 5 --preview 5
```

### "Cluster has only X records"
**Solução:** Aumente `--clusters` ou reduza `k`
```bash
python src/main.py -i seu_arquivo.csv -o output.csv -q col1,col2 -k 5 --clusters 10
```

### Muito lento
**Solução:** Reduza parâmetros de otimização
```bash
python src/main.py -i seu_arquivo.csv -o output.csv -q col1,col2 -k 5 --gorillas 20 --iterations 30
```

## 🎉 Pronto!

Agora você pode anonimizar **qualquer dataset CSV** com ATGK!

Para mais exemplos, veja `EXAMPLES.md`  
Para documentação completa, veja `README.md`

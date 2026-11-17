# Análise de Sentimento com PLN

Projeto desenvolvido na aula de Fundamentos de Inteligencia Artificial, desenvolvido em Python para classificar avaliações de produtos em sentimentos positivos ou negativos utilizando Processamento de Linguagem Natural (PLN). 

## Tecnologias utilizadas

- Python
- Pandas
- NumPy
- Scikit-learn

## Estrutura do projeto

- `data/`: arquivos CSV com avaliações e casos difíceis.
- `resultados/`: arquivos gerados durante a análise.
- `main.py`: código principal do projeto.
- `RELATORIO.md`: relatório com os resultados e conclusões.

## Como executar

1. Instale o Python 3.10 ou superior.
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Execute o programa:
```bash
python main.py
```
## Experimentos

Foram comparadas quatro configurações utilizando:

- Bag of Words (BoW)
- TF-IDF
- Stopwords mantidas e removidas
- Regressão Logística

A configuração *C* apresentou o melhor resultado na validação cruzada, com 80% de acurácia média.

## Autora

Caroline Lopes de Carvalho — Estudante de Análise e Desenvolvimento de Sistemas.
Classe: Fundamentos de Inteligencia Artificial.
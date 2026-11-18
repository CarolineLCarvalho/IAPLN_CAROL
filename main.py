import re
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    make_scorer
)
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.pipeline import Pipeline


BASE = Path(__file__).parent
DATA = BASE / "data"
RESULTADOS = BASE / "resultados"
RESULTADOS.mkdir(exist_ok=True)

avaliacoes = pd.read_csv(DATA / "avaliacoes.csv")
casos = pd.read_csv(DATA / "casos_dificeis.csv")

avaliacoes["sentimento"] = avaliacoes["sentimento"].str.strip().str.lower()

stopwords = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    "de", "da", "do", "das", "dos", "em", "no", "na",
    "nos", "nas", "para", "por", "com", "e", "ou",
    "que", "é", "foi", "ser", "ao", "se"
}


def limpar_texto(texto, remover_stopwords=False):
    texto = texto.lower()
    palavras = re.findall(r"[a-záàâãéêíóôõúçü]+", texto)

    if remover_stopwords:
        palavras = [p for p in palavras if p not in stopwords]

    return " ".join(palavras)


X = avaliacoes["texto"]
y = avaliacoes["sentimento"]

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

configuracoes = [
    ("A", False, "BoW", CountVectorizer),
    ("B", False, "TF-IDF", TfidfVectorizer),
    ("C", True, "BoW", CountVectorizer),
    ("D", True, "TF-IDF", TfidfVectorizer)
]

resultados = []
modelos = {}

f1 = make_scorer(f1_score, pos_label="positivo")

for nome, remover, tipo, vetor in configuracoes:
    modelo = Pipeline([
        ("vetorizador", vetor(
            preprocessor=lambda texto, r=remover: limpar_texto(texto, r),
            tokenizer=str.split,
            token_pattern=None,
            lowercase=False
        )),
        ("classificador", LogisticRegression(max_iter=1000))
    ])

    validacao = cross_validate(
        modelo,
        X_treino,
        y_treino,
        cv=5,
        scoring={"accuracy": "accuracy", "f1": f1}
    )

    modelo.fit(X_treino, y_treino)
    vocabulario = len(modelo.named_steps["vetorizador"].vocabulary_)

    resultados.append({
        "config": nome,
        "stopwords": "removidas" if remover else "mantidas",
        "vetorizador": tipo,
        "vocabulario": vocabulario,
        "acc_cv_media": validacao["test_accuracy"].mean(),
        "acc_cv_desvio": validacao["test_accuracy"].std(),
        "f1_cv_media": validacao["test_f1"].mean(),
        "f1_cv_desvio": validacao["test_f1"].std()
    })

    modelos[nome] = modelo

comparacao = pd.DataFrame(resultados)
comparacao.to_csv(RESULTADOS / "comparacao.csv", index=False)

melhor_config = comparacao.loc[comparacao["f1_cv_media"].idxmax(), "config"]
modelo_final = modelos[melhor_config]

previsoes = modelo_final.predict(X_teste)
probabilidades = modelo_final.predict_proba(X_teste).max(axis=1)

pd.DataFrame(
    confusion_matrix(y_teste, previsoes, labels=["negativo", "positivo"]),
    index=["real_negativo", "real_positivo"],
    columns=["previsto_negativo", "previsto_positivo"]
).to_csv(RESULTADOS / "matriz_confusao.csv")

relatorio = classification_report(y_teste, previsoes)
(RESULTADOS / "relatorio_classificacao.txt").write_text(relatorio, encoding="utf-8")

erros = pd.DataFrame({
    "texto": X_teste.reset_index(drop=True),
    "real": y_teste.reset_index(drop=True),
    "previsto": previsoes,
    "probabilidade": probabilidades
})

erros = erros[erros["real"] != erros["previsto"]]
erros.to_csv(RESULTADOS / "erros.csv", index=False)

vetorizador = modelo_final.named_steps["vetorizador"]
classificador = modelo_final.named_steps["classificador"]

nomes_palavras = vetorizador.get_feature_names_out()
coeficientes = classificador.coef_[0]

if classificador.classes_[1] != "positivo":
    coeficientes = -coeficientes

palavras = pd.DataFrame({
    "palavra": nomes_palavras,
    "coeficiente": coeficientes
})

influentes = pd.concat([
    palavras.nlargest(10, "coeficiente"),
    palavras.nsmallest(10, "coeficiente")
])

influentes.to_csv(RESULTADOS / "palavras_influentes.csv", index=False)

casos["previsao"] = modelo_final.predict(casos["texto"])
casos["probabilidade_positivo"] = modelo_final.predict_proba(
    casos["texto"]
)[:, list(classificador.classes_).index("positivo")]

casos_resultado = casos[["texto", "tipo", "sentimento_esperado"]].copy()
casos_resultado["previsto"] = casos["previsao"]
casos_resultado["probabilidade_positivo"] = casos["probabilidade_positivo"]

casos_resultado.columns = [
    "texto", "tipo", "esperado", "previsto", "probabilidade_positivo"
]

casos_resultado.to_csv(
    RESULTADOS / "casos_dificeis_resultados.csv",
    index=False
)

print("Análise concluída!")
print("Melhor configuração:", melhor_config)
print("Resultados salvos na pasta resultados.")
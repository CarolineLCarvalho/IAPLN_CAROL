# relatório — análise de sentimento com pln

*nome:* caroline lopes de carvalho  
*repositório:* [coloque o link do seu github]  
*data:* 17/11/2026

## tabela-resumo

| config | stopwords | vetorizador | vocabulário | acurácia cv (média ± desvio) | f1 cv (média ± desvio) |
|---|---|---|---:|---:|---:|
| a | mantidas | bow | 425 | 78,46% ± 7,36% | 78,89% ± 6,75% |
| b | mantidas | tf-idf | 425 | 76,92% ± 5,13% | 76,88% ± 4,99% |
| c | removidas | bow | 407 | 80,00% ± 5,48% | 80,15% ± 5,39% |
| d | removidas | tf-idf | 407 | 78,97% ± 6,36% | 79,12% ± 6,52% |

*configuração escolhida:* c  
*acurácia no teste:* 84,62%  
*f1 no teste:* 84,62% (f1 macro, aproximadamente)

---

## 1. pré-processamento

no pré-processamento, deixei todos os textos em letras minúsculas e retirei as pontuações e os números, mas deixei os acentos, também criei uma lista com 29 stopwords para comparar os resultados mantendo e removendo essas palavras, a palavra "não" foi mantida porque é importante para identificar negações e pode mudar o sentido de uma frase, no final, o vocabulário ficou com 425 palavras nas configurações com stopwords e 407 nas configurações sem stopwords, com isso foi possível perceber que a remoção dessas palavras diminuiu o tamanho do vocabulário.

## 2. bow vs. tf-idf

a configuração C apresentou os melhores resultados, com 80% de acurácia média e 80,15% de f1 médio na validação cruzada, o bow também apresentou resultados melhores que o tf-idf nas duas comparações, os desvios padrão mostraram que houve algumas diferenças entre as divisões dos dados, então não considero que os resultados sejam tão distantes assim.
o bow conta a frequência com que as palavras aparecem, enquanto o tf-idf dá mais importância para palavras que aparecem menos vezes nos textos. escolhi a configuração c porque foi a que apresentou a maior média de f1 na validação cruzada, sem usar os resultados do teste para decidir qual modelo seria escolhido.

## 3. avaliação no teste

na matriz de confusão, o modelo acertou 26 avaliações negativas e 29 positivas. também classificou 7 avaliações negativas como positivas e 3 positivas como negativas.
para a classe negativa, a precisão foi 0,90, o recall foi 0,79 e o f1 foi 0,84. já para a classe positiva, a precisão foi 0,81, o recall foi 0,91 e o f1 foi 0,85.
considero mais grave para uma loja classificar uma reclamação como elogio, porque isso pode fazer com que um problema real passe despercebido. nesse trabalho, a acurácia representa bem os resultados porque as duas classes possuem quantidades parecidas de exemplos. isso seria diferente em um caso de fraude, por exemplo, em que uma das classes poderia ter muito menos exemplos que a outra.

## 4. validação cruzada vs. divisão única

a validação cruzada é uma forma mais confiável de comparar as configurações, porque os dados de treinamento são divididos em diferentes partes e o modelo é avaliado várias vezes. no meu trabalho, utilizei cinco divisões e calculei a média e o desvio padrão dos resultados.
não é correto escolher o modelo olhando os resultados do teste, porque isso poderia influenciar a escolha e deixar a avaliação final menos confiável. um exemplo de vazamento de dados seria criar o vocabulário utilizando também os dados de teste. para evitar esse problema, utilizei o pipeline, que faz a vetorização durante cada etapa do treinamento. também deixei os casos difíceis separados dos dados de treinamento.

## 5. análise de erros e palavras influentes

um dos erros aconteceu na frase "o sabor é maravilhoso e as porções são generosas", que era positiva, mas foi classificada como negativa. outro erro aconteceu na frase "panela de péssima qualidade, a comida gruda e queima", que era negativa, mas foi classificada como positiva.
também aconteceu um erro na frase "cheguei animado, mas me arrependi, tudo estava sujo". acredito que isso aconteceu porque o modelo teve dificuldade para entender a mudança de sentido da frase.
entre as palavras positivas apareceram "ótimo", "gostei" e "excelente". já entre as negativas apareceram "não", "decepcionado" e "terrível". algumas palavras, como "bastante", "bem", "tudo", "mais" e "dinheiro", não possuem um sentimento positivo ou negativo por si mesmas. isso mostra que o modelo conseguiu relacionar algumas palavras aos sentimentos, mas ainda tem dificuldade para entender o contexto completo das frases.

## 6. casos difíceis e limitações

nos casos de negação, o modelo acertou 2 dos 4 exemplos. nas frases irônicas, acertou 2 dos 3 exemplos, mostrando que teve dificuldade para perceber quando uma palavra positiva estava sendo usada com um sentido negativo.
nas frases com sentimentos mistos, classificou as duas como positivas. isso acontece porque o modelo trabalha apenas com as classes positivo e negativo, não conseguindo representar corretamente quando uma frase apresenta os dois sentimentos.
também classificou a frase neutra "chegou ontem" como negativa.
como melhorias, poderiam ser utilizados bigramas, que ajudam a considerar combinações de palavras, e um tratamento melhor para as negações, considerando expressões como "não gostei".
duas limitações do conjunto de dados são a quantidade pequena de exemplos, com apenas 260 avaliações, e o fato de trabalhar somente com duas classes. um risco de utilizar esse modelo em uma situação real seria deixar reclamações sem atenção porque foram classificadas incorretamente como elogios.

---

## declaração de uso de ia

- [ ] não usei ia generativa em nenhuma parte deste trabalho.
- [x] usei ia generativa para ajudar nas explicações de alguns conceitos, nas configurações das dependências, na organização das pastas e para tirar dúvidas sobre alguns erros que tive no projeto.
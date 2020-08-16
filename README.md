# Riscos e Recomendações


## Risks-and-Recommendations
Programs to read risks and recommendations produced by the Regente platform and create roadmap spreadsheet with scores and frequencies.

## Riscos

### Lerjson.py:

a partir de json produzido pelo Regente, cria arquivo com os riscos, Riscoscsv.csv, primeira aba da planilha roadmap

### Lerjson.js
Versão Javascript de lerjson.py
Segue mesma lógica e estrutura de dados, não foi repensado por enquanto
Ainda não usei Typescript

## Recomendações

### Lerecom.py: (primeira versão)

Lê as recomendações do Regente e produz arquivo Strings.csv. Aí carregar em planilha, que vai separar as recomendações em seus vários itens. Gravar .csv

Diversos testes feitos, inclusive um para avaliar o valor de corte da medida Leuvenshtein: Lê csv, aplica medida de leuvenshtein, compara cada recomendação com todas as outras calculando frequência e produz lista de frequência por recomendação.

Observar que a frequência não é propriamente uma frequência exata. Depende do parametro adotado para corte. Estimado num primeiro teste: Leuven1.csv

seprador.py: separa recomendação múltipla, tira os números, tira os brancos no começo, grava Separados.csv

Fazerlista.py: Faz a lista de recomendações, aplicando Leuvenshtein

### Lerecom.py: (versão final)

junta os vários programas anteriores

Não precisa mais passar pela etapa de carregar numa planilha porque consegui separar recomendações múltiplas colocando um "\n" ao final. E mais eliminar os 1), 2)..., os brancos, etc

lê o json do Regente, separa recomendações múltiplas, limpa, aplica Leveinshtein, e produz lista final: frequencias.csv

### lerecom.JS:
Programas para Regente em js e node

## trocaTexto
TrocaTexto.ts
Programa que testa as 2 funções AchaSemelhante e TrocaFrase, a serem usadas no Regente Alfa para facilitar digitação de recomendações

## Notas

1. Os programas ainda têm os print() diversos usados para debug
2. Copiado do diretorio de trabalho dt, antigo diretorio rr
3. myApp: tutorial NetCore


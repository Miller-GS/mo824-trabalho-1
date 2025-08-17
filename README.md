# mo824-trabalho-1
Repositório para trabalho 1 da disciplina de MO824

## Descrição do problema
O problema consiste em resolver uma instância de Max-SC-QBF.

É dada uma função quadrática binária (QBF), no formato sum(Aij * Xi * Xj), sendo Aij um coeficiente, e Xi e Xj variáveis binárias dentre as N de entrada.
Também são dados N conjuntos, cada um associado a uma variável. Esses conjuntos possuem elementos de 1 até N.

A solução precisa maximizar a QBF e cobrir todos os elementos dos conjuntos.

## Solver
Para utilizar o solver:
1. Abra o diretório src/solver
2. Instale as dependências com `pip install -r requirements.txt`
3. Execute o seguinte comando:

```
python solver.py --input <caminho_para_o_arquivo_de_entrada> -v
```

O arquivo de entrada deve ser gerado no formato
```
<n> (número de variáveis binárias)
<s1> <s2> ... <sn> (número de elementos cobertos por cada subconjunto)
<lista de elementos cobertos por S1>
<lista de elementos cobertos por S2>
...
<lista de elementos cobertos por Sn>
<a11> <a12> ... <a1n>
<a22> ... <a2n>
...
<ann>
```
conforme especificado no enunciado do problema.


O parâmetro -v é opcional e ativa a saída detalhada do processo de resolução.

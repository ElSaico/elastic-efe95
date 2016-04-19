# Relatório sobre ferramenta de IR: Elasticsearch

Autor: Bruno Oliveira Marques

## Pré-requisitos

* Elasticsearch 2.x
* Python 3.x
* Bibliotecas [lxml](http://lxml.de/) e [elasticsearch-py](http://elasticsearch-py.readthedocs.org/)

## Utilização

Os scripts fornecidos assumem que existe uma instância do Elasticsearch em execução na máquina local, acessível através da porta padrão (9200).

### loaddata.py

O script `loaddata.py` é o responsável por ler o corpus e armazená-lo corretamente no sistema. Para que ele funcione é preciso copiar a pasta `efe95`, contendo o corpus a ser processado, para a mesma localização dele.

A execução dele pode ser feita na linha de comando sem parâmetros adicionais:
```
$ python loaddata.py
```

### query.py

Já o script `query.py` é responsavel por ler o arquivo de consultas (já presente no repositório) e, a partir daí, pesquisar os dados armazenados na base.
Devido a uma configuração presente no `loaddata.py`, os campos de texto são armazenados de duas formas distintas:

* **title** e **text** - título e conteúdo, respectivamente, sem nenhuma forma de tratamento
* **title.spanish** e **text.spanish** - os mesmos campos descritos acima, porém utilizando o analisador de língua espanhola padrão do Elasticsearch

A consulta é realizada sobre ambas as variações, cada uma delas gerando um arquivo de saída: `results-standard.txt` e `results-spanish.txt`, respectivamente.
A execução do script ocorre da mesma forma que o anterior:
```
$ python query.py
```

## Funcionalidades presentes

O Elasticsearch fornece uma vasta gama de filtros prontos para processamento de texto - para utilizá-los, basta configurar os campos onde eles devem ser aplicados. Com eles é possível implementar, dentre vários outros:

* remoção de stopwords
* stemmização
* preservação de termos-chave (exceções a stemmização)
* normalização de maiúsculas/minúsculas
* tokenização por n-gramas
* tokenização fonética
* identificação de termos compostos

Uma lista mais completa pode ser vista na [documentação do Elasticsearch sobre analisadores](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html).

## Técnicas utilizadas

Conforme descrito acima, são gerados dois arquivos de saída:

* `results-standard.txt`, utilizando apenas a busca de texto normal
* `results-spanish.txt`, utilizando o analisador de textos de língua espanhola incluso no Elasticsearch - que implementa, nesta ordem:
  * normalização de maiúsculas e minúsculas
  * remoção de stopwords
  * marcação de palavras-chave
  * stemmização

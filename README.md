# ANÁLISE DE FLUXO DE DADOS

Trabalho da disciplina de **Compiladores** da Universidade Federal do Ceará – Campus Quixadá, lecionada pelo professor **Lucas Ismaily**, no semestre **2025.1**.

Realizado pelos alunos:

| Nome                                     | Matrícula | GitHub         |
|------------------------------------------|-----------|----------------|
| Francisco Djalma Pereira da Silva Júnior | 554222    | @juniors719    |
| Francisco Leudes Bezerra Neto            | 552478    | @Leudes        |
| Kauan Pablo de Sousa Silva               | 556027    | @auanK         |

---

## Descrição do Projeto

O trabalho consiste em implementar **três algoritmos clássicos de Análise de Fluxo de Dados** sobre um **grafo de fluxo de controle**. Os algoritmos desenvolvidos foram:

- **🔵 Análise de Longevidade (Liveness Analysis):**
  Determina para cada ponto do programa quais variáveis contêm valores que ainda poderão ser utilizados.

- **🟢 Definições Alcançantes (Reaching Definitions):**
  Identifica o conjunto de definições que podem alcançar cada ponto do programa.

- **🟡 Expressões Disponíveis (Available Expressions):**
  Encontra o conjunto de expressões cujo valor já foi calculado e continua válido em cada ponto do programa.

---

## Requisitos

O projeto foi desenvolvido em **Python** e **não requer bibliotecas externas**.
É necessário ter instalado:

- Python 3.x

---

## Como Executar o Projeto

1. **Preparar o ambiente**
   Crie uma pasta chamada `in/` na raiz do projeto (caso ainda não exista) e coloque os arquivos de teste dentro dela, por exemplo: `1.txt`, `2.txt`, etc.
   Cada arquivo deve conter a representação de um grafo de fluxo de controle, conforme especificado no enunciado do trabalho.

2. **Executar as análises**
   Para rodar cada análise, utilize os seguintes comandos na raiz do projeto:

   ```bash
   # Executa a Análise de Longevidade
   python3 longevidade/longevidade.py

   # Executa a Análise de Definições Alcançantes
   python3 reaching_definitions/reaching_definitions.py

   # Executa a Análise de Expressões Disponíveis
   python3 expressoes_disponiveis/expressoes_disponiveis.

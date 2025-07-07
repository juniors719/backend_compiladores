import re
import os

class BlocoBasico:
    """
    Representa um bloco básico no grafo de fluxo de controle
    """
    def __init__(self, numero):
        self.numero = numero
        self.instrucoes = []
        self.sucessores = []

        self.use = set()
        self.def_ = set()
        self.in_set = set()
        self.out_set = set()
    def __repr__(self):
        return f"Bloco {self.numero}: Sucessores={self.sucessores}, IN={sorted(list(self.in_set))}, OUT={sorted(list(self.out_set))}"

def extrair_variaveis(instrucao):
    """
    Extrai a variável definida e as variáveis usadas de uma instrução.
    Exemplo: 'd = a + b' -> def='d', use={'a', 'b'}
    """
    if '=' in instrucao:
        lado_esq, lado_dir = instrucao.split('=')
        definida = lado_esq.strip()
        usadas = set(re.findall(r"[a-zA-Z_]\w*", lado_dir))
    else:
        definida = None
        usadas = set(re.findall(r"[a-zA-Z_]\w*", instrucao))
    return definida, usadas


def calcular_use_def(bloco):
    """
    Calcula os conjuntos 'use' e 'def' para um bloco básico.
    """
    defs_no_bloco = set()
    for instrucao in bloco.instrucoes:
        definida, usadas = extrair_variaveis(instrucao)
        for usada in usadas:
            if usada not in defs_no_bloco:
                bloco.use.add(usada)
        if definida:
            defs_no_bloco.add(definida)
    bloco.def_ = defs_no_bloco

def analisar_longevidade(blocos):
    """
    Executa o algoritmo iterativo de Análise de Longevidade.
    """
    numero_blocos = sorted(blocos.keys(), reverse=True)

    alterou = True
    while alterou:
        alterou = False
        for num_bloco in numero_blocos:
            bloco = blocos[num_bloco]
            novo_out = set()
            for num_sucessor in bloco.sucessores:
                if num_sucessor in blocos:
                    novo_out.update(blocos[num_sucessor].in_set)
            novo_in = bloco.use.union(novo_out - bloco.def_)
            if novo_in != bloco.in_set or novo_out != bloco.out_set:
                alterou = True
                bloco.in_set = novo_in
                bloco.out_set = novo_out

def ler_entrada(dados_entrada):
    """
    Lê a entrada e constrói o grafo de blocos básicos, seguindo o formato
    especificado no enunciado do trabalho.
    """
    blocos = {}
    linhas = dados_entrada.strip().split('\n')
    i = 0
    while i < len(linhas):
        partes_info = linhas[i].split()
        if not partes_info:
            i += 1
            continue
        num_bloco = int(partes_info[0])
        qtd_instrucoes = int(partes_info[1])
        i += 1
        bloco = BlocoBasico(num_bloco)
        bloco.instrucoes = [l.strip() for l in linhas[i : i + qtd_instrucoes]]
        i += qtd_instrucoes
        sucessores = [int(s) for s in linhas[i].split() if s != '0']
        bloco.sucessores = sucessores
        i += 1
        blocos[num_bloco] = bloco
    return blocos

def formatar_saida(blocos):
    """
    Gera a string de saída formatada com os resultados da análise.
    """
    linhas_saida = []
    linhas_saida.append("Resultado da Análise de Longevidade:")
    for num_bloco in sorted(blocos.keys()):
        bloco = blocos[num_bloco]
        in_formatado = sorted(bloco.in_set)
        out_formatado = sorted(bloco.out_set)
        linhas_saida.append(f"IN[{bloco.numero}] = {in_formatado}")
        linhas_saida.append(f"OUT[{bloco.numero}] = {out_formatado}")
        linhas_saida.append("-" * 20)
    return "\n".join(linhas_saida)

def main():
    PASTA_ENTRADA = "../in"
    PASTA_SAIDA = "out"

    if not os.path.isdir(PASTA_ENTRADA):
        print(f"Erro: A pasta de entrada '{PASTA_ENTRADA}' não foi encontrada.")
        print(f"Por favor, crie a pasta '{PASTA_ENTRADA}' e coloque os ficheiros de teste (ex: 1.txt, 2.txt) dentro dela.")
        return

    os.makedirs(PASTA_SAIDA, exist_ok=True)

    print(f"A ler ficheiros da pasta '{PASTA_ENTRADA}'...")
    for nome_ficheiro in os.listdir(PASTA_ENTRADA):
        caminho_entrada = os.path.join(PASTA_ENTRADA, nome_ficheiro)
        caminho_saida = os.path.join(PASTA_SAIDA, nome_ficheiro)

        print(f"A processar '{caminho_entrada}'...")

        with open(caminho_entrada, 'r', encoding='utf-8') as f:
            dados_entrada = f.read()

        blocos = ler_entrada(dados_entrada)
        for num_bloco in blocos:
            calcular_use_def(blocos[num_bloco])
        analisar_longevidade(blocos)
        conteudo_saida = formatar_saida(blocos)

        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(conteudo_saida)
            print(f" -> Resultado salvo em '{caminho_saida}'")
    print("\nProcessamento concluído com sucesso!")

if __name__ == "__main__":
    main()
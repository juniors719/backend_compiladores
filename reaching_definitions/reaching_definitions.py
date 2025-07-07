import re
import os
from collections import defaultdict

class Definicao:
    """
    Representa uma única definição (ex: d1, d2), conforme os slides.
    Cada definição tem um ID único, a variável que define, e onde ocorre.
    """
    def __init__(self, id_def, var, bloco_num):
        self.id = id_def
        self.var = var
        self.bloco_num = bloco_num

    def __repr__(self):
        return self.id
    
    def __lt__(self, other):
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Definicao) and self.id == other.id

class BlocoBasico:
    """
    Representa um bloco básico com campos para a análise de Definições Alcançantes.
    """
    def __init__(self, numero):
        self.numero = numero
        self.instrucoes = []
        self.sucessores = []
        self.predecessores = []
        self.gen_rd = set()
        self.kill_rd = set()
        self.in_rd = set()
        self.out_rd = set()

    def __repr__(self):
        in_rd_str = sorted([d.id for d in self.in_rd])
        out_rd_str = sorted([d.id for d in self.out_rd])
        return f"Bloco {self.numero}: Sucessores={self.sucessores}, IN_RD={in_rd_str}, OUT_RD={out_rd_str}"

def extrair_variavel_definida(instrucao):
    if '=' in instrucao:
        return instrucao.split('=', 1)[0].strip()
    return None

def pre_processar_definicoes(blocos):
    """
    Encontra todas as definições no programa e as mapeia.
    """
    todas_as_defs = {}
    defs_por_variavel = defaultdict(set)
    def_count = 1
    
    for num_bloco in sorted(blocos.keys()):
        for instrucao in blocos[num_bloco].instrucoes:
            var_def = extrair_variavel_definida(instrucao)
            if var_def:
                id_def = f"d{def_count}"
                definicao = Definicao(id_def, var_def, num_bloco)
                todas_as_defs[id_def] = definicao
                defs_por_variavel[var_def].add(definicao)
                def_count += 1
    return todas_as_defs, defs_por_variavel

def calcular_gen_kill_rd(blocos, defs_por_variavel):
    """
    Calcula os conjuntos GEN e KILL para cada bloco.
    """
    for bloco in blocos.values():
        defs_locais = {}
        for instrucao in bloco.instrucoes:
            var_def = extrair_variavel_definida(instrucao)
            if var_def:
                for d_obj in defs_por_variavel[var_def]:
                    if d_obj.bloco_num == bloco.numero:
                        defs_locais[var_def] = d_obj
        bloco.gen_rd = set(defs_locais.values())
        for def_gerada in bloco.gen_rd:
            outras_defs = defs_por_variavel[def_gerada.var] - {def_gerada}
            bloco.kill_rd.update(outras_defs)

def analisar_definicoes_alcancantes(blocos):
    """
    Executa o algoritmo iterativo de análise para a frente.
    """
    alterou = True
    while alterou:
        alterou = False
        for num_bloco in sorted(blocos.keys()):
            bloco = blocos[num_bloco]

            in_set = set()
            for p_num in bloco.predecessores:
                in_set.update(blocos[p_num].out_rd)

            out_antigo = bloco.out_rd
            bloco.in_rd = in_set
            bloco.out_rd = bloco.gen_rd.union(bloco.in_rd - bloco.kill_rd)

            if bloco.out_rd != out_antigo:
                alterou = True

def ler_entrada_e_construir_grafo(dados_entrada):
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
        bloco.instrucoes = [linhas[j].strip() for j in range(i, i + qtd_instrucoes)]
        i += qtd_instrucoes
        bloco.sucessores = [int(s) for s in linhas[i].split() if s != '0']
        i += 1
        blocos[num_bloco] = bloco

    # Preencher predecessores
    for bloco in blocos.values():
        for suc_num in bloco.sucessores:
            if suc_num in blocos:
                blocos[suc_num].predecessores.append(bloco.numero)
    return blocos

def main():
    PASTA_ENTRADA = os.path.join("..", "in")
    PASTA_SAIDA = "out"
    if not os.path.isdir(PASTA_ENTRADA):
        print(f"Erro: Pasta '{PASTA_ENTRADA}' não encontrada.")
        return
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    for nome_ficheiro in os.listdir(PASTA_ENTRADA):
        caminho_entrada = os.path.join(PASTA_ENTRADA, nome_ficheiro)
        nome_saida = os.path.splitext(nome_ficheiro)[0] + "_rd.txt"
        caminho_saida = os.path.join(PASTA_SAIDA, nome_saida)

        with open(caminho_entrada, 'r', encoding='utf-8') as f:
            dados_entrada = f.read()

        blocos = ler_entrada_e_construir_grafo(dados_entrada)
        _, defs_por_variavel = pre_processar_definicoes(blocos)
        calcular_gen_kill_rd(blocos, defs_por_variavel)
        analisar_definicoes_alcancantes(blocos)

        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write("Resultado das Definições Alcançantes:\n")
            for num_bloco in sorted(blocos.keys()):
                bloco = blocos[num_bloco]
                in_str = sorted([d.id for d in bloco.in_rd])
                out_str = sorted([d.id for d in bloco.out_rd])
                f.write(f"IN[{bloco.numero}] = {in_str}\n")
                f.write(f"OUT[{bloco.numero}] = {out_str}\n")
                f.write("--------------------\n")

        print(f"Análise de '{caminho_entrada}' salva em '{caminho_saida}'")

if __name__ == "__main__":
    main()
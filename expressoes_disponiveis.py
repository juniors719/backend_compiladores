import re
import os

class BlocoBasico:
    """
    Representa um bloco básico no grafo de fluxo de controle.
    """
    def __init__(self, numero):
        self.numero = numero
        self.instrucoes = []
        self.sucessores = []
        self.predecessores = []

        self.gen_ae = set()
        self.kill_ae = set()
        self.in_ae = set()
        self.out_ae = set()

def extrair_partes_instrucao(instrucao):
    """
    Extrai a variável definida e a expressão do lado direito.
    """
    if '=' in instrucao:
        definida, lado_dir = instrucao.split('=', 1)
        definida = definida.strip()
        
        op_match = re.search(r'[\+\-\*\/]', lado_dir)
        if op_match:
            expressao = "".join(lado_dir.split())
            return definida, expressao
        
        return definida, None
    return None, None

def pre_processar_expressoes(blocos):
    """Encontra todas as expressões únicas no programa."""
    todas_expressoes = set()
    for bloco in blocos.values():
        for instrucao in bloco.instrucoes:
            _, expressao = extrair_partes_instrucao(instrucao)
            if expressao:
                todas_expressoes.add(expressao)
    return todas_expressoes

def calcular_gen_kill_ae(blocos, todas_expressoes):
    """
    Calcula os conjuntos gen e kill para cada bloco.
    """
    for bloco in blocos.values():
        disponibilidade_local = set()
        for instrucao in bloco.instrucoes:
            definida, expressao = extrair_partes_instrucao(instrucao)
            if definida:
                exp_a_remover = {expr for expr in disponibilidade_local if re.search(r'\b' + re.escape(definida) + r'\b', expr)}
                disponibilidade_local -= exp_a_remover
            if expressao:
                operandos = re.findall(r'[a-zA-Z_]\w*', expressao)
                if definida not in operandos:
                    disponibilidade_local.add(expressao)
        bloco.gen_ae = disponibilidade_local
        defs_deste_bloco = {p[0] for p in [extrair_partes_instrucao(i) for i in bloco.instrucoes] if p[0]}
        for expr in todas_expressoes:
            operandos_expr = re.findall(r'[a-zA-Z_]\w*', expr)
            if any(op in defs_deste_bloco for op in operandos_expr):
                bloco.kill_ae.add(expr)

def analisar_expressoes_disponiveis(blocos, todas_expressoes):
    for bloco in blocos.values():
        if bloco.predecessores:
             bloco.out_ae = todas_expressoes.copy()
    
    alterou = True
    while alterou:
        alterou = False
        for num_bloco in sorted(blocos.keys()):
            bloco = blocos[num_bloco]
            if not bloco.predecessores:
                in_set = set()
            else:
                in_set = todas_expressoes.copy()
                for p_num in bloco.predecessores:
                    in_set.intersection_update(blocos[p_num].out_ae)
            out_antigo = bloco.out_ae
            bloco.in_ae = in_set
            bloco.out_ae = bloco.gen_ae.union(bloco.in_ae - bloco.kill_ae)
            if bloco.out_ae != out_antigo:
                alterou = True

def ler_entrada_e_construir_grafo(dados_entrada):
    blocos = {}
    linhas = dados_entrada.strip().split('\n')
    i=0
    while i < len(linhas):
        parts = linhas[i].split();
        if not parts: i+=1; continue
        num, n_inst = int(parts[0]), int(parts[1]); i+=1
        bloco = BlocoBasico(num)
        bloco.instrucoes = [l.strip() for l in linhas[i:i+n_inst]]; i+=n_inst
        bloco.sucessores = [int(s) for s in linhas[i].split() if s != '0']; i+=1
        blocos[num] = bloco
    for num, bloco in blocos.items():
        for suc in bloco.sucessores:
            if suc in blocos: blocos[suc].predecessores.append(num)
    return blocos

def main():
    PASTA_ENTRADA = "in"
    PASTA_SAIDA = "out"
    if not os.path.isdir(PASTA_ENTRADA):
        print(f"Erro: Pasta '{PASTA_ENTRADA}' não encontrada."); return
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    for nome_ficheiro in os.listdir(PASTA_ENTRADA):
        caminho_entrada = os.path.join(PASTA_ENTRADA, nome_ficheiro)
        nome_saida = os.path.splitext(nome_ficheiro)[0] + "_ae.txt"
        caminho_saida = os.path.join(PASTA_SAIDA, nome_saida)
        with open(caminho_entrada, 'r', encoding='utf-8') as f: dados_entrada = f.read()

        blocos = ler_entrada_e_construir_grafo(dados_entrada)
        todas_expressoes = pre_processar_expressoes(blocos)
        calcular_gen_kill_ae(blocos, todas_expressoes)
        analisar_expressoes_disponiveis(blocos, todas_expressoes)

        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write("Resultado das Expressões Disponíveis:\n")
            for num_bloco in sorted(blocos.keys()):
                bloco = blocos[num_bloco]
                in_str = sorted(bloco.in_ae)
                out_str = sorted(bloco.out_ae)
                f.write(f"IN[{bloco.numero}] = {in_str}\n")
                f.write(f"OUT[{bloco.numero}] = {out_str}\n")
                f.write("--------------------\n")
        print(f"Análise de '{caminho_entrada}' salva em '{caminho_saida}'")

if __name__ == "__main__":
    main()
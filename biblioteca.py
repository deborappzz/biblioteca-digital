"""
Sistema de Gerenciamento de Biblioteca Digital
PUCPR - Programação para Ciência de Dados - Hora da Prática 2

Funcionalidades:
    - Listar documentos por tipo e ano de publicação
    - Adicionar novos documentos ao repositório
    - Renomear documentos existentes
    - Remover documentos
    - Criar e remover diretórios
"""

import argparse
import os
import shutil
from collections import defaultdict
from pathlib import Path

# Diretório raiz onde os documentos ficam armazenados
DIRETORIO_BASE = Path("documentos")

# Tipos de arquivo aceitos pelo sistema
TIPOS_SUPORTADOS = {".pdf", ".epub", ".docx", ".txt", ".mobi"}


def inicializar_repositorio():
    """Cria a estrutura base de diretórios caso ainda não exista."""
    DIRETORIO_BASE.mkdir(exist_ok=True)
    print(f"Repositório inicializado em: {DIRETORIO_BASE.resolve()}")


def listar_documentos(tipo=None, ano=None):
    """
    Lista os documentos do repositório, organizados por tipo e ano.

    Parâmetros:
        tipo (str): Filtra por extensão de arquivo (ex: 'pdf', 'epub').
        ano  (str): Filtra por ano de publicação (ex: '2023').

    Retorna:
        dict: Estrutura { tipo: { ano: [nomes] } } com os documentos encontrados.
    """
    if not DIRETORIO_BASE.exists():
        print("Repositório não encontrado. Execute 'inicializar' primeiro.")
        return {}

    # Dicionário aninhado: tipo → ano → lista de nomes
    documentos = defaultdict(lambda: defaultdict(list))
    total = 0

    for arquivo in DIRETORIO_BASE.rglob("*"):
        if not arquivo.is_file():
            continue

        extensao = arquivo.suffix.lower()
        partes = arquivo.relative_to(DIRETORIO_BASE).parts

        # Estrutura esperada: documentos/<tipo>/<ano>/arquivo
        ano_arquivo = partes[1] if len(partes) >= 3 else "sem_ano"
        tipo_arquivo = extensao.lstrip(".")

        # Aplica os filtros opcionais
        if tipo and tipo_arquivo != tipo.lower().lstrip("."):
            continue
        if ano and ano_arquivo != ano:
            continue

        # Calcula tamanho em KB para exibição (feedback dos bibliotecários)
        tamanho_kb = round(arquivo.stat().st_size / 1024, 1)
        documentos[tipo_arquivo][ano_arquivo].append((arquivo.name, tamanho_kb))
        total += 1

    if not total:
        print("Nenhum documento encontrado com os filtros aplicados.")
        return documentos

    print(f"\n{'=' * 55}")
    print(f"  BIBLIOTECA DIGITAL  —  {total} documento(s) encontrado(s)")
    print(f"{'=' * 55}")

    for tipo_doc, anos in sorted(documentos.items()):
        print(f"\n[{tipo_doc.upper()}]")
        for ano_doc, arquivos in sorted(anos.items()):
            print(f"  {ano_doc}:")
            for nome, tamanho in sorted(arquivos):
                print(f"    - {nome}  ({tamanho} KB)")

    return documentos


def adicionar_documento(caminho_origem, ano):
    """
    Copia um documento para o repositório na pasta correta (tipo/ano).

    Parâmetros:
        caminho_origem (str): Caminho do arquivo a ser adicionado.
        ano            (str): Ano de publicação usado para organizar o arquivo.

    Retorna:
        bool: True se o documento foi adicionado com sucesso, False caso contrário.
    """
    origem = Path(caminho_origem)

    if not origem.exists():
        print(f"Erro: arquivo '{caminho_origem}' não encontrado.")
        return False

    extensao = origem.suffix.lower()

    if extensao not in TIPOS_SUPORTADOS:
        print(f"Erro: tipo '{extensao}' não é suportado.")
        print(f"Tipos aceitos: {', '.join(sorted(TIPOS_SUPORTADOS))}")
        return False

    # Monta o caminho de destino: documentos/<tipo>/<ano>/
    tipo_pasta = extensao.lstrip(".")
    destino_dir = DIRETORIO_BASE / tipo_pasta / str(ano)
    destino_dir.mkdir(parents=True, exist_ok=True)

    destino = destino_dir / origem.name

    if destino.exists():
        print(f"Aviso: '{origem.name}' já existe no repositório.")
        return False

    shutil.copy2(origem, destino)
    print(f"Documento adicionado: {destino.relative_to(DIRETORIO_BASE)}")
    return True


def renomear_documento(nome_antigo, nome_novo):
    """
    Renomeia um documento dentro do repositório.

    Parâmetros:
        nome_antigo (str): Nome atual do arquivo.
        nome_novo   (str): Novo nome para o arquivo.

    Retorna:
        bool: True se renomeado com sucesso, False caso contrário.
    """
    encontrados = list(DIRETORIO_BASE.rglob(nome_antigo))

    if not encontrados:
        print(f"Erro: documento '{nome_antigo}' não encontrado.")
        return False

    if len(encontrados) > 1:
        print(f"Aviso: múltiplos arquivos com o nome '{nome_antigo}':")
        for f in encontrados:
            print(f"  - {f.relative_to(DIRETORIO_BASE)}")
        print("Use o caminho completo para ser mais específico.")
        return False

    arquivo = encontrados[0]
    novo_caminho = arquivo.parent / nome_novo

    if novo_caminho.exists():
        print(f"Erro: já existe um arquivo chamado '{nome_novo}' na mesma pasta.")
        return False

    arquivo.rename(novo_caminho)
    print(f"Documento renomeado: '{nome_antigo}'  ->  '{nome_novo}'")
    return True


def remover_documento(nome_arquivo):
    """
    Remove um documento do repositório após confirmação do usuário.

    Parâmetros:
        nome_arquivo (str): Nome do arquivo a ser removido.

    Retorna:
        bool: True se removido com sucesso, False caso contrário.
    """
    encontrados = list(DIRETORIO_BASE.rglob(nome_arquivo))

    if not encontrados:
        print(f"Erro: documento '{nome_arquivo}' não encontrado.")
        return False

    if len(encontrados) > 1:
        print(f"Aviso: múltiplos arquivos com o nome '{nome_arquivo}':")
        for f in encontrados:
            print(f"  - {f.relative_to(DIRETORIO_BASE)}")
        print("Use o caminho completo para ser mais específico.")
        return False

    arquivo = encontrados[0]

    # Exibe o caminho completo antes da confirmação (feedback dos bibliotecários)
    caminho_relativo = arquivo.relative_to(DIRETORIO_BASE)
    confirmacao = input(f"Confirmar remoção de '{caminho_relativo}'? (s/n): ")

    if confirmacao.strip().lower() != "s":
        print("Remoção cancelada.")
        return False

    arquivo.unlink()
    print(f"Documento removido: '{nome_arquivo}'")
    return True


def criar_diretorio(caminho):
    """
    Cria um novo diretório dentro do repositório.

    Parâmetros:
        caminho (str): Caminho relativo a ser criado (ex: 'mobi/2025').

    Retorna:
        bool: True se criado com sucesso, False caso contrário.
    """
    novo_dir = DIRETORIO_BASE / caminho

    if novo_dir.exists():
        print(f"Aviso: o diretório '{caminho}' já existe.")
        return False

    novo_dir.mkdir(parents=True)
    print(f"Diretório criado: {novo_dir.relative_to(DIRETORIO_BASE)}")
    return True


def remover_diretorio(caminho):
    """
    Remove um diretório do repositório (com confirmação se não estiver vazio).

    Parâmetros:
        caminho (str): Caminho relativo do diretório a remover.

    Retorna:
        bool: True se removido com sucesso, False caso contrário.
    """
    alvo = DIRETORIO_BASE / caminho

    if not alvo.exists():
        print(f"Erro: diretório '{caminho}' não encontrado.")
        return False

    if any(alvo.iterdir()):
        confirmacao = input(
            f"O diretório '{caminho}' não está vazio. Remover mesmo assim? (s/n): "
        )
        if confirmacao.strip().lower() != "s":
            print("Remoção cancelada.")
            return False
        shutil.rmtree(alvo)
    else:
        alvo.rmdir()

    print(f"Diretório removido: '{caminho}'")
    return True


def configurar_cli():
    """Configura e retorna o parser de argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        prog="biblioteca",
        description="Sistema de Gerenciamento de Biblioteca Digital — PUCPR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python biblioteca.py inicializar
  python biblioteca.py listar
  python biblioteca.py listar --tipo pdf
  python biblioteca.py listar --ano 2023
  python biblioteca.py listar --tipo epub --ano 2022
  python biblioteca.py adicionar artigo.pdf --ano 2023
  python biblioteca.py renomear artigo.pdf artigo_v2.pdf
  python biblioteca.py remover artigo.pdf
  python biblioteca.py criar-dir mobi/2025
  python biblioteca.py remover-dir mobi/2021
        """,
    )

    subparsers = parser.add_subparsers(dest="comando", help="Comando disponível")

    # inicializar
    subparsers.add_parser(
        "inicializar",
        help="Inicializa o repositório de documentos"
    )

    # listar
    p_listar = subparsers.add_parser(
        "listar",
        help="Lista os documentos do repositório"
    )
    p_listar.add_argument(
        "--tipo",
        help="Filtrar por tipo de arquivo (pdf, epub, docx...)",
        default=None,
    )
    p_listar.add_argument(
        "--ano",
        help="Filtrar por ano de publicação",
        default=None,
    )

    # adicionar
    p_adicionar = subparsers.add_parser(
        "adicionar",
        help="Adiciona um documento ao repositório"
    )
    p_adicionar.add_argument("arquivo", help="Caminho do arquivo a adicionar")
    p_adicionar.add_argument("--ano", help="Ano de publicação", required=True)

    # renomear
    p_renomear = subparsers.add_parser(
        "renomear",
        help="Renomeia um documento no repositório"
    )
    p_renomear.add_argument("nome_antigo", help="Nome atual do arquivo")
    p_renomear.add_argument("nome_novo", help="Novo nome do arquivo")

    # remover
    p_remover = subparsers.add_parser(
        "remover",
        help="Remove um documento do repositório"
    )
    p_remover.add_argument("arquivo", help="Nome do arquivo a remover")

    # criar-dir
    p_criar_dir = subparsers.add_parser(
        "criar-dir",
        help="Cria um diretório no repositório"
    )
    p_criar_dir.add_argument("caminho", help="Caminho do diretório (ex: mobi/2025)")

    # remover-dir
    p_remover_dir = subparsers.add_parser(
        "remover-dir",
        help="Remove um diretório do repositório"
    )
    p_remover_dir.add_argument("caminho", help="Caminho do diretório a remover")

    return parser


def main():
    """Ponto de entrada principal: interpreta os argumentos e chama a função correta."""
    parser = configurar_cli()
    args = parser.parse_args()

    if not args.comando:
        parser.print_help()
        return

    comandos = {
        "inicializar": lambda: inicializar_repositorio(),
        "listar": lambda: listar_documentos(tipo=args.tipo, ano=args.ano),
        "adicionar": lambda: adicionar_documento(args.arquivo, args.ano),
        "renomear": lambda: renomear_documento(args.nome_antigo, args.nome_novo),
        "remover": lambda: remover_documento(args.arquivo),
        "criar-dir": lambda: criar_diretorio(args.caminho),
        "remover-dir": lambda: remover_diretorio(args.caminho),
    }

    comandos[args.comando]()


if __name__ == "__main__":
    main()

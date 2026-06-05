# Biblioteca Digital — Sistema de Gerenciamento

Sistema de gerenciamento de documentos digitais desenvolvido em Python para a Biblioteca Universitária da PUCPR.

Permite que bibliotecários listem, adicionem, renomeiem e removam documentos diretamente pela linha de comando, organizando-os automaticamente por tipo de arquivo e ano de publicação.

---

## Funcionalidades

| Funcionalidade | Comando |
|---|---|
| Inicializar repositório | `inicializar` |
| Listar documentos | `listar` |
| Filtrar por tipo | `listar --tipo pdf` |
| Filtrar por ano | `listar --ano 2023` |
| Adicionar documento | `adicionar` |
| Renomear documento | `renomear` |
| Remover documento | `remover` |
| Criar diretório | `criar-dir` |
| Remover diretório | `remover-dir` |

---

## Estrutura do Projeto

```
biblioteca-digital/
├── biblioteca.py            # Sistema principal (CLI)
├── tests/
│   └── test_biblioteca.py   # Testes automatizados
├── documentos/              # Repositório de documentos
│   ├── pdf/
│   │   ├── 2022/
│   │   ├── 2023/
│   │   └── 2024/
│   ├── epub/
│   │   ├── 2022/
│   │   └── 2023/
│   └── docx/
│       └── 2024/
├── README.md
├── CONTRIBUTING.md
└── RELATORIO_TESTES.md
```

---

## Pré-requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa necessária (apenas módulos da stdlib)

---

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/biblioteca-digital.git

# 2. Acesse o diretório
cd biblioteca-digital

# 3. Inicialize o repositório de documentos
python biblioteca.py inicializar
```

---

## Uso

### Listar documentos

```bash
# Todos os documentos
python biblioteca.py listar

# Apenas PDFs
python biblioteca.py listar --tipo pdf

# Apenas documentos de 2023
python biblioteca.py listar --ano 2023

# PDFs de 2023
python biblioteca.py listar --tipo pdf --ano 2023
```

**Saída esperada:**
```
=======================================================
  BIBLIOTECA DIGITAL  —  3 documento(s) encontrado(s)
=======================================================

[PDF]
  2023:
    - artigo_ia.pdf  (12.4 KB)
    - tese_redes.pdf  (8.1 KB)
  2024:
    - livro_python.pdf  (20.0 KB)
```

### Adicionar documento

```bash
python biblioteca.py adicionar caminho/para/artigo.pdf --ano 2024
```

O arquivo é copiado automaticamente para `documentos/pdf/2024/`.

### Renomear documento

```bash
python biblioteca.py renomear artigo_ia.pdf artigo_inteligencia_artificial.pdf
```

### Remover documento

```bash
python biblioteca.py remover artigo.pdf
```

O sistema pede confirmação antes de remover, exibindo o caminho completo do arquivo.

### Gerenciar diretórios

```bash
# Criar pasta para novo formato/ano
python biblioteca.py criar-dir mobi/2025

# Remover pasta vazia (ou com confirmação se tiver arquivos)
python biblioteca.py remover-dir epub/2021
```

---

## Executar Testes

```bash
# Com unittest (nativo do Python)
python -m unittest tests/test_biblioteca.py -v

# Com pytest (se instalado)
pip install pytest
pytest tests/ -v
```

---

## Tipos de Arquivo Suportados

| Extensão | Formato |
|---|---|
| `.pdf` | Portable Document Format |
| `.epub` | Electronic Publication |
| `.docx` | Microsoft Word |
| `.txt` | Texto simples |
| `.mobi` | Formato Kindle |

---

## Organização dos Arquivos

Os documentos são armazenados seguindo a estrutura:

```
documentos/<tipo>/<ano>/<nome_do_arquivo>
```

**Exemplo:**
```
documentos/pdf/2023/artigo_machine_learning.pdf
documentos/epub/2022/introducao_dados.epub
```

---

## Autor

**Débora Pizzolatto Pacassa**  
PUCPR — Programação para Ciência de Dados — 2025

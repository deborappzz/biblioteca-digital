# Relatório de Testes e Feedback

**Projeto:** Sistema de Gerenciamento de Biblioteca Digital  
**Disciplina:** Programação para Ciência de Dados — PUCPR  
**Autora:** Débora Pizzolatto Pacassa  
**Data:** 2025-06-05  
**Versão:** 1.0.0  

---

## 1. Testes Automatizados

Os testes foram escritos com o módulo `unittest` da biblioteca padrão do Python e executados com o comando:

```bash
python -m unittest tests/test_biblioteca.py -v
```

### Resultado

```
test_adicionar_arquivo_inexistente ... ok
test_adicionar_documento_duplicado ... ok
test_adicionar_documento_pdf_valido ... ok
test_adicionar_tipo_nao_suportado ... ok
test_criar_diretorio_ja_existente ... ok
test_criar_diretorio_novo ... ok
test_listar_filtro_por_ano ... ok
test_listar_filtro_por_tipo_pdf ... ok
test_listar_repositorio_vazio ... ok
test_listar_sem_repositorio ... ok
test_listar_todos_os_documentos ... ok
test_remover_diretorio_com_arquivos_confirmado ... ok
test_remover_diretorio_inexistente ... ok
test_remover_diretorio_vazio ... ok
test_remover_documento_cancelado ... ok
test_remover_documento_confirmado ... ok
test_remover_documento_inexistente ... ok
test_renomear_documento_existente ... ok
test_renomear_documento_inexistente ... ok
test_renomear_para_nome_ja_existente ... ok

----------------------------------------------------------------------
Ran 20 tests in 0.015s

OK
```

**Taxa de sucesso: 20/20 testes — 100%**

---

## 2. Detalhamento por Funcionalidade

### `listar_documentos()`

| Cenário de teste | Resultado |
|---|---|
| Listar todos os documentos (6 arquivos de exemplo) | PASSOU |
| Filtrar apenas PDFs | PASSOU |
| Filtrar por ano 2023 | PASSOU |
| Repositório vazio (pasta existe, sem arquivos) | PASSOU |
| Repositório inexistente (pasta não existe) | PASSOU |

### `adicionar_documento()`

| Cenário de teste | Resultado |
|---|---|
| Adicionar PDF válido para ano 2024 | PASSOU |
| Tentar adicionar arquivo que não existe | PASSOU |
| Tentar adicionar extensão não suportada (.mp4) | PASSOU |
| Tentar adicionar arquivo duplicado | PASSOU |

### `renomear_documento()`

| Cenário de teste | Resultado |
|---|---|
| Renomear documento existente com sucesso | PASSOU |
| Renomear arquivo inexistente | PASSOU |
| Renomear para nome que já está em uso | PASSOU |

### `remover_documento()`

| Cenário de teste | Resultado |
|---|---|
| Remover com confirmação do usuário (s) | PASSOU |
| Cancelar remoção (n) | PASSOU |
| Tentar remover arquivo inexistente | PASSOU |

### `criar_diretorio()`

| Cenário de teste | Resultado |
|---|---|
| Criar diretório novo (mobi/2025) | PASSOU |
| Tentar criar diretório já existente | PASSOU |

### `remover_diretorio()`

| Cenário de teste | Resultado |
|---|---|
| Remover diretório vazio | PASSOU |
| Tentar remover diretório inexistente | PASSOU |
| Remover diretório com arquivos (com confirmação) | PASSOU |

---

## 3. Testes Manuais (Linha de Comando)

Testes realizados simulando o uso real do sistema:

| Ação | Comando executado | Resultado |
|---|---|---|
| Inicializar repositório | `python biblioteca.py inicializar` | Pasta `documentos/` criada |
| Listar sem documentos | `python biblioteca.py listar` | Mensagem amigável exibida |
| Adicionar artigo.pdf | `python biblioteca.py adicionar artigo.pdf --ano 2023` | Arquivo copiado para `pdf/2023/` |
| Listar após adição | `python biblioteca.py listar` | Arquivo aparece com tamanho em KB |
| Filtrar por tipo | `python biblioteca.py listar --tipo pdf` | Apenas PDFs listados |
| Filtrar por ano | `python biblioteca.py listar --ano 2023` | Apenas documentos de 2023 |
| Renomear documento | `python biblioteca.py renomear artigo.pdf artigo_v2.pdf` | Renomeado com sucesso |
| Remover (confirmar) | `python biblioteca.py remover artigo_v2.pdf` + `s` | Arquivo removido |
| Remover (cancelar) | `python biblioteca.py remover artigo_v2.pdf` + `n` | Arquivo mantido |
| Criar diretório | `python biblioteca.py criar-dir mobi/2025` | Pasta criada |
| Remover diretório | `python biblioteca.py remover-dir mobi/2025` | Pasta removida |
| Ajuda geral | `python biblioteca.py --help` | Todos os comandos listados |

---

## 4. Feedback dos Bibliotecários

O sistema foi apresentado a dois bibliotecários da biblioteca universitária para avaliação prática de usabilidade.

---

### Bibliotecário 1

**Cargo:** Chefe do Setor de Documentação Digital  
**Contexto:** Avaliou o sistema realizando operações reais com arquivos do acervo.

**Feedback recebido:**
> "O sistema funcionou bem e foi fácil de usar. Consegui listar, adicionar e remover arquivos sem dificuldades. Uma coisa que senti falta: ao listar os documentos, seria útil saber o tamanho de cada arquivo para verificar se o upload foi feito corretamente antes de distribuir para os estudantes."

---

### Bibliotecário 2

**Cargo:** Auxiliar de Biblioteca — Setor de Teses e Artigos  
**Contexto:** Testou especialmente as operações de remoção e renomeação.

**Feedback recebido:**
> "A confirmação antes de remover foi uma boa escolha, previne acidentes. Mas quando aparece 'Confirmar remoção de artigo.pdf?', não sei se é o arquivo certo se tiver vários com nomes parecidos. Seria melhor mostrar o caminho completo, tipo em qual pasta ele está."

---

## 5. Ajustes Realizados com Base no Feedback

| Feedback | Problema identificado | Solução implementada |
|---|---|---|
| Exibir tamanho dos arquivos na listagem | A listagem mostrava apenas o nome dos arquivos, sem informação de tamanho | Adicionado cálculo de tamanho em KB via `arquivo.stat().st_size` na função `listar_documentos()`. Exibição: `artigo.pdf  (12.4 KB)` |
| Mostrar caminho completo na confirmação de remoção | A mensagem exibia apenas o nome do arquivo, sem indicar em qual pasta estava | A confirmação passou a exibir o caminho relativo completo: `Confirmar remoção de 'pdf/2023/artigo.pdf'? (s/n):` |

---

## 6. Conclusão

O sistema atende a todos os requisitos da atividade:

- Listagem de documentos por tipo e ano de publicação
- Interface de linha de comando funcional para todas as operações
- Tratamento de erros em todos os cenários (arquivo inexistente, duplicado, tipo inválido)
- 20 testes automatizados com 100% de aprovação
- Feedback dos usuários coletado e incorporado ao código
- Documentação completa (README e CONTRIBUTING)

# Guia de Contribuição

Obrigado por querer contribuir com o projeto **Biblioteca Digital**!  
Este guia explica como colaborar corretamente usando Git e GitHub.

---

## Pré-requisitos

- [Git](https://git-scm.com/) instalado
- Python 3.8 ou superior
- Conta no GitHub

---

## Configuração Inicial (apenas na primeira vez)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/biblioteca-digital.git
cd biblioteca-digital

# Configure seu nome e e-mail
git config user.name "Seu Nome"
git config user.email "seu@email.com"
```

---

## Fluxo de Trabalho

### 1. Criar uma Branch

Nunca trabalhe diretamente na branch `main`. Crie uma branch para cada funcionalidade ou correção:

```bash
git checkout -b feat/nome-da-funcionalidade
```

**Convenção de nomes para branches:**

| Prefixo | Uso |
|---|---|
| `feat/` | Nova funcionalidade |
| `fix/` | Correção de bug |
| `docs/` | Atualização de documentação |
| `test/` | Novos testes ou correção de testes |
| `refactor/` | Refatoração sem mudança de comportamento |

**Exemplos:**
```
feat/filtro-por-tamanho
fix/erro-renomear-duplicado
docs/atualiza-readme
```

---

### 2. Fazer Commits

Commits devem ser pequenos, focados e ter mensagens claras. Use o padrão:

```
<tipo>: <mensagem curta descrevendo o que foi feito>
```

**Exemplos de commits corretos:**
```bash
git commit -m "feat: adiciona filtro por tamanho de arquivo na listagem"
git commit -m "fix: corrige erro ao renomear arquivo com nome duplicado"
git commit -m "docs: atualiza exemplos de uso no README"
git commit -m "test: adiciona teste para remoção de diretório com arquivos"
git commit -m "refactor: extrai lógica de busca para função auxiliar"
```

**Commits ruins (evitar):**
```bash
git commit -m "ajustes"          # vago demais
git commit -m "wip"              # não descreve nada
git commit -m "corrigindo coisas" # não é específico
```

---

### 3. Enviar para o GitHub (Push)

```bash
git push origin feat/nome-da-funcionalidade
```

---

### 4. Abrir um Pull Request

1. Acesse o repositório no GitHub
2. Clique em **"Compare & pull request"** (aparece automaticamente após o push)
3. Preencha:
   - **Título:** descreve o que foi feito (ex: `feat: adiciona filtro por tamanho`)
   - **Descrição:** explica o motivo da mudança e como testar
4. Clique em **"Create pull request"**

---

### 5. Revisão e Merge

- Aguarde a revisão do mantenedor
- Responda aos comentários e faça os ajustes solicitados
- Após aprovação, o merge será realizado pelo mantenedor

---

## Padrões de Código

- Seguir **PEP 8** (guia de estilo oficial do Python)
- Documentar todas as funções com **docstrings**
- Nomes de variáveis e funções em **português** (manter consistência com o projeto)
- Toda nova funcionalidade deve ter **testes automatizados** correspondentes

---

## Executar Testes Antes de Enviar

```bash
python -m unittest tests/test_biblioteca.py -v
```

Todos os testes devem passar antes de abrir um Pull Request.

---

## Reportar Problemas (Issues)

Encontrou um bug ou tem uma sugestão? Abra uma [Issue](https://github.com/seu-usuario/biblioteca-digital/issues) incluindo:

- Descrição clara do problema ou sugestão
- Comportamento esperado vs. comportamento observado
- Passos para reproduzir o problema
- Versão do Python utilizada (`python --version`)

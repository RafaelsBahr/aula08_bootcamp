# Desafios — Aula 08 (ETL com Pandas, JSON e Parquet)

> Prática **graduada**: faça um exercício por vez, na ordem. Cada um treina UMA peça da aula.
>
> **Regras (combinadas com o Rafael):**
> - Tente sozinho primeiro. Se travar, consulte os cadernos ou peça **uma dica** — não a solução pronta.
> - Cadernos de apoio: `Jornada de dados.md` (Python) e `Engenharia de Dados na Prática.md` (ETL/pandas).
> - Cada exercício tem: **Objetivo**, **Dica** (direção, não solução) e **Saída esperada** (para você conferir).
>
> **Dados:** pasta `data/` — 3 arquivos JSON de vendas, 3 registros cada (**9 linhas no total**).

---

## Exercício 0 — Preparar o ambiente

**Objetivo:** ter as bibliotecas instaladas e um arquivo `.py` para escrever.

**Dica:** num projeto com poetry, `poetry add pandas pandera fastparquet loguru`. Depois crie um arquivo (ex.: `solucao.py`) e teste `import pandas as pd`.

**Saída esperada:** o `import pandas as pd` roda sem erro.

---

## Exercício 1 — Ler UM JSON num DataFrame  (fácil)

**Objetivo:** ler `data/coleta_dia01.json` para um DataFrame e dar `print` nele.

**Dica:** existe uma função da família `pd.read_...` para JSON. Passe o caminho do arquivo.

**Saída esperada:** uma tabela com **3 linhas** (Notebook Gamer, Mouse Sem Fio, Teclado Mecânico) e as colunas `Produto, Categoria, Quantidade, Venda, Data`.

---

## Exercício 2 — Achar e juntar os 3 JSONs

**Objetivo:** descobrir automaticamente todos os `.json` da pasta `data/`, ler cada um e juntar tudo num DataFrame só.

**Dica:** três passos — (1) `glob.glob(os.path.join("data", "*.json"))` para a lista de caminhos; (2) uma **list comprehension** lendo cada caminho com `pd.read_json`; (3) `pd.concat(lista, ignore_index=True)` para empilhar.

**Saída esperada:** um DataFrame com **9 linhas**, índice de `0` a `8` (sem índices repetidos).

> Por que `ignore_index=True`? Releia "concat" no caderno de Engenharia de Dados.

---

## Exercício 3 — Criar a coluna Receita

**Objetivo:** adicionar uma coluna `Receita` = `Quantidade` × `Venda` (em cada linha).

**Dica:** no pandas você opera colunas inteiras de uma vez: `df["nova"] = df["a"] * df["b"]`.

**Saída esperada:** nova coluna `Receita`. Confira: Notebook Gamer do dia01 (3 × 1500) = **4500**; Mouse Sem Fio (10 × 30) = **300**.

---

## Exercício 4 — Salvar em CSV e Parquet

**Objetivo:** gravar o DataFrame final em `dados.csv` e `dados.parquet`, **sem** a coluna de índice.

**Dica:** são **métodos** do DataFrame (`df.to_...`), não funções do `pd`. Lembre do parâmetro que remove o índice.

**Saída esperada:** dois arquivos criados na pasta. Abra o `dados.csv`: primeira linha é o cabeçalho (terminando em `Receita`), depois 9 linhas. O `.parquet` não abre no bloco de notas (é binário) — normal.

---

## Exercício 5 — Organizar em funções (extrair / transformar / carregar / pipeline)

**Objetivo:** refatorar tudo que você fez em **três funções** + uma função `pipeline` que chama as três em ordem. Use **type hints**.

**Dica:** assinaturas no estilo:
`def extrair_dados(pasta: str) -> pd.DataFrame:` /
`def transformar_dados(df: pd.DataFrame) -> pd.DataFrame:` /
`def carregar_dados(df: pd.DataFrame, formatos: list):`.
A `pipeline` passa o resultado de uma para a próxima (lembre do papel do `return`).

**Saída esperada:** chamar `pipeline("data", ["csv"])` gera o mesmo `dados.csv` do Exercício 4.

---

## Exercício 6 — Decorador de log com Loguru

**Objetivo:** escrever um decorador `log_decorator` que registra quando uma função é chamada e o que ela retorna, e aplicá-lo nas suas funções com `@`.

**Dica:** a estrutura é `def log_decorator(func): def wrapper(*args, **kwargs): ...; return wrapper`. Dentro do wrapper: logue antes, chame `func(*args, **kwargs)`, logue depois, e `return` o resultado. Use `from loguru import logger` e `func.__name__` para o nome da função. (Ver "Decoradores" no caderno Python e "Decorador de log" no de Eng. de Dados.)

**Saída esperada:** ao rodar o pipeline, aparecem logs tipo `Chamando 'extrair_dados' ...` e `'extrair_dados' retornou ...`.

---

## Exercício 7 — Validação com Pandera  (difícil)

**Objetivo:** criar um `VendasSchema` descrevendo as colunas esperadas e validar a saída de `extrair_dados` com `@pa.check_output(VendasSchema)`.

**Dica:** o schema é uma **classe** que herda de `pa.DataFrameModel` (nome novo; o curso usa o antigo `SchemaModel`). Cada coluna é `Nome: Series[tipo]`; regras de valor com `pa.Field(ge=0)`; e um bloco `class Config: coerce = True / strict = True`. Importe `from pandera.typing import Series`.

**Saída esperada:** com os dados bons, roda sem erro. 

**Desafio de verdade:** edite um JSON e coloque uma `Venda` negativa (ex.: `-50`). Rode de novo — a validação deve **falhar** com um erro do Pandera apontando a regra `ge=0`. Depois desfaça a alteração.

---

## Quando terminar os 7

Você terá reconstruído a ETL completa da aula, peça por peça. O próximo passo (combinado) é **reconstruir do zero**, agora sem o passo a passo — só com um esqueleto de arquivos vazios — para fixar a visão do todo.

> Dúvida em qualquer exercício? Peça **uma dica** ao Claude Code, ou volte ao caderno correspondente. Boa prática! 🚀

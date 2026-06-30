import pandas as pd
import pandera as pa
from pandera.typing import Series
import fastparquet
from loguru import logger
from pathlib import Path

logger.add(Path(__file__).parent / "output" / "pipeline.log", rotation="5 MB")

class VendasSchema(pa.DataFrameModel):    # herda do molde base do Pandera
    Produto: Series[str]
    Categoria: Series[str]
    Quantidade: Series[int] = pa.Field(ge=0)
    Venda: Series[int] = pa.Field(ge=0)
    Data: Series[str]
    class Config:
        coerce = True
        strict = True


def log_decorator(func):
    def wrapper(*args, **kwargs):
        logger.info(f"Chamando '{func.__name__}'")
        try:
            resultado = func(*args, **kwargs)
            logger.info(f"'{func.__name__}' terminou")
            return resultado
        except Exception:
            logger.exception(f"'{func.__name__}' falhou")
            raise
    return wrapper

@log_decorator
@pa.check_output(VendasSchema)
def extrair_dados(pasta: str) -> pd.DataFrame:
    lista_arquivos = pasta.glob('*.json')
    lista_df = [pd.read_json(arquivo) for arquivo in lista_arquivos]
    df = pd.concat(lista_df, ignore_index=True)
    return df

@log_decorator
def transformar_dados(df: pd.DataFrame):
    df["Receita"] = df["Quantidade"] * df["Venda"]
    return df

@log_decorator
def carregar_dados(df: pd.DataFrame):
    pasta_saida = Path(__file__).parent / 'output'
    pasta_saida.mkdir(exist_ok=True)
    df.to_csv(pasta_saida / "dados.csv", index=False)
    df.to_parquet(pasta_saida / "dados.parquet", index=False)

@log_decorator
def pipeline(pasta: str):
    dados = extrair_dados(pasta)
    dados_transformados = transformar_dados(dados)
    carregar_dados(dados_transformados)

if __name__ == "__main__":
    pipeline(Path(__file__).parent / "data")
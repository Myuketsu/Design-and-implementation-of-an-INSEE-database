import pandas as pd
import tomllib

from io import StringIO
from typing import Any

CONFIG_PATH = './data/config.toml'

def load_config(section_name: str) -> dict[str, Any]:
    with open(CONFIG_PATH, 'rb') as config_file:
        return tomllib.load(config_file)[section_name]
    
def select_rename_columns(df: pd.DataFrame, section_config: str) -> pd.DataFrame:
    mapper = load_config(section_config)
    return df.copy()[list(mapper.keys())].rename(columns=mapper)

def DataFrame_to_buffer(df: pd.DataFrame) -> StringIO:
    buffer = StringIO()

    df.to_csv(
        path_or_buf=buffer,
        header=True,
        index=False
    )

    buffer.seek(0)
    return buffer

def load_query(file_name: str) -> dict[str, dict[str, Any]]:
    with open(file_name, 'rb') as query_file:
        return tomllib.load(query_file)
    
def population_preprocessing(df: pd.DataFrame, table: str='population') -> pd.DataFrame:
    population_config = load_config(table)

    df = df.copy()[~df['CODGEO'].str.startswith('97')]

    rename_mapper = {key: value for key, value in population_config.items() if isinstance(value, str)}
    df = df[list(population_config.keys())].rename(
        columns=rename_mapper
    )
    
    temp_dfs = []
    statistics_mapper = {key: value for key, value in population_config.items() if isinstance(value, list)}
    nbr_max_params = sum(map(len, statistics_mapper.values()))
    for column, fields in statistics_mapper.items():
        temp_dfs.append(
            pd.DataFrame(
                {name: df[name] for name in rename_mapper.values()} | {
                    'annee_debut': fields[1],
                    'annee_fin': None if len(fields) < nbr_max_params else fields[2],
                    'type_statistique': fields[0],
                    'valeur': df[column]
                }
            )
        )

    return pd.concat(temp_dfs, ignore_index=True)

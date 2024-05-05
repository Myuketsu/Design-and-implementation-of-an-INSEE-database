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
import pandas as pd
import tomllib

from re import finditer
from io import StringIO
from typing import Any

CONFIG_PATH = './data/config.toml'

def load_config(section_name: str) -> dict[str, Any]:
    with open(CONFIG_PATH, 'rb') as config_file:
        return tomllib.load(config_file)[section_name]

def select_and_rename_csv(file_name: str, section_config: str) -> StringIO:
    buffer = StringIO()
    mapper = load_config(section_config)

    pd.read_csv(
        filepath_or_buffer=file_name
    )[list(mapper.keys())].rename(
        columns=mapper
    ).to_csv(
        path_or_buf=buffer,
        header=False,
        index=False
    )

    buffer.seek(0)
    return buffer

def extract_from_file(file_name: str, start: str, end: str) -> list[str]:
    with open(file_name, 'r') as views_file:
        file_as_str = views_file.read()
        starts = [index.start() for index in finditer('CREATE VIEW', file_as_str)]
        ends = [index.end() for index in finditer(';', file_as_str)]
        
    return [file_as_str[start:end] for start, end in zip(starts, ends)]
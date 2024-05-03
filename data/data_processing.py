import pandas as pd
import tomllib

from io import StringIO
from typing import Any

CONFIG_PATH = './data/config.toml'

def load_config(section_name: str) -> dict[str, Any]:
    with open(CONFIG_PATH, 'rb') as config_file:
        return tomllib.load(config_file)[section_name]

def select_and_rename_csv(file_path: str, section_config: str) -> StringIO:
    buffer = StringIO()
    mapper = load_config(section_config)

    pd.read_csv(
        filepath_or_buffer=file_path
    )[list(mapper.keys())].rename(
        columns=mapper
    ).to_csv(
        path_or_buf=buffer,
        header=False,
        index=False
    )

    buffer.seek(0)
    return buffer
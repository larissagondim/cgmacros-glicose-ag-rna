"""
Funções para ler e preparar os dados do CGMacros.

Este arquivo não é executado diretamente: os notebooks importam as funções
daqui. Assim, o pré-processamento, a RNA e o AG usam o mesmo código para 
abrir e tratar os dados, e uma correção feita aqui vale para todos, centralizando
as alterações e modificações sem ter que mudar em vários cantos.

Funções:
- carregar(pid): lê o CSV de um participante, limpa os nomes das colunas
  e converte o horário.
- listar_pids(): devolve os números dos participantes que têm pasta em data/raw.
"""

from pathlib import Path
import pandas as pd

RAW = Path(__file__).resolve().parent.parent / 'data' / 'raw'


def carregar(pid):
    """lê o CSV de um participante, limpa os nomes das colunas e converte o horário."""
    df = pd.read_csv(RAW / f'CGMacros-{pid:03d}' / f'CGMacros-{pid:03d}.csv')
    df.columns = df.columns.str.strip()
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['pid'] = pid
    return df


def listar_pids():
    """lista o número de todos os participantes que têm pasta em data/raw."""
    return sorted(int(p.name.split('-')[1]) for p in RAW.glob('CGMacros-*') if p.is_dir())
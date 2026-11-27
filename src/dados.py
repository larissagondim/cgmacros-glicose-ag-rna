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
- resumo_dia(df): transforma os minutos de um participante em uma linha por dia,
  com a glicose (Dexcom) e o comportamento do dia.
- maior_sequencia(bom): tamanho do maior bloco de dias bons seguidos.
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


def resumo_dia(df):
    """Uma linha por dia: glicose (Dexcom) e comportamento do dia.

    O calendário é completado: uma data sem nenhuma linha no arquivo entra
    com cobertura 0, para que a contagem de dias seguidos não pule o buraco.
    """
    d = df.copy()

    # alguns arquivos não têm essa coluna (ex.: 007); vira vazio em vez de quebrar
    if 'Calories (Activity)' not in d.columns:
        d['Calories (Activity)'] = float('nan')

    d['data'] = d['Timestamp'].dt.normalize()                              # data, sem a hora
    d['hora'] = d['Timestamp'].dt.hour + d['Timestamp'].dt.minute / 60     # 20h48 -> 20.8

    refeicoes = d[d['Meal Type'].notna()]
    g = d.groupby('data')
    glic = g['Dexcom GL']

    dia = pd.DataFrame({
        'cobertura':   glic.count() / 1440,
        'glic_media':  glic.mean(),
        'glic_dp':     glic.std(),
        'glic_pico':   glic.max(),
        'pct_140':     glic.apply(lambda s: (s.dropna() > 140).mean() * 100),
        'carbs':       g['Carbs'].sum(),
        'proteina':    g['Protein'].sum(),
        'gordura':     g['Fat'].sum(),
        'fibra':       g['Fiber'].sum(),
        'n_refeicoes': g['Meal Type'].count(),
        'atividade':   g['Calories (Activity)'].sum(min_count=1),
        'hora_ultima_refeicao': refeicoes.groupby('data')['hora'].max(),
    })

    # completa o calendário: datas sem nenhuma linha entram com cobertura 0
    calendario = pd.date_range(dia.index.min(), dia.index.max(), freq='D')
    dia = dia.reindex(calendario)
    dia['cobertura'] = dia['cobertura'].fillna(0)

    dia['pid'] = df['pid'].iloc[0]
    return dia.rename_axis('data').reset_index()


def maior_sequencia(bom):
    """Tamanho do maior bloco de valores True seguidos (ex.: dias bons em sequência)."""
    grupos = (bom != bom.shift()).cumsum()     # novo grupo cada vez que alterna entre bom e ruim
    return bom.groupby(grupos).sum().max()     # o bloco de True mais longo
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
- carregar_bio(): lê o bio.csv com as colunas usadas no modelo e o grupo clínico.
- tratar_estranhos(dias): limita os carboidratos a 500 g e preenche a atividade
  que falta com a média do próprio participante.
- montar_dataset_rna(dias, n_anteriores): monta os exemplos de treino da rede.
- montar_blocos(dias): os 9 dias seguidos (D1 a D9) de cada participante,
  usados pelo AG e pela avaliação.
- salvar_tabela(df, nome) / carregar_tabela(nome): grava e lê as tabelas
  prontas em data/processed/.
"""

from pathlib import Path
import pandas as pd

RAW = Path(__file__).resolve().parent.parent / 'data' / 'raw'
PROCESSED = Path(__file__).resolve().parent.parent / 'data' / 'processed'


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


def carregar_bio():
    """Lê o bio.csv com as colunas usadas no modelo e cria o grupo clínico.

    Sexo vira número (1 = masculino, 0 = feminino), porque a rede só recebe números.
    O grupo segue os cortes de HbA1c da ADA: < 5,7 saudável, 5,7 a 6,4 pré-diabetes,
    >= 6,5 DM2. Ele serve para analisar os resultados, não como entrada da rede,
    já que a própria HbA1c entra.
    """
    bio = pd.read_csv(RAW / 'bio.csv')
    bio = bio.rename(columns={
        'subject': 'pid',
        'Age': 'idade',
        'BMI': 'imc',
        'A1c PDL (Lab)': 'hba1c',
        'Fasting GLU - PDL (Lab)': 'glicemia_jejum',
    })
    bio['sexo_masc'] = (bio['Gender'] == 'M').astype(int)
    bio['grupo'] = pd.cut(bio['hba1c'], bins=[0, 5.7, 6.5, 100], right=False,
                          labels=['saudável', 'pré-diabetes', 'DM2'])
    return bio[['pid', 'idade', 'sexo_masc', 'imc', 'hba1c', 'glicemia_jejum', 'grupo']]


# variáveis de comportamento do dia (são também os genes do AG)
COMPORTAMENTO = ['carbs', 'proteina', 'gordura', 'fibra', 'atividade', 'hora_ultima_refeicao']

# dados do participante que entram na rede (o grupo fica de fora, porque a HbA1c já entra)
BIO = ['idade', 'sexo_masc', 'imc', 'hba1c', 'glicemia_jejum']

# medidas de glicose dos dias anteriores que entram na rede
GLICOSE = ['glic_media', 'glic_dp', 'glic_pico', 'pct_140']


def tratar_estranhos(dias, teto_carbs=500):
    """Trata os valores estranhos da tabela de dias (precisa da coluna 'bom').

    - Carboidratos acima de `teto_carbs` gramas viram `teto_carbs`. Remover esses
      dias quebraria a sequência de 9 dias de alguns participantes.
    - Atividade vazia num dia bom (Fitbit não registrou) vira a média de atividade
      dos dias bons do mesmo participante.
    """
    d = dias.copy()
    d['carbs'] = d['carbs'].clip(upper=teto_carbs)

    media_ativ = d['atividade'].where(d['bom']).groupby(d['pid']).transform('mean')
    falta = d['bom'] & d['atividade'].isna()
    d.loc[falta, 'atividade'] = media_ativ[falta]
    return d


def montar_dataset_rna(dias, n_anteriores):
    """Monta os exemplos de treino da rede: uma linha por dia bom d.

    Entrada: glicose dos `n_anteriores` dias antes de d + comportamento de d + bio.
    Alvo: glicose média de d ('alvo').
    Só entram dias em que d e todos os dias anteriores usados são bons. A glicose
    do próprio dia d nunca entra na entrada, para não vazar o alvo.
    """
    d = dias.sort_values(['pid', 'data']).copy()
    por_pid = d.groupby('pid')

    todos_bons = d['bom'].copy()
    colunas_ant = []
    for j in range(1, n_anteriores + 1):
        # o calendário está completo, então shift(j) é exatamente o dia d-j
        todos_bons &= por_pid['bom'].shift(j, fill_value=False)
        for col in GLICOSE:
            nome = f'{col}_ant{j}'
            d[nome] = por_pid[col].shift(j)
            colunas_ant.append(nome)

    d = d[todos_bons]
    entrada = colunas_ant + COMPORTAMENTO + BIO
    saida = d[['pid', 'data', 'grupo'] + entrada + ['glic_media']]
    return saida.rename(columns={'glic_media': 'alvo'}).reset_index(drop=True)


def montar_blocos(dias, n_dias=9):
    """Os primeiros `n_dias` dias bons seguidos de cada participante (D1 a D9).

    D1 a D6 são os dias observados e D7 a D9 os dias em que o AG recomenda o
    comportamento. A coluna 'dia' numera os dias do bloco de 1 a `n_dias`.
    """
    partes = []
    for _, d in dias.sort_values(['pid', 'data']).groupby('pid'):
        sequencia = (d['bom'] != d['bom'].shift()).cumsum()     # um número por bloco de dias iguais
        bons = d[d['bom']]
        for _, bloco in bons.groupby(sequencia[d['bom']]):
            if len(bloco) >= n_dias:
                b = bloco.head(n_dias).copy()
                b['dia'] = range(1, n_dias + 1)
                partes.append(b)
                break                                            # só o primeiro bloco
    blocos = pd.concat(partes, ignore_index=True)
    primeiras = ['pid', 'dia', 'data']
    return blocos[primeiras + [c for c in blocos.columns if c not in primeiras]]


def salvar_tabela(df, nome):
    """Grava uma tabela pronta em data/processed/<nome>.csv."""
    PROCESSED.mkdir(parents=True, exist_ok=True)
    caminho = PROCESSED / f'{nome}.csv'
    df.to_csv(caminho, index=False)
    return caminho


def carregar_tabela(nome):
    """Lê uma tabela de data/processed/, com a data e o grupo nos tipos certos."""
    df = pd.read_csv(PROCESSED / f'{nome}.csv', parse_dates=['data'])
    if 'grupo' in df.columns:
        df['grupo'] = pd.Categorical(df['grupo'], categories=['saudável', 'pré-diabetes', 'DM2'],
                                     ordered=True)
    return df
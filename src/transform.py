import json
import pandas as pd

def transform_to_parquet(in_json_path: str, out_parquet_path: str) -> str:
    with open(in_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    tabela = data["standings"][0]["table"]

    dados = []
    for item in tabela:
        dados.append({
            "posicao": item["position"],
            "time": item["team"]["name"],
            "sigla": item["team"]["tla"],
            "pontos": item["points"],
            "jogos": item["playedGames"],
            "vitorias": item["won"],
            "empates": item["draw"],
            "derrotas": item["lost"],
            "saldo_gols": item["goalDifference"],
        })

    df = pd.DataFrame(dados)
    if df.empty:
        raise ValueError("DataFrame vazio (transform)")

    df.to_parquet(out_parquet_path, index=False)
    return out_parquet_path

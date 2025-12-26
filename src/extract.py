import os
import requests
import json

def extract_standings(api_key: str, out_json_path: str) -> str:
    headers = {"X-Auth-Token": api_key}

    url = os.getenv("FOOTBALL_DATA_URL")
    if not url:
        raise RuntimeError("FOOTBALL_DATA_URL não definida no .env")

    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()

    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return out_json_path

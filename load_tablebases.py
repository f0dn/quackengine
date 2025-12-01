import requests
import os

endgames = [
    "KPvK",
    "KNvK",
    "KBvK",
    "KRvK",
    "KQvK",
    "KPvKP",
    "KNvKP",
    "KBvKP",
    "KNvKN",
    "KBvKP",
    "KBvKN",
    "KBvKB",
    "KRvKP",
    "KRvKN",
    "KRvKB",
    "KRvKR",
    "KQvKP",
    "KQvKN",
    "KQvKB",
    "KQvKR",
    "KQvKQ",
    "KPPvK",
    "KNPvK",
    "KNNvK",
    "KBPvK",
    "KBNvK",
    "KBBvK",
    "KRPvK",
    "KRNvK",
    "KRBvK",
    "KRRvK",
    "KQPvK",
    "KQNvK",
    "KQBvK",
    "KQRvK",
    "KQQvK",
]

os.makedirs("endgames", exist_ok=True)

def save(url, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Saved {filename}")

for endgame in endgames:
    wdl = f"https://tablebase.lichess.ovh/tables/standard/3-4-5-wdl/{endgame}.rtbw"
    dtz = f"https://tablebase.lichess.ovh/tables/standard/3-4-5-dtz/{endgame}.rtbz"

    save(wdl, f"endgames/{endgame}.rtbw")
    save(dtz, f"endgames/{endgame}.rtbz")

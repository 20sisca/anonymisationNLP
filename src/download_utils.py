import datetime
import logging
import os
import time
import json
import requests
from dotenv import load_dotenv

load_dotenv()

PISTE_API_KEY = os.environ.get('API_KEY')
PISTE_API_URL = "https://sandbox-api.piste.gouv.fr/cassation/judilibre/v1.0"

PISTE_API_HEADERS = {"KeyId": os.environ.get('API_KEY')}

DEFAULT_KEYS = [
    "id",
    "source",
    "jurisdiction",
    "chamber",
    "number",
    "location",
    "decision_date",
    "update_date",
    "type",
    "nac",
]


def download_data_between_update_dates(
    start_date: datetime.date,
    end_date: datetime.date,
    jurisdiction: str = "cc",
    headers: str = PISTE_API_HEADERS,
    base_url: str = PISTE_API_URL,
    timeout: int = 5,
    mask: list[str] = DEFAULT_KEYS,
):
    params = {
        "date_start": str(start_date),
        "date_end": str(end_date),
        "jurisdiction": jurisdiction,
        "date_type": "update",
        "batch_size": 1_000,
        "batch": 0,
    }

    data = {m: [] for m in mask}
    n_results = 0

    has_next_batch = True
    aux = []

    while has_next_batch:
        # print("before requesting to ", f"{base_url}/export")
        response = requests.get(
            url=f"{base_url}/export", headers=headers, params=params
        )
        # print("after requesting")

        if response.status_code != 200:
            print('bad request', response.status_code)
            logging.debug(
                f"Request received a non 200 status code {response.status_code}"
            )
            time.sleep(timeout)
        else:
            print('good request')
            response_json = response.json()
            has_next_batch = response_json["next_batch"] is not None

            results = response_json["results"]
            aux.append(results)
            # print(results)

            for r in results:
                n_results += 1
                for m in mask:
                    data[m].append(r.get(m))

            params["batch"] += 1

    logging.debug(
        f"Collected {n_results} decisions from {start_date} to {end_date}")

    # aux[0][i] being un decret
    # print(aux, len(aux), type(aux), aux[0], type(
    #     aux[0][0]), json.dumps(aux[0][1], indent=4))
    return [aux[0]]
    # return data


def download_specific_document_by_id(
    document_id: str,
    headers: str = PISTE_API_HEADERS,
    base_url: str = PISTE_API_URL,
    mask: list[str] = DEFAULT_KEYS,
):
    response = requests.get(
        url=f"{base_url}/decision", headers=headers, params={"id": document_id}
    )

    if response.status_code == 200:
        result = response.json()

        return {m: result.get(m) for m in mask}

    logging.debug(f"Received status code {response.status_code}")

    return dict()


data = download_data_between_update_dates(
    '2022-02-01', '2022-02-04', timeout=1)
# firstRep = download_specific_document_by_id(data.get('id')[0])

print(json.dumps(data, indent=4), type(data))
# print(firstRep)

# Serializing json
json_object = json.dumps(data[:10], indent=4)

# Writing to sample.json
with open("arrets.json", "w") as outfile:
    outfile.write(json_object)

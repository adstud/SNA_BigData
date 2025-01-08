# Extragerea datelor și încărcarea în BigQuery

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from google.cloud import bigquery

# Configurare BigQuery
client = bigquery.Client(project="tehnologii-big-data-ad")
dataset_id = "openalex_work"
table_id = "machine_learning_works"
table_ref = f"{client.project}.{dataset_id}.{table_id}"

# Verifică dacă tabelul există, altfel creează-l
try:
    client.get_table(table_ref)
except:
    schema = [
        bigquery.SchemaField("id", "STRING"),
        bigquery.SchemaField("title", "STRING"),
        bigquery.SchemaField("publication_year", "INTEGER"),
        bigquery.SchemaField("concepts", "RECORD", mode="REPEATED", fields=[
            bigquery.SchemaField("id", "STRING"),
            bigquery.SchemaField("display_name", "STRING")
        ]),
        bigquery.SchemaField("cited_by_count", "INTEGER"),
        bigquery.SchemaField("referenced_works", "STRING", mode="REPEATED")
    ]
    table = bigquery.Table(table_ref, schema=schema)
    client.create_table(table)
    print(f"Tabelul {table_id} a fost creat.")

# Configurare sesiune cu retry și backoff exponențial
session = requests.Session()
retry_strategy = Retry(
    total=5,  # Numărul total de încercări
    backoff_factor=1,  # Factorul de backoff exponențial
    status_forcelist=[429, 500, 502, 503, 504],  # Coduri de status pentru care se face retry
    allowed_methods=["GET"]  # Metode HTTP pentru care se aplică retry
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Funcție pentru a extrage date din API-ul OpenAlex folosind paginarea cu cursor
def fetch_data_with_cursor():
    base_url = "https://api.openalex.org/works"
    params = {
        "filter": "concepts.id:C119857082",
        "per-page": 200,
        "cursor": "*"
    }
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; MyBot/0.1; +http://example.com/bot)",
        "From": "exemplu@domeniu.com"  # Înlocuiește cu adresa ta de email
    }

    while True:
        try:
            response = session.get(base_url, headers=headers, params=params, timeout=(5, 10))
            response.raise_for_status()
        except requests.exceptions.Timeout:
            print("Cererea a expirat. Se încearcă din nou...")
            continue
        except requests.exceptions.RequestException as e:
            print(f"A apărut o eroare: {e}")
            break

        data = response.json()
        results = data.get("results", [])
        if not results:
            print("Nu mai sunt date de procesat.")
            break

        rows_to_insert = []
        for work in results:
            rows_to_insert.append({
                "id": work.get("id", ""),
                "title": work.get("title", ""),
                "publication_year": work.get("publication_year", 0),
                "concepts": [{"id": c.get("id", ""), "display_name": c.get("display_name", "")} for c in work.get("concepts", [])],
                "cited_by_count": work.get("cited_by_count", 0),
                "referenced_works": work.get("referenced_works", [])
            })

        errors = client.insert_rows_json(table_ref, rows_to_insert)
        if errors == []:
            print(f"Încărcat {len(rows_to_insert)} rânduri cu succes.")
        else:
            print(f"Erori la încărcare: {errors}")

        # Actualizează cursorul pentru pagina următoare
        params["cursor"] = data.get("meta", {}).get("next_cursor", None)
        if not params["cursor"]:
            print("Nu mai sunt pagini de procesat.")
            break

# Execută funcția pentru a începe extragerea și încărcarea datelor
fetch_data_with_cursor()

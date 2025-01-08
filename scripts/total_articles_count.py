import requests

url = "https://api.openalex.org/works?filter=concepts.id:C119857082&per-page=200"
response = requests.get(url)
data = response.json()

# Numărul total de articole
print("Numărul total de articole:", data["meta"]["count"])

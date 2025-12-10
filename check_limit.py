import urllib.request
import json

url = "https://vgregion.entryscape.net/rowstore/dataset/1802e57a-b25d-4716-8437-9ed648bbae59"

for limit in [100, 500, 1000, 5000, 10000]:
    try:
        full_url = f"{url}?_limit={limit}&_offset=0"
        with urllib.request.urlopen(full_url) as response:
            data = json.loads(response.read().decode())
            count = len(data.get("results", []))
            print(f"Requested limit: {limit}, Returned count: {count}")
    except Exception as e:
        print(f"Error with limit {limit}: {e}")

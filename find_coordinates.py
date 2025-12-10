import urllib.request
import json

url = "https://vgregion.entryscape.net/rowstore/dataset/1802e57a-b25d-4716-8437-9ed648bbae59"

# Sample different offsets to find items with coordinates
offsets = [0, 5000, 10000, 20000, 30000, 40000, 50000, 60000]
total_with_coords = 0
samples = []

for offset in offsets:
    try:
        full_url = f"{url}?_limit=1000&_offset={offset}"
        with urllib.request.urlopen(full_url) as response:
            data = json.loads(response.read().decode())
            results = data.get("results", [])

            with_coords = [
                r for r in results
                if r.get('latitude') and r.get('longitude')
                and str(r['latitude']).strip() != ''
                and str(r['longitude']).strip() != ''
            ]

            total_with_coords += len(with_coords)

            if with_coords and len(samples) < 5:
                samples.extend(with_coords[:min(5-len(samples), len(with_coords))])

            print(f"Offset {offset}: {len(with_coords)} items with coordinates out of {len(results)}")

    except Exception as e:
        print(f"Error at offset {offset}: {e}")

print(f"\n=== SUMMARY ===")
print(f"Total items with coordinates found: {total_with_coords}")
print(f"\nSample items with coordinates:")
for item in samples:
    print(f"\n  ID: {item['id']}")
    print(f"  Title: {item.get('title', 'N/A')}")
    print(f"  Creator: {item.get('creator', 'N/A')}")
    print(f"  Coordinates: {item['latitude']}, {item['longitude']}")

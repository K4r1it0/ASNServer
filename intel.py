import subprocess
import asyncio
import itertools
import json

async def parse_rdap_response(asn):
    result = subprocess.run(['rdap-client', '-asn', str(asn)], stdout=subprocess.PIPE)
    response = result.stdout.decode('utf-8')
    entities = []

    entity_data = {}
    for line in response.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key == "aut-num":
                asn = value
            elif key not in ("created", "changed"):
                entity_data[key] = value
        elif line.strip() == "":
            if entity_data:
                entity_data["asn"] = asn
                entities.append(entity_data)
                entity_data = {}

    if entity_data:
        entity_data["asn"] = asn
        entities.append(entity_data)

    return entities

async def main():
    with open("asns.txt", "r") as f:
        asns = [line.strip() for line in f if line.strip()]
        
    coroutines = [parse_rdap_response(asn) for asn in asns]
    results = await asyncio.gather(*coroutines)
    merged_results = list(itertools.chain.from_iterable(results))
    with open('merged_results.json', 'w') as f:
        json.dump(merged_results, f)

if __name__ == "__main__":
    asyncio.run(main())


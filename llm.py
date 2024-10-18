"""
Make requests to (Azure) OpenAI model
"""
from urllib.request import Request, urlopen
import urllib.error
import time
import os
import json

with open("config.json", "r") as f:
    cfg = json.loads(f.read())
    API_URL = cfg["OPENAI_API_URL"]
    API_KEY = cfg["OPENAI_API_KEY"]

def respond(messages, temperature=0.0):
    params = {
        "messages": messages,
        "stream": True,
        "temperature": temperature,
    }

    req = Request(
        API_URL,
        data=json.dumps(params).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'api-key': API_KEY},
        method="POST"
    )

    num_retries = 3
    while num_retries > 0:
        num_retries -= 1
        try:
            with urlopen(req) as resp:
                for line in resp:
                    decoded = line.decode('utf-8')
                    if "data: [DONE]" in decoded:
                        return
                    if not decoded.startswith('data:'):
                        continue
                    obj = json.loads(decoded.replace("data:", ""))
                    if len(obj["choices"]) > 0 and obj["choices"][0]["delta"]:
                        yield obj["choices"][0]["delta"]["content"]
            return
        except urllib.error.HTTPError as e:
            if e.status == 429:
                # have some timeout so we don't wait for ages...
                if int(e.headers["Retry-After"]) > 60:
                    raise RuntimeError
                time.sleep(int(e.headers["Retry-After"]))
            else:
                raise RuntimeError
    raise RuntimeError

if __name__ == "__main__":
    import sys
    print("".join(respond([{"role": "user", "content": sys.argv[1]}])))

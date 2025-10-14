import requests

url = "https://cdn.jsdelivr.net/npm/vis-network@9.1.2/dist/vis-network.min.js"
vis_js = requests.get(url).text

with open("vis-network.min.js", "w", encoding="utf-8") as f:
    f.write(vis_js)

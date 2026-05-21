import urllib.request

url = 'https://kroki.io/plantuml/png'
with open("d:/TypeBlast/diagrams/activity.puml", "r", encoding='utf-8') as f:
    puml = f.read()

req = urllib.request.Request(
    url, 
    data=puml.encode('utf-8'), 
    headers={
        'Content-Type': 'text/plain',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
)

try:
    with urllib.request.urlopen(req) as response:
        with open('d:/TypeBlast/diagrams/activity.png', 'wb') as f:
            f.write(response.read())
    print("Success")
except Exception as e:
    print(f"Failed: {e}")

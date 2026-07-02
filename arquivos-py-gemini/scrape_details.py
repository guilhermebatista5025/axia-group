import urllib.request
import re
import html

url = 'https://www.axiagroup.com.br/produto/7/administracao-imobiliaria'
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

try:
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
        
    # Write to a file
    with open('scratch_prod.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Downloaded successfully to scratch_prod.html")
except Exception as e:
    print(f"Error: {e}")

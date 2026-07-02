import urllib.request
import re
import html
import json
import time

products = [
    {"id": 1, "slug": "gestao-administrativa"},
    {"id": 2, "slug": "comercial"},
    {"id": 3, "slug": "financeiro"},
    {"id": 4, "slug": "contabil"},
    {"id": 5, "slug": "marketing-digital"},
    {"id": 6, "slug": "assessoria-juridica"},
    {"id": 7, "slug": "administracao-imobiliaria"},
    {"id": 8, "slug": "exportacao-e-importacao"},
    {"id": 9, "slug": "captacao-de-recursos-financeiros"},
    {"id": 10, "slug": "recursos-humanos"},
    {"id": 11, "slug": "antecipacao-de-recebiveis"},
    {"id": 12, "slug": "workshops-e-treinamentos"},
    {"id": 13, "slug": "plano-de-negocio"},
    {"id": 14, "slug": "pericia-judicial"},
    {"id": 15, "slug": "analise-de-viabilidade-economico-financeira"},
    {"id": 16, "slug": "pesquisa-mercadologica-de-negocios-"},
    {"id": 17, "slug": "holding-"}
]

data = []

for prod in products:
    url = f"https://www.axiagroup.com.br/produto/{prod['id']}/{prod['slug']}"
    print(f"Fetching {url}...")
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            
        # Extract title
        title_match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
        title = title_match.group(1).strip() if title_match else prod['slug'].replace('-', ' ').upper()
        
        # Extract text content inside <div class="text">...</div>
        text_match = re.search(r'<div class="text">(.*?)</div>', content, re.DOTALL)
        text_content = text_match.group(1).strip() if text_match else ""
        
        # Extract image URL
        img_match = re.search(r'<div class="main item">.*?href="(.*?)"', content, re.DOTALL)
        img_url = img_match.group(1).strip() if img_match else ""
        if not img_url:
            img_match2 = re.search(r'property="og:image"\s+content="(.*?)"', content)
            img_url = img_match2.group(1).strip() if img_match2 else ""
            
        data.append({
            "id": prod["id"],
            "slug": prod["slug"],
            "title": title,
            "description": text_content,
            "image": img_url
        })
        time.sleep(0.5)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

with open('products_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Scrape finished. Saved to products_data.json")

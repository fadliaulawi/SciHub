import requests
import re
import urllib

# Number of page (each page consists of 10 paper)
numPage = 10
dwn = 0
na = 0

lst = []

# Extract list of PubMed's url based on term keywords
for i in range(1, numPage + 1):
  urlSearch = f"https://pubmed.ncbi.nlm.nih.gov/?term=nutrigenomic&page={i}"
  req = requests.get(urlSearch)

  lst.extend(list(set([r[0] for r in re.findall('permalink-url="(https:([^"]+))"', req.text)])))

for l in lst:
  req = requests.get(l)
 
  # Get identifier (DOI) of the paper
  url = re.findall('href="(https:\/\/doi.org\/([^"]+))"', req.text)

  if len(url) == 0:
    print(f"DOI not available: {l}")
    na += 1
    continue

  url = url[0]
  title = re.findall('(?<=heading-title">)([^<]+)', req.text)[0].strip()

  # Access Sci Hub based on DOI
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
  req = requests.get("https://sci-hub.se/" + url[0], headers=headers)

  urlPdf = re.findall('src="\/\/([^"]+)"', req.text)
  
  # Check if Sci Hub has the paper
  if len(urlPdf) > 0:
    print(f"Downloading: {title}")
    urllib.request.urlretrieve(f"https://{urlPdf[0]}", f"{title.replace('/', ' ')}.pdf")
    dwn += 1
  else:
    print(f"Not available in Sci Hub: {url[0]}")
    na += 1

print(f"\nDownloaded: {dwn}, Not downloaded: {na}")
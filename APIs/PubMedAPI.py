from .Caching import txt_cache
import requests
import xml.etree.ElementTree as ET
from time import sleep

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ELINK_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"

# Search pubmed with a general querry
@txt_cache()
def search_pubmed(query, retmax=500):
    sleep(1)  # rate limit
    
    url = BASE_URL
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }
    r = requests.post(url, data=params)
    r.raise_for_status()
    data = r.json()

    pmids_from_result = data["esearchresult"]["idlist"]
    if(len(pmids_from_result) >= retmax): raise Exception(f"Result exceed maximum possible returnable results of {retmax}")
    return pmids_from_result

# Papers given paper cites
def get_references_from_pmid(pmid):
    params = {
        "dbfrom": "pubmed",
        "db": "pubmed",
        "linkname": "pubmed_pubmed_refs",  
        "id": pmid,
        "retmode": "json"
    }
    
    r = requests.get(ELINK_URL, params=params)
    r.raise_for_status()
    data = r.json()
    linksets = data.get("linksets", [])
    if not linksets:
        return set()

    linksetdbs = linksets[0].get("linksetdbs", [])
    if not linksetdbs:
        return set()

    return set(linksetdbs[0].get("links", []))

# Papers that cite given paper
@txt_cache()
def get_citing_pmids(pmid, api_key=None):
    sleep(1) # rate limit

    params = {
        "dbfrom": "pubmed",
        "linkname": "pubmed_pubmed_citedin",
        "id": pmid,
        "retmode": "xml"
    }
    
    if api_key:
        params["api_key"] = api_key  

    response = requests.get(ELINK_URL, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.text)

    citing_pmids = [
        link_id.text
        for link_id in root.findall(".//LinkSetDb[DbTo='pubmed']/Link/Id")
    ]

    return citing_pmids
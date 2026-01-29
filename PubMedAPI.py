import requests
import time
import os
import xml.etree.ElementTree as ET

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ELINK_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
CACHE_FILE = "doi_pmid_cache.txt"

def search_pubmed(query, retmax=500):
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
    return set(data["esearchresult"]["idlist"]) 

def get_references_from_pmid(pmid):
    params = {
        "dbfrom": "pubmed",
        "db": "pubmed",
        "linkname": "pubmed_pubmed_refs",  # papers THIS paper cites
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


def load_doi_cache():
    """Load DOI to PMID mappings from cache file."""
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    doi, pmid = line.split("\t", 1)
                    cache[doi] = pmid
    return cache


def save_to_doi_cache(doi, pmid):
    """Save a single DOI to PMID mapping to cache file."""
    with open(CACHE_FILE, "a") as f:
        f.write(f"{doi}\t{pmid}\n")


def doi_to_pmid(doi, sleep=1):
    """
    Convert a single DOI to a PMID using PubMed.
    Checks cache first, then queries API if not found.
    sleep: delay to stay under NCBI rate limits (~3 req/sec without API key)
    """
    # Check cache first
    cache = load_doi_cache()
    if doi in cache:
        print(f"Found in cache: {doi} -> {cache[doi]}")
        return cache[doi]
    
    # Query API if not in cache
    params = {
        "db": "pubmed",
        "term": f"{doi}[AID]",
        "retmode": "json"
    }
    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    data = r.json()
    
    idlist = data["esearchresult"]["idlist"]
    time.sleep(sleep)
    
    if idlist:
        pmid = idlist[0]  # usually one match
        save_to_doi_cache(doi, pmid)
        print(f"Saved to cache: {doi} -> {pmid}")
        return pmid
    return None


def save_results(pmids, filename="search_results.txt"):
    """
    Save search results (PMIDs) to a file.
    
    Args:
        pmids: Set or list of PubMed IDs
        filename: Output filename (default: search_results.txt)
    """
    with open(filename, "w") as f:
        for pmid in sorted(pmids):
            f.write(f"{pmid}\n")
    print(f"Results saved to {filename} ({len(pmids)} PMIDs)")


def get_citing_pmids(pmid, api_key=None):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
    params = {
        "dbfrom": "pubmed",
        "linkname": "pubmed_pubmed_citedin",
        "id": pmid,
        "retmode": "xml"
    }
    
    if api_key:
        params["api_key"] = api_key  # optional but recommended for higher rate limits

    response = requests.get(base_url, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.text)

    citing_pmids = [
        link_id.text
        for link_id in root.findall(".//LinkSetDb[DbTo='pubmed']/Link/Id")
    ]

    return citing_pmids
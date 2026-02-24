
from APIs.PubMedAPI import *
from APIs.BibTexAPI import *

bibtex_path = "/home/andre/Downloads/GWAVA FeasbilityPain.bib"

#query = "(predict*[ti] OR annotat*[ti] OR detect*[ti] OR assess*[ti]) AND (variant*[ti] OR mutation*[ti] OR snp[ti] OR snv[ti] OR \"point mutation\"[ti]) AND (functional[tiab] OR pathogenic[tiab] OR deleterious[tiab] OR consequence*[tiab] OR impact[tiab]) AND (score[ti] OR model[ti] OR algorithm[ti] OR tool[ti]) NOT review[Publication Type]"
query = """(("genetic variant"[Title/Abstract] OR variants[Title/Abstract] OR mutation*[Title/Abstract] OR missense[Title/Abstract] OR "amino acid substitution"[Title/Abstract] OR noncoding[Title/Abstract] OR "non-coding"[Title/Abstract] OR "regulatory variant*"[Title/Abstract])
AND
("variant effect"[Title/Abstract] OR "functional impact"[Title/Abstract] OR pathogenic*[Title/Abstract] OR deleterious*[Title/Abstract] OR damaging[Title/Abstract])
AND
(predict*[Title/Abstract] OR scor*[Title/Abstract] OR "prediction model"[Title/Abstract] OR "computational model"[Title/Abstract] OR classifier[Title/Abstract] OR "in silico"[Title/Abstract])
AND
("we developed"[Title/Abstract] OR "we present"[Title/Abstract] OR "we introduce"[Title/Abstract] OR "we propose"[Title/Abstract] OR framework[Title/Abstract] OR algorithm*[Title/Abstract] OR tool[Title/Abstract] OR method[Title/Abstract])
AND
(generaliz*[Title/Abstract] OR genome-wide[Title/Abstract] OR proteome-wide[Title/Abstract] OR "all possible"[Title/Abstract] OR "across the genome"[Title/Abstract] OR integrat*[Title/Abstract] OR ensemble[Title/Abstract] OR "machine learning"[Title/Abstract] OR "deep learning"[Title/Abstract] OR conservation[Title/Abstract] OR evolutionary[Title/Abstract]))
NOT
(review[Publication Type] OR guideline*[Title] OR recommendation*[Title] OR ACMG[Title/Abstract] OR ClinGen[Title/Abstract])
NOT
("association study"[Title/Abstract] OR GWAS[Title/Abstract] OR cohort[Title/Abstract] OR patients[Title/Abstract] OR survival[Title/Abstract] OR prognosis[Title/Abstract])
NOT
("functional assay"[Title/Abstract] OR "in vitro"[Title/Abstract] OR CRISPR[Title/Abstract] OR "molecular dynamics"[Title/Abstract])
NOT
(gene-specific[Title/Abstract] OR "BRCA1"[Title/Abstract] OR "BRCA2"[Title/Abstract] OR "CFTR"[Title/Abstract] OR "TP53"[Title/Abstract])
AND
(score[Title] OR scoring[Title] OR predictor[Title] OR prediction[Title])"""



pubmed_pmids = search_pubmed(query)
print(f"PubMed results: {len(pubmed_pmids)} papers")

bib_dois = get_dois_from_bib(bibtex_path)
print(f"DOIs in BibTeX: {len(bib_dois)}")

doi_pmid_map = {}
not_found_doi = []

for doi in bib_dois:
    pmid = doi_to_pmid(doi.lower())
    if pmid:
        doi_pmid_map[doi] = pmid
        print(f"✔ {doi} → PMID {pmid}")
    else:
        not_found_doi.append(doi)
        print(f"✖ {doi} → NOT FOUND")

print("\n" + "="*80)
print("COMPARISON RESULTS")
print("="*80)
print(f"\nSearch Results: {len(pubmed_pmids)} PMIDs")
print(f"Bibliography: {len(doi_pmid_map)} PMIDs with DOIs")

# Find matches
bib_pmids = set(doi_pmid_map.values())
matches = bib_pmids.intersection(pubmed_pmids)
not_in_search = bib_pmids - pubmed_pmids

print(f"\n✔ MATCHING PMIDs: {len(matches)}")
print(f"✖ NOT IN SEARCH RESULTS: {len(not_in_search)}")
print(f"⚠ DOIs NOT RESOLVED TO PMID: {len(not_found_doi)}")

if matches:
    print("\nMatching PMIDs (found in both bibliography and search):")
    for doi, pmid in sorted(doi_pmid_map.items()):
        if pmid in matches:
            print(f"  ✔ PMID {pmid} ({doi})")

if not_in_search:
    print("\nBibliography PMIDs NOT found in search results:")
    for doi, pmid in sorted(doi_pmid_map.items()):
        if pmid in not_in_search:
            print(f"  PMID {pmid} ({doi})")

if not_found_doi:
    print("\nDOIs that could not be resolved to PMID:")
    for doi in sorted(not_found_doi):
        print(f"  {doi}")



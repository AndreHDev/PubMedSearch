from PubMedAPI import *
from BibTexAPI import *

from time import sleep

#scores
pmids = [
    "38183205", "33618777", "30371827", "24487276",
    "25338716",
    "26727659",
    "26727659",
    "27666373",
    "25552646",
    "25552646",
    "20354512",
    "23056405",
    "21727090",
    "33219223",
    "21152010",
    "19858363",
    "25599402",
    "28288115",
    "24487584",
    "22955989",
    "28968714",
    "21457909",
    "30256891",
    "30675030",
    "33893808",
    "28093075",
    "12952881",
    "33219223",
    "15965030",
    "26301843",
    "16024819",
    "19478016",
    "17526529",
    "22241780",
    "22505138",
    "19602639",
    "16895930",
    "18387208",
    "23819870",
    "26213851",
    "27197224"
]
# Pain–related query string
pain_query = """(
((chronic) OR (persisting) OR (persistent) OR (lasting) OR (neuropathic) OR 
(nociceptive) OR (nociplastic) OR (mixed) OR (neurogenic) OR (back) OR (neck) OR 
(migraine) OR (arthritis) OR (osteoart*) OR (joint) OR (rheumatic) OR 
(inflammatory) OR (musculoskeletal) OR (muscle) OR (visceral) OR (widespread) OR 
(somatoform) OR (cancer) OR (postoperative) OR (postsurgic*) OR (perioperative))
AND ((pain OR painful)) OR orchialgia OR analgesi* OR fibromyalgia OR pain*)
"""

# Open a file for writing
with open("results.txt", "w", encoding="utf-8") as f:

    all_citing_matching_pain = {}

    for pmid in pmids:
        citing_pmids = get_citing_pmids(pmid)

        if not citing_pmids:
            print(f"PMID {pmid}: No citing papers found", file=f)
            continue

        # Build query like manual PubMed search
        combined_query = pain_query + " " + " ".join(citing_pmids)

        match_pmids = search_pubmed(combined_query)

        print(f"PMID {pmid}:", file=f)
        print(f"  Citing papers found: {len(citing_pmids)}", file=f)
        print(f"  Amount of citing papers matching pain query: {len(match_pmids)}", file=f)
        all_citing_matching_pain[pmid] = match_pmids
        print("------", file=f)

        sleep(1)  # respect NCBI rate limits

    # Collect all PMIDs into a single set to remove duplicates
    all_pmids = set()
    for match_pmids in all_citing_matching_pain.values():
        all_pmids.update(match_pmids)  # add all PMIDs from the set

    # Join into a simple string with spaces
    all_pmids_str = " ".join(all_pmids)

    # Write to file
    print("All unique PMIDs from citing papers matching pain query:", file=f)
    f.write(all_pmids_str + "\n")


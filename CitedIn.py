from APIs.PubMedAPI import *
#from BibTexAPI import *



# all scores from paper
score_pmids = [
    "38183205", "33618777", "30371827", "24487276", "33618777", "25338716", "26727659", "26727659", 
    "27666373", "25552646", "25552646", "36209109", "20354512", "23056405", "21727090", "21152010", 
    "19858363", "25599402", "28288115", "24487584", "22955989", "28968714", "25583119", "23033316", 
    "28985712", "21457909", "30256891", "33893808", "24681721", "20676075", "28093075", "34717010", 
    "12952881", "27193693", "33219223", "19734154", "15965030", "26301843", "30013180", "33462483", 
    "16024819", "19478016", "17526529", "22241780", "22505138", "19602639", "16895930", "18387208", 
    "16204125", "23819870", "26213851", "27197224", "29588361", "11337480", "22689647", "12824425", 
    "27776117", "4843792", "37733863", "1438297", "30661751", "30220433", "33479230", "30559491", 
    "28498993", "27153718", "28851873", "27995669", "32352516", "34551312", "34861178", "37563329", 
    "38934805", "35639618", "37636282", "40397311", "38168397", "41286104", "34707284", "28092658", 
    "34270679", "37550700", "37084271", "35453737", "32831124", "36376793", "29617928", "33300042", 
    "37475887", "32340307", "35486646", "31096927", "30518757", "27569544", "33543123", "34349788", 
    "27009626", "37198692", "35036922", "32735577", "30823901", "33789710", "30475984", "15285897", 
    "14695534", "29689380", "35965322", "33761318", "37083939", "32101277", "30804562", "35079159", 
    "36273432", "29750258", "34289339", "35801945", "36707993", "34648033", "36063453", "32938008", 
    "26075791", "33686085", "32444882", "28592878", "36611253", "36651276", "31157880", "23736532", 
    "28794409", "30704475", "34850938", "33866367", "33603233", "34608324", "39779956", "35551308", 
    "35449021","41606153", "37733863"
]

# Pain–related query string
pain_query = """(
((chronic) OR (persisting) OR (persistent) OR (lasting) OR (neuropathic) OR 
(nociceptive) OR (nociplastic) OR (mixed) OR (neurogenic) OR (back) OR (neck) OR 
(migraine) OR (arthritis) OR (osteoart*) OR (joint) OR (rheumatic) OR 
(inflammatory) OR (musculoskeletal) OR (muscle) OR (visceral) OR (widespread) OR 
(somatoform) OR (cancer) OR (postoperative) OR (postsurgic*) OR (perioperative))
AND ((pain OR painful)) OR orchialgia OR analgesi* OR fibromyalgia) 
"""

pain_query2 = """(
(((chronic) OR (persisting) OR (persistent) OR (lasting) OR (neuropathic) OR (nociceptive) OR (nociplastic)
OR (mixed) OR (neurogenic) OR (back) OR (neck) OR (migraine) OR (arthritis) OR (osteoart*) OR (joint) OR 
(rheumatic) OR (inflammatory) OR (musculoskeletal) OR (muscle) OR (visceral) OR (widespread) OR (somatoform)
OR (cancer) OR (postoperative) OR (postsurgic*) OR (perioperative)) AND (pain OR painful) OR orchialgia OR 
analgesi* OR fibromyalgia) AND ("rare variant" OR "rare variants" OR "rare genetic variant")
)

"""

# Open a file for writing
with open("results.txt", "w", encoding="utf-8") as f:

    all_citing_matching_pain = {}

    for pmid in score_pmids:
        citing_pmids = get_citing_pmids(pmid)

        if not citing_pmids:
            print(f"PMID {pmid}: No citing papers found", file=f)
            continue

        # Build query like manual PubMed search
        combined_query = pain_query2 + " " + " ".join(citing_pmids)

        match_pmids = search_pubmed(combined_query)

        print(f"PMID {pmid}:", file=f)
        print(f"  Citing papers found: {len(citing_pmids)}", file=f)
        print(f"  Amount of citing papers matching pain query: {len(match_pmids)}", file=f)
        all_citing_matching_pain[pmid] = match_pmids
        print("------", file=f)

    # Collect all PMIDs into a single set to remove duplicates
    all_pmids = set()
    for match_pmids in all_citing_matching_pain.values():
        all_pmids.update(match_pmids)  # add all PMIDs from the set

    # Join into a simple string with spaces
    all_pmids_str = " ".join(all_pmids)

    # Write to file
    print("All unique PMIDs from citing papers matching pain query:", file=f)
    f.write(all_pmids_str + "\n")
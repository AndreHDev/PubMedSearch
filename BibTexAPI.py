import bibtexparser

# TODO: Not every entry has a DOI
# TODO: Find way get amount of entries without relying on fields

def get_titles_from_bib(bib_path):
    with open(bib_path) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    titles = set()
    for entry in bib_database.entries:
        if "title" in entry:
            titles.add(entry["title"].strip())
    return titles

def get_dois_from_bib(bib_path):
    with open(bib_path) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    dois = set()
    for entry in bib_database.entries:
        if "doi" in entry:
            dois.add(entry["doi"].lower().strip())
    return dois

def get_bib_entries(bib_path):
    with open(bib_path) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    return bib_database.entries

import bibtexparser

def get_metadata_from_bib(bib_path):
    with open(bib_path) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    records = []

    for entry in bib_database.entries:
        record = {
            "id": entry.get("ID"),
            "title": entry.get("title"),
            "doi": entry.get("doi"),
            "pmid": entry.get("pmid"),
            "abstract": entry.get("abstract") or entry.get("annote") or entry.get("note"),
            "year": entry.get("year"),
            "journal": entry.get("journal") or entry.get("booktitle"),
        }
        records.append(record)

    return records

def get_abstracts(records):
    # How many have abstracts?
    with_abstract = [r for r in records if r["abstract"]]
    print(f"Entries with abstracts: {len(with_abstract)}")

    # Write all abstracts to a text file
    output_file = "abstracts.txt"
    with open(output_file, "w") as f:
        for i, r in enumerate(with_abstract, 1):
            f.write(f"=== ABSTRACT {i} ===\n")
            f.write(f"Title: {r['title']}\n")
            f.write(f"ID: {r['id']}\n")
            if r['doi']:
                f.write(f"DOI: {r['doi']}\n")
            if r['year']:
                f.write(f"Year: {r['year']}\n")
            if r['journal']:
                f.write(f"Journal: {r['journal']}\n")
            f.write(f"\n{r['abstract']}\n")
            f.write("\n" + "-"*80 + "\n\n")

    print(f"Abstracts written to {output_file}")
    
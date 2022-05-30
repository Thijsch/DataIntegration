# DataIntegration
Dit project is gedaan door Thijs, Janneke en David.
## Orginele dataset.

Voor dit project is er gebruik gemaakt van drie verschillende data van personen. Deze data komt van PersonalGenome (BRON?). De personen die voor dit project gebruikt zijn: PGP13, PGP18 en PGP48. Per persoon is er een PDF bestand waar zij zelf informatie overzich zelf hebben gegeven. Zoals hun lengte, ziektes en medische procedures. Verder is er ook een VCF bestand waar de mutatie per persoon zijn aangegeven.

Om de data van VCF te kunnen gebruiken, is de data door SNPeff gehaald. Deze annoteert de varianten die zich op chromosoon 21 bevinden. Hierna worden er 10 missense variants en ook 10 frameshift variants opgeslagen. Deze woorden ook gebruikt als test data set.

Om de data van de drie personen te mappen is er gebruikt gemaakt van verschillende vocabularies van Athena (BRON?). Dit zijn de SNOMED, Gender, Race, OMOP Extension, HGNC en de OMOP Genomic. 

De data van Sex, Ethnicity en Conditions or Symptoms is met de hand gemapped omdat deze data door de persoon zelf is ingevuld, waardoor het niet een standaard manier is ingvuld. De concept_id’s met de omschrijvingen zijn in een nieuwe tabel “mapping” gezet zodat deze opgehaald kunnen worden door de pipeline. 

## Python files: 
| Naam: | Functie: |
| ----- | -------- |
| PDF_reader.py | Dit bestand bevat een class waarin de PDF’s in gelezen worden. Dit wordt gedaan met tabula. Dit is een package waarmee PDF’s makkelijk ingelezen kunnen worden. Uit de PDF’s wordt de volgende data gehaald: profile en conditions or symptoms. Ook wordt de data gemapped in tegen de data in de database. |
| Vcf_reader.py | Dit bestand bevat een class waarin de VCF’s in gelezen worden. Dit wordt gedaan met een RegEx. Er worden hier verschillende dingen uit op gehaald: chromosoom nummer, gene, type, positie van het aminozuur, de lengte van het aminozuur en wat de mutatie is. Ook wordt de data gemapped in tegen de data in de database. |
| Inserter.py | Dit bestand vult de database met de data die uit de twee data readers komt.|


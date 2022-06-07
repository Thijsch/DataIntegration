# DataIntegration
Dit project is gedaan door Thijs, Janneke en David.

# Requirements
* De code is geschreven in Python 3.10. Om het te kunnen runnen is het belangrijk dat deze versie ook gebruikt wordt, omdat er nieuwe syntax gebruikt is. 
* Gebruik example.env om de juiste variabelen in een .env file te zetten.
* Zie requirements.txt.
## Orginele dataset.

Voor dit project is er gebruik gemaakt van drie verschillende data van personen. Deze data komt van PersonalGenome (Szego & Scherer, z.d.). De personen die voor dit project gebruikt zijn: PGP13, PGP18 en PGP48. Per persoon is er een PDF bestand waar zij zelf informatie overzich zelf hebben gegeven. Zoals hun lengte, ziektes en medische procedures. Verder is er ook een VCF bestand waar de mutatie per persoon zijn aangegeven.

Om de data van VCF te kunnen gebruiken, is de data door SNPeff gehaald. Deze annoteert de varianten die zich op chromosoon 21 bevinden. Hierna worden er 10 missense variants en ook 10 frameshift variants opgeslagen. Deze worden ook gebruikt als test data set.

Om de data van de drie personen syntactisch te mappen is er gebruikt gemaakt van verschillende vocabularies van Athena (Odysseus Data Services, 2015). Dit zijn de SNOMED, Gender, Race, OMOP Extension, HGNC en de OMOP Genomic. 

De data van Sex, Ethnicity en Conditions or Symptoms is met de hand semantisch gemapped omdat deze data door de persoon zelf is ingevuld, waardoor het niet een standaard manier is ingevuld. De concept_id’s met de omschrijvingen zijn in een nieuwe database tabel “mapping” gezet zodat deze opgehaald kunnen worden door de pipeline. 

Op het moment dat een er niks gevonden kan worden door middel van syntactisch mappen wordt het concept_id op 0 gezet. Dit betekend dat er geen matching concept is.

## Python files: 
| Naam: | Functie: |
| ----- | -------- |
| PDF_reader.py | Dit bestand bevat een class waarin de PDF’s in gelezen worden. Dit wordt gedaan met tabula. Dit is een package waarmee PDF’s makkelijk ingelezen kunnen worden. Uit de PDF’s wordt de volgende data gehaald: profile en conditions or symptoms. Ook wordt de data gemapped tegen de data in de database. |
| Vcf_reader.py | Dit bestand bevat een class waarin de VCF’s in gelezen worden. Er worden hier verschillende dingen uit op gehaald: chromosoom nummer, gene, type, positie van het aminozuur, de lengte van het aminozuur en wat de mutatie is. Ook wordt de data gemapped tegen de data in de database. |
| Inserter.py | Dit bestand vult de database met de data die uit de twee data readers komt.|

## Workflow
![workflow](https://github.com/Thijsch/DataIntegration/blob/master/workflow_data_integratie.png)

## Bronvermelding
- Odysseus Data Services. (2015). Athena. Athena. Geraadpleegd op 30 mei 2022, van https://athena.ohdsi.org/
- Szego, M., & Scherer, S. (z.d.). PGP Canada - Personal Genome Project Canada. PGP Canada - Personal Genome Project Canada. Geraadpleegd op 30 mei 2022, van https://personalgenomes.ca/

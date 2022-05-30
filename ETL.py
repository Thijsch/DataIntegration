# Thijs Ermens
# 25-4-2022
# Script dat de genomische data gewonnen van VEP in de OMOP database laad

import data_reader


def load_to_omop(path):
    lijst = data_reader.vcf_reader(path)
    print(lijst)


if __name__ == '__main__':
    Kollomnamen = ['Uploaded_variation', 'Location', 'Allele', 'Gene',
                   'Feature', 'Feature_type', 'Consequence',
                   'cDNA_position',
                   ' CDS_position', 'Protein_position', 'Amino_acids',
                   'Codons', 'Existing_variation', 'Extra'], \
                  ['chrM_73_G/A', 'chrM:73', 'A', 'ENSG000000',
                   'ENST00000',
                   'Transcript', 'upstream_gene_variant', '-', '-',
                   '-', '-',
                   '-', 'IMPACT=MODIFIER;DISTANCE']
    print(Kollomnamen)

    path = "vcfs/PGPC_0013_S1.flt.vcf"
    load_to_omop(path)

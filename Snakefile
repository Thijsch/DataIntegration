# Thijs Ermens
# 23-5-2022
# Met dit snakefile kan snpEFF gerund worden over de vcf files. Deze data
# wordt vervolgens ingelezen en in de database gezet
from PDF_reader import PdfReader
from Vcf_reader import VcfReader
from inserter import Inserter
import glob
from pathlib import Path

# TODO paths as command line arguments or in .env
raw = []
for name in glob.glob('data/10_variants/*.vcf'):
    raw.append(name)

# rule snpEFF:
#     """
#     Bij deze rule wordt de input door de app snpEFF heel gehaald. Output zal in
#     """
#     input: raw
#     output: Path({raw}).stem
#     shell:
#         "java -Xmx8g -jar snpEff.jar GRCh37.75 -no-downstream -no-intergenic -no-intron -no-upstream -no-utr -verbose -noStats {input} > {output}.snpEff.vcf"


vcf = []
pdf = []
print("hoi")
for name in glob.glob('data/10_variants/*.vcf'):
    vcf.append(name)

for name in glob.glob('data/pdf/*.pdf'):
    pdf.append(name)
pdf_reader = PdfReader(input_files=pdf,
    )
patient_list, conditions_list, patient_ids = pdf_reader.read_pdfs()
vcf_reader = VcfReader(input_files=vcf,
    patient_ids=patient_ids)
measurement_list = vcf_reader.read_vcfs()

inserter = Inserter(auto_commit=True,person=patient_list,
    condition_occurrence=conditions_list,
    measurement=measurement_list)
inserter.insert_data()
inserter.close_connection()

# Thijs Ermens
# 23-5-2022
# Met dit snakefile kan snpEFF gerund worden over de vcf files. Deze data
# wordt vervolgens ingelezen en in de database gezet
from pathlib import Path
import os
import glob
import dotenv

from PDF_reader import PdfReader
from Vcf_reader import VcfReader
from inserter import Inserter

dotenv.load_dotenv(".env")

# TODO paths as command line arguments or in .env
raw = []
vcf_dir = str(os.getenv("VCF_FILES"))
if vcf_dir.endswith("/"):
    vcf_dir = vcf_dir[:-1]

for name in glob.glob(f'{vcf_dir}/*.vcf'):
    raw.append(name)
    print(Path(name).stem)
    print(name)

# rule snpEFF:
#     """
#     Bij deze rule wordt de input door de app snpEFF heel gehaald. Output zal in
#     """
#     input: raw
#     output: raw
#     shell:
#         "java -Xmx8g -jar snpEff.jar GRCh37.75 -no-downstream
#         -no-intergenic -no-intron -no-upstream -no-utr -verbose -noStats {
#         input} > {output}.snpEff.vcf"


vcf_input_files = []
pdf_input_files = []
for name in glob.glob(f'{vcf_dir}/*.vcf'):
    vcf_input_files.append(name)

pdf_dir = str(os.getenv("PDF_FILES"))
if pdf_dir.endswith("/"):
    pdf_dir = pdf_dir[:-1]
for name in glob.glob(f'{pdf_dir}/*.pdf'):
    pdf_input_files.append(name)

if len(pdf_input_files) != len(vcf_input_files):
    raise Exception(
        "Amount of meta data files (pdf) does not match the amount of vcf files.")

pdf_reader = PdfReader(input_files=pdf_input_files,)
patient_list, conditions_list, patient_ids = pdf_reader.read_pdfs()
vcf_reader = VcfReader(input_files=vcf_input_files,
    patient_ids=patient_ids)
measurement_list = vcf_reader.read_vcfs()

inserter = Inserter(auto_commit=True,person=patient_list,
    condition_occurrence=conditions_list,
    measurement=measurement_list)
inserter.insert_data()
inserter.validate()
inserter.close_connection()

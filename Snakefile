import os
from PDF_reader import PdfReader
from Vcf_reader import VcfReader
from pprint import pprint
from inserter import Inserter
import glob


vcf = []
pdf = []

for name in glob.glob('data/10_variants/*.vcf'):
    vcf.append(name)

for name in glob.glob('data/pdf/*.pdf'):
    pdf.append(name)

concept_ids = {
    "missense": 43020565,
    "frameshift": 4209465,
    "Bipolar disorder": 436665,
    "Heartblock secondary catheter ablation for PAT": 43021509,
    "Uterine fibroids and polyps": 4147607,
    "Epilepsy (7-10 y)": 380378,
    "Arthritis": 4291025,
    "M": 8507,
    "F": 8532,
    "White": 8527
}

rule all:

rule snpEFF:
    input: vcf
    output: "data/10_variants"

    shell:
        "java -Xmx8g -jar snpEff.jar GRCh37.75 -no-downstream -no-intergenic -no-intron -no-upstream -no-utr -verbose -noStats *.chr21.vcf > *.chr21.snpEff.vcf"

rule pdf_reader:
    input: pdf

rule vcf_reader:
    input: vcf

rule inserter:
    input:
        vcf

    ## Installeer snpEff via source
    # https://pcingola.github.io/SnpEff/download/

    ## Run SNPeff
    ### Verander filenames in commando
    ### Het kan zijn dat je na een paar minuten op enter moet drukken om de output te zien
    # "java -Xmx8g -jar snpEff.jar GRCh37.75 -no-downstream -no-intergenic -no-intron -no-upstream -no-utr -verbose -noStats *.chr21.vcf > *.chr21.snpEff.vcf"

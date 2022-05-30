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

# rule all:
#     input:
#         "out.snpEFF.vcf"
#     shell:
#         print("hoi")

rule snpEFF:
    """
    Bij deze rule wordt de input door de app snpEFF heel gehaald. Output zal in
    """
    input: "/home/daaf/Downloads/PGPC_0018_S1_chr21.flt.vcf"
    output: "out"
    shell:
        f"java -Xmx8g -jar {os.getenv("SNPEFF_FILE")} GRCh37.75 "
        "-no-downstream -no-intergenic -no-intron -no-upstream -no-utr -verbose -noStats {input} > {output}.snpEff.vcf"




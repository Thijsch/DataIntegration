# 23-5-2022
# Met dit snakefile kan snpEFF gerund worden over de vcf files. Deze data
# wordt vervolgens ingelezen en in de database gezet
from pathlib import Path
import os
# import dotenv

# dotenv.load_dotenv(".env")
import snaketwo
from snaketwo import snakeextra


rule snpEFF:
    """
    Bij deze rule wordt de input door de app snpEFF heen gehaald. Output zal in
    """
    input:
        "/home/thijsch/PycharmProjects/DataIntegration/data/vcf_raw/PGPC_0018_S1_chr21.flt.vcf"
    output:
        "out"
    params:
        path="/home/thijsch/snpEff/snpEff.jar"
    shell:
        "java -Xmx8g -jar {params.path} GRCh37.75 -no-downstream -no-intergenic "
        "-no-intron -no-upstream -no-utr -verbose -noStats {input} > {output}.snpEff.vcf"

rule steptwo:
    """ 
    """
    input: "out.snpEff.jar"
    run:
        """snaketwo.snakeextra()"""

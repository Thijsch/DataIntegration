# 23-5-2022
# Thijs Ermens
# Met dit snakefile kan snpEFF gerund worden over de vcf files. Deze data
# wordt vervolgens ingelezen en in de database gezet
from pathlib import Path
import os
import dotenv

dotenv.load_dotenv(".env")
import snaketwo
from snaketwo import snakeextra

from os import listdir
from os.path import isfile, join

MYPATH = os.getenv("VCF_DIR")
if MYPATH.endswith('/'):
    os.getenv("VCF_DIR")[:-1]
print(MYPATH)
INPUT_FILES = [f for f in listdir(MYPATH) if isfile(join(MYPATH, f))]
print(INPUT_FILES)

rule snpEFF:
    """
    With this rule the input in the map data/10_variants will be put through
     snpEff and will go to the map data/10_variants/output where it can be
     processed in the next rule
    """
    input:
        expand("{mypath}/{input_files}",mypath=MYPATH,input_files=INPUT_FILES)
    output:
        "out"
    params:
        path="/home/daaf/snpEff/snpEff.jar"
    shell:
        "java -Xmx8g -jar {params.path} GRCh37.75 -no-downstream -no-intergenic "
        "-no-intron -no-upstream -no-utr -verbose -noStats {input} > {output}.snpEff.vcf"

rule steptwo:
    """
    This rule calls the python funcion snakeextra() from snaketwo to insert
    data in database
    """
    run:
        snakeextra()

# 23-5-2022
# Met dit snakefile kan snpEFF gerund worden over de vcf files. Deze data
# wordt vervolgens ingelezen en in de database gezet
import glob
import json
import os
from datetime import datetime
from pathlib import Path

import dotenv

from inserter import Inserter
from PDF_reader import PdfReader
from Vcf_reader import VcfReader

dotenv.load_dotenv(".env")


def snakeextra():
    """
        This function will put the data in the map VCF_FILES to the database
    """
    get_metadata()
    # get files
    raw = []
    vcf_dir = str(os.getenv("VCF_FILES"))
    if vcf_dir.endswith("/"):
        vcf_dir = vcf_dir[:-1]

    for name in glob.glob(f'{vcf_dir}/*.vcf'):
        raw.append(name)
        print(Path(name).stem)
        print(name)

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

    pdf_reader = PdfReader(input_files=pdf_input_files, )
    patient_list, conditions_list, patient_ids = pdf_reader.read_pdfs()
    vcf_reader = VcfReader(input_files=vcf_input_files,
                           patient_ids=patient_ids)
    measurement_list = vcf_reader.read_vcfs()

    # insert into database
    inserter = Inserter(auto_commit=True, person=patient_list,
                        condition_occurrence=conditions_list,
                        measurement=measurement_list)
    inserter.insert_data()
    inserter.validate()
    inserter.close_connection()


def get_metadata():
    """Get metadata for workflow"""
    metadata = {
        "time": str(datetime.now()),
        "vcf files": str(os.getenv("VCF_DIR")),
        "pdf_files": str(os.getenv("PDF_DIR")),
        "snpeff file": str(os.getenv("SNPEFF_FILE")),
        "run by user": str(os.getenv("USER"))
    }

    with open('metadata.json', 'w') as fp:
        json.dump(metadata, fp, indent=4)

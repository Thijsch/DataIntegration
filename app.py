from PDF_reader import PdfReader
from Vcf_reader import VcfReader
from snpeff import SnpEff
from inserter import Inserter
import glob
import os
import dotenv

dotenv.load_dotenv(".env")

def main():
    snpeff = SnpEff(str(os.getenv("VCF_DIR")), str(os.getenv("SNPEFF_FILE")))
    snpeff.run()
    vcf_dir = snpeff.output_path

    pdf_dir = str(os.getenv("PDF_DIR"))
    if pdf_dir.endswith("/"):
        pdf_dir = pdf_dir[:-1]
    pdf_input_files = [
        name for name in glob.glob(f'{pdf_dir}/*.pdf')
    ]

    if vcf_dir.endswith("/"):
        vcf_dir = vcf_dir[:-1]

    vcf_input_files = [
        name for name in glob.glob(f'{vcf_dir}/*.vcf')
    ]

    if len(pdf_input_files) != len(vcf_input_files):
        raise Exception("Amount of meta data files (pdf) "
                        "does not match the amount of vcf files.")

    pdf_reader = PdfReader(input_files=pdf_input_files)
    patient_list, conditions_list, patient_ids = pdf_reader.read_pdfs()

    vcf_reader = VcfReader(input_files=vcf_input_files,
                           patient_ids=patient_ids)
    measurement_list = vcf_reader.read_vcfs()

    inserter = Inserter(
        auto_commit=True,
        person=patient_list,
        condition_occurrence=conditions_list,
        measurement=measurement_list
    )

    inserter.insert_data()
    inserter.validate()
    inserter.close_connection()


if __name__ == "__main__":
    main()

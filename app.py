from PDF_reader import PdfReader
from Vcf_reader import VcfReader
from inserter import Inserter
import glob
import os



def main():
    pdf_input_files = [
        name for name in glob.glob('data/pdf/*.pdf')
    ]

    vcf_dir = str(os.getenv("VCF_FILES"))
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

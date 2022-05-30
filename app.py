from PDF_reader import PdfReader
from Vcf_reader import VcfReader
from inserter import Inserter


def main():
    pdf_input_files = [
        "data/pdf/PGPC-13.pdf",
        "data/pdf/PGPC-18.pdf",
        "data/pdf/PGPC-48.pdf",
    ]
    vcf_input_files = [
        "data/10_variants/PGPC_0013_S1_chr21_out_filtered_10.flt.vcf",
        "data/10_variants/PGPC_0018_S1_chr21_out_filtered_10.flt.vcf",
        "data/10_variants/PGPC_0048_S1_chr21_out_filtered_10.flt.vcf"
    ]

    pdf_reader = PdfReader(input_files=pdf_input_files)
    patient_list, conditions_list, patient_ids = pdf_reader.read_pdfs()

    vcf_reader = VcfReader(input_files=vcf_input_files,
                           patient_ids=patient_ids)
    measurement_list = vcf_reader.read_vcfs()

    
    # TODO test
    inserter = Inserter(
        auto_commit=True,
        person=patient_list,
        condition_occurrence=conditions_list,
        measurement=measurement_list
    )

    inserter.insert_data()
    inserter.close_connection()
    
    
if __name__ == "__main__":
    main()
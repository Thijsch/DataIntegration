from PDF_reader import PdfReader
from Vcf_reader import VcfReader
from pprint import pprint
from inserter import Inserter


def main():
    pdf_input_files = [
        "/home/janneke/Documents/Data_integratie/DataIntegration/data/pdf/PGPC-13.pdf",
        "/home/janneke/Documents/Data_integratie/DataIntegration/data/pdf/PGPC-18.pdf",
        "/home/janneke/Documents/Data_integratie/DataIntegration/data/pdf/PGPC-48.pdf",
    ]
    vcf_input_files = [
        "/home/janneke/Documents/Data_integratie/DataIntegration/data/10_variants/PGPC_0013_S1_chr21_out_filtered_10.flt.vcf",
        "/home/janneke/Documents/Data_integratie/DataIntegration/data/10_variants/PGPC_0018_S1_chr21_out_filtered_10.flt.vcf",
        "/home/janneke/Documents/Data_integratie/DataIntegration/data/10_variants/PGPC_0048_S1_chr21_out_filtered_10.flt.vcf"
    ]

    concept_ids = {
        "missense": 43020565, 
        "frameshift":4209465,
        "Bipolar disorder": 436665, 
        "Heartblock secondary catheter ablation for PAT": 43021509, 
        "Uterine fibroids and polyps": 4147607, 
        "Epilepsy (7-10 y)": 380378, 
        "Arthritis": 4291025, 
        "M": 8507, 
        "F": 8532, 
        "White": 8527
    }

    pdf_reader = PdfReader(input_files=pdf_input_files, concept_ids=concept_ids)
    patient_list, conditions_list, patient_ids = pdf_reader.read_pdfs()
    pprint(patient_list)
    pprint(conditions_list)
    pprint(patient_ids)

    vcf_reader = VcfReader(input_files=vcf_input_files, concept_ids=concept_ids, patient_ids=patient_ids)
    measurement_list = vcf_reader.read_vcfs()
    pprint(measurement_list)
    
    inserter = Inserter(auto_commit=True, person=patient_list, condition_occurrence=conditions_list, measurement=measurement_list)
    # inserter.insert_data()
    # inserter.close_connection()
    
    
if __name__ == "__main__":
    main()
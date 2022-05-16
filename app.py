from PDF_reader import PdfReader
from pprint import pprint
import uuid
# from inserter import Inserter


def main():
    pdf_input_files = ["/home/janneke/Documents/Data_integratie/PGPC-13.pdf", "/home/janneke/Documents/Data_integratie/PGPC-18.pdf"]
    vcf_input_files = [
        "/home/janneke/Documents/Data_integratie/DataIntegration/data/10_variants/PGPC_0013_S1_chr21_out_filtered_10.flt.vcf",
        "/home/janneke/Documents/Data_integratie/DataIntegration/data/10_variants/PGPC_0018_S1_chr21_out_filtered_10.flt.vcf",
        "/home/janneke/Documents/Data_integratie/DataIntegration/data/10_variants/PGPC_0048_S1_chr21_out_filtered_10.flt.vcf"
    ]

    pdf_reader = PdfReader(input_files=pdf_input_files)
    vcf_reader = VcfReader(input_files=vcf_input_files)
    pdf_data = pdf_reader.read_pdfs()
    # pprint(pdf_data)
    reformat_data(pdf_data=pdf_data)
    # inserter = Inserter()
    # inserter.insert_data(input=pdf_data)
    
def reformat_data(pdf_data: dict[str, dict[str, str]]):
    """Format data to 2d lists with uuid's"""
    profile_list = []
    for patient, metadata in pdf_data.items():
        for key, value in metadata.items():
            if key == "condition_symptoms":
                print(value)
                pass
            elif key =="profile":
                person_id = str(uuid.uuid4())
                gender_concept_id = 8532 if value[2] == "F" else 8507
                year_of_birth = value[1]
                month_of_birth = value[0]
                race_concept_id = 0 #TODO
                ethnicity_concept_id = 0 #TODO
                person_source_value = patient
                gender_source_value = value[2]
                race_source_value = value[3]
                ethnicity_source_value = 0 #TODO
                profile_list.append([person_id, gender_concept_id, year_of_birth, month_of_birth, race_concept_id, ethnicity_concept_id, person_source_value, gender_source_value, race_source_value, ethnicity_source_value])
                # person_id, gender_concept_id, year_of_birth, month_of_birth, race_concept_id, ethnicity_concept_id, person_source_value, gender_source_value, race_source_value, ethnicity_source_value
    print(profile_list)
    
if __name__ == "__main__":
    main()
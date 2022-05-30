import os
import uuid
from datetime import datetime

import tabula as t
import psycopg


class PdfReader:
    def __init__(self, input_files: list[str]):
        self.input_files = input_files
        if not input_files:
            raise Exception("No metadata files (pdf) found")
        self.pdf_data = {}

    def read_pdfs(self) -> tuple[list[list], list[list], dict]:
        """Parse all vcf files.

        Returns:
            list[list]: Lists ready for import into to the database.

        Returns:
            tuple[
                list[list]: List with person data ready for import into
                to the database.
                list[list]: List with condition symptoms data ready for
                import into to the database.
                dict: Person ids with source patient ids.
            ]
        """
        # TODO as command line arguments
        self.conn = psycopg.connect("dbname='onderwijs' "
                                    "user='DI_groep_7' "
                                    "host='postgres.biocentre.nl' "
                                    "password='blaat1234'")

        try:
            for input_file in self.input_files:
                output_file = self.convert_to_csv(input_file)
                dict_, participant = self.read_csv(output_file)
                profile, condition_symptoms = \
                    self.get_conditions_symptoms(dict_)
                self.pdf_data[participant] = {
                    "condition_symptoms": condition_symptoms,
                    "profile": profile}
                os.remove(output_file)

            pdf_list, conditions_list, patient_ids = self.reformat_data(
                self.pdf_data)
        except:  # Make sure that the connection in clossed when there's
            # an exception
            raise
        finally:
            self.conn.close()
        return pdf_list, conditions_list, patient_ids

    def convert_to_csv(self, input_file):
        """_summary_

        Args:
            input_file (_type_): _description_

        Returns:
            _type_: _description_
        """
        out = input_file.split(".")[0] + "_out" + "." + input_file.split(".")[
            1]
        t.convert_into(input_file, out, pages="all")
        return out

    def read_csv(self, input):
        pdf = {}
        participant = ""

        with open(input) as file:
            for line in file:
                if line.startswith("Participant"):
                    pdf[line] = []
                else:
                    pdf[list(pdf)[-1]].append(line)
                    participant = line.split(",")[0]
        return pdf, participant

    def get_conditions_symptoms(self, csv):
        conditions_symptom = []
        profile = []
        for keys, values in csv.items():
            if "Conditions or Symptom" in keys:
                for value in values:
                    conditions_symptom.append(value.strip().split(",")[1])
            elif "Birth month" in keys:
                for value in values:
                    profile = (value.strip().split(",")[1::])
        return profile, conditions_symptom

    def make_csv(self, profile, conditions_symptom, name, participant):
        file_name = name.split(".")[0] + "_Conditions_or_Symptom" + ".csv"
        with open(file_name, "w") as file:
            file.write(participant + ",")

            for i in range(len(profile)):
                if i + 1 < len(profile):
                    file.write(profile[i] + ",")
                else:
                    file.write(profile[i])

            file.write(participant + ",")

            for i in range(len(conditions_symptom)):
                if i + 1 < len(conditions_symptom):
                    file.write(conditions_symptom[i] + ",")
                else:
                    file.write(conditions_symptom[i])

    def reformat_data(self, pdf_data: dict[str, dict[str, str]]):
        """Format data to 2d lists with uuid's"""
        profile_list = []
        conditions_list = []
        patient_ids = {}
        for patient, metadata in pdf_data.items():
            patient_data = metadata["profile"]
            person_id = int(str(uuid.uuid4().int)[-9:-1])
            gender_concept_id = self.get_concept_id([patient_data[2]])
            year_of_birth = patient_data[1]
            month_of_birth = patient_data[0]
            race_concept_id = self.get_concept_id([patient_data[3]])
            ethnicity_concept_id = self.get_concept_id([patient_data[3]])
            person_source_value = patient
            gender_source_value = patient_data[2]
            race_source_value = patient_data[3]
            ethnicity_source_value = patient_data[3]
            profile_list.append(
                [person_id, gender_concept_id, year_of_birth, month_of_birth,
                 race_concept_id, ethnicity_concept_id, person_source_value,
                 gender_source_value, race_source_value,
                 ethnicity_source_value])

            patient_ids[person_source_value] = person_id

            for condition in metadata["condition_symptoms"]:
                condition_occurrence_id = int(str(uuid.uuid4().int)[-9:-1])
                condition_concept_id = self.get_concept_id([condition])
                condition_start_date = datetime(1970, 1, 1)
                condition_type_concept_id = 0  # TODO uhhhh wat is dit?
                conditions_list.append(
                    [condition_occurrence_id, person_id, condition_concept_id,
                     condition_start_date, condition_type_concept_id])

        return profile_list, conditions_list, patient_ids

    def get_concept_id(self, value):
        """
        Get the concept id out of the database by looking for the source
        value in the table mapping
        :param value: Source value
        :return: The concept id
        """
        if type(value) == list:
            value = value[0]

        cur = self.conn.cursor()
        cur.execute(f"""
            SELECT concept_id 
            FROM di_groep_7.mapping 
            WHERE source_value = '{value}';
        """)
        try:
            rows = cur.fetchall()
            return int(rows[0][0])
        except IndexError:
            return 0

import tabula as t
import os

class PdfReader:
    def __init__(self, input_files: list[str]):
        pdf_data = {}
        self.input_files = input_files
        
        for input_file in self.input_files:
            output_file = self.convert_to_csv(input_file)
            dict_, participant = self.read_csv(output_file)
            profile, condition_symptoms = self.get_conditions_symptoms(dict_)
            for i in [profile, condition_symptoms, participant]:
                print(i)
            pdf_data[participant] = {"condition_symptoms": condition_symptoms, "profile": profile}
            os.remove(output_file)
            # self.make_csv(profile, condition_symptoms, input_file, participant)
        
        return pdf_data
        
    def convert_to_csv(self, input_file):
        out = input_file.split(".")[0] + "_out" + "." + input_file.split(".")[1]
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
        with open(file_name,"w") as file:
            file.write(participant+",")

            for i in range(len(profile)):
                if i+1 < len(profile):
                    file.write(profile[i]+",")
                else:
                    file.write(profile[i])

            file.write(participant+",")

            for i in range(len(conditions_symptom)):
                if i+1 < len(conditions_symptom):
                    file.write(conditions_symptom[i]+",")
                else:
                    file.write(conditions_symptom[i])

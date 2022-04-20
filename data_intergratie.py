import tabula as t


def convert_to_csv(input):
    out = input_file.split(".")[0] + "_out" + "." + input_file.split(".")[1]
    t.convert_into(input, out, pages="all")
    return out


def read_csv(input):
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


def get_conditions_symptoms(csv):
    conditions_symptom = []
    profile = []
    for keys, values in csv.items():
        if "Conditions or Symptom" in keys:
            for value in values:
                conditions_symptom.append(value.split(",")[1])
        elif "Birth month" in keys:
            for value in values:
                profile = (value.split(",")[1::])
    return profile, conditions_symptom


def make_csv(profile, conditions_symptom, name, participant):
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


if __name__ == '__main__':
    input_file = "PGPC-13.pdf"
    output_file = convert_to_csv(input_file)
    dict_, participant = read_csv(output_file)
    profile, c_s = get_conditions_symptoms(dict_)
    make_csv(profile, c_s, input_file, participant)

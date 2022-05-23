import re
import uuid
import datetime

class VcfReader:
    def __init__(self, input_files: list[str], concept_ids, patient_ids):
        self.input_files = input_files        
        self.patient_ids = patient_ids       
        self.measurement = []
        self.concept_ids = concept_ids
        
    def read_vcfs(self) -> list[list]:
        """Parse all vcf files.

        Returns:
            list[list]: Lists ready for import into to the database.
        """
        for input_file in self.input_files:
            self.read_vcf(file=input_file)
        return self.measurement

    def read_vcf(self, file):
        """
        Functie die een file als input neemt en als output een lijst met
        variabelen uit een vcf file geeft
        :param file: string, pad naar het vcf file
        """
        person_id = 0
        date_time = datetime.datetime.now()
        pattern = r';[^\|]*\|(?P<type>[a-z]+)_[a-z]+\|[^;\|]*\|(?P<gene>[^;\|]+)\|([^;\|]*\|){6}(?P<AAchange>p.(?P<ref>[A-z]+)(?P<pos>[0-9]+)(?P<alt>[A-z]+))\|([^;\|]*\|){2}(?P<AApos>[0-9]+)/(?P<AAlength>[0-9]+)\|'
        with open(file) as infile:
            for line in infile:
                if line.startswith("#"):
                    match = re.search(r'#CHROM.*?(?P<person_id_str>[A-Z]+)_00(?P<person_id_int>[0-9]+)', line)
                    if match:
                        person_id = self.patient_ids[f"{str(match.group('person_id_str'))}-{str(match.group('person_id_int'))}"]
                    match = match = re.search(r'^##startTime=[A-z]+\s(?P<month>[A-z]{3})\s(?P<day>[0-9]{,2})\s(?P<time>[0-9]{,2}:[0-9]{,2}:[0-9]{,2})\s[0-9]{2}(?P<year>[0-9]{2})', line)
                    if match:
                        datetime_object = datetime.datetime.strptime(match.group('month'), "%b")
                        month_number = datetime_object.month if len(str(datetime_object.month)) > 1 else f"0{datetime_object.month}"
                        date_time_str = f"{match.group('day')}/{month_number}/{match.group('year')} {match.group('time')}"
                        date_time = datetime.datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
                
                elif line.strip():
                    match = re.search(pattern, line)
                    assert match, f"Line does not match the requested format:\n'{line}'"
                    self.measurement.append([
                        uuid.uuid4().int,                       # measurement_id
                        person_id,                              # person_id
                        match.group('gene'),                 # TODO measurement_concept_id gen uit db halen (match.group('gene') gebruiken)
                        date_time.date,                         # measurement_date
                        date_time,                              # measurement_datetime
                        self.concept_ids[match.group('type')],  # 'measurement_type_concept_id
                        37394434,                               # unit_concept_id
                        match.group('AApos'),                   # range_low
                        match.group('AAlength'),                # range_high
                        match.group('AAchange')                 # measurement_source_value
                    ])

import datetime
import re
import uuid

import psycopg


class VcfReader:
    def __init__(self, input_files: list[str], patient_ids):
        self.input_files = input_files
        if not input_files:
            raise Exception("No metadata files (pdf) found")
        self.patient_ids = patient_ids
        self.measurement = []

    def read_vcfs(self) -> list[list]:
        """Parse all vcf files.

        Returns:
            list[list]: Lists ready for import into to the database.
        """
        self.conn = psycopg.connect("dbname='onderwijs' user='DI_groep_7' "
                                    "host='postgres.biocentre.nl' "
                                    "password='blaat1234'")
        try:
            for input_file in self.input_files:
                self.read_vcf(file=input_file)
        except:
            raise
        finally:
            self.conn.close()
        return self.measurement

    def read_vcf(self, file):
        """Parse values for condition_occurence table in database
        from vcf files.
        
        Args:
            file (str): Path to the vcf file.
        """
        person_id = 0
        date = datetime.datetime.now()
        pattern = r';[^\|]*\|(?P<type>[a-z]+)_[a-z]+\|[^;\|]*\|' \
                  r'(?P<gene>[^;\|]+)\|([^;\|]*\|){6}' \
                  r'(?P<AAchange>p.(?P<ref>[A-z]+)(?P<pos>[0-9]+)' \
                  r'(?P<alt>[A-z]+))\|([^;\|]*\|){2}' \
                  r'(?P<AApos>[0-9]+)/(?P<AAlength>[0-9]+)\|'
        with open(file) as infile:
            for line in infile:
                if line.startswith("#"):
                    new_person_id = self.search_person_id(line)
                    if new_person_id:
                        person_id = new_person_id

                    new_date = self.search_date(line)
                    if new_date:
                        date = new_date

                elif line.strip():
                    match = re.search(pattern, line)
                    assert match, f"Line does not match the requested " \
                                  f"format:\n'{line}' "
                    self.measurement.append([
                        # measurement_id
                        int(str(uuid.uuid4().int)[-9:-1]),
                        # person_id
                        person_id,
                        # concept_id
                        self.get_gene_concept_id(match.group('gene')),
                        # measurement_date
                        date,
                        # 'measurement_type_concept_id
                        self.get_concept_id(match.group('type')),
                        # unit_concept_id
                        37394434,
                        # range_low
                        match.group('AApos'),
                        # range_high
                        match.group('AAlength'),
                        # measurement_source_value
                        match.group('AAchange')
                    ])

    def search_person_id(self, line: str) -> str | None:
        """Search line for person id.

        Args:
            line (str): Line to search for the person_id.

        Raises:
            Exception: When the person id is not present in the metadata.

        Returns:
            str | None: String of person id if found in line
        """
        match = re.search(
            r'#CHROM.*?(?P<person_id_str>[A-Z]+)_00'
            r'(?P<person_id_int>[0-9]+)',
            line
        )
        if match:
            try:
                return self.patient_ids[
                    f"{str(match.group('person_id_str'))}-" 
                    f"{str(match.group('person_id_int'))}"]
            except KeyError:
                raise Exception(
                    f"Patient with id {str(match.group('person_id_str'))}-"
                    f"{str(match.group('person_id_int'))} "
                    f"not found in metadata (pdf) files."
                )
        else:
            return None

    def search_date(self, line):
        match = match = re.search(
            r'^##startTime=[A-z]+'
            r'\s(?P<month>[A-z]{3})'
            r'\s(?P<day>[0-9]{,2})'
            r'\s(?P<time>[0-9]{,2}:[0-9]{,2}:[0-9]{,2})'
            r'\s[0-9]{2}(?P<year>[0-9]{2})',
            line)
        if match:
            datetime_object = datetime.datetime.strptime(
                match.group('month'), "%b")
            month_number = datetime_object.month
            return datetime.datetime(int(match.group('year')),
                                     month_number,
                                     int(match.group('day')))
        else:
            return None

    def get_gene_concept_id(self, gene):
        """
        Get the concept id out of the database by looking for the name
        of the gene in the table concept_name
        :param gene: Name of the gene
        :return: The concept id
        """
        cur = self.conn.cursor()
        cur.execute(f"""
            SELECT concept_id
            FROM di_groep_7.concept concept 
            WHERE concept.concept_name SIMILAR TO '{gene} %'  AND
            concept.concept_class_id = 'Genetic Variation';
        """)
        try:
            rows = cur.fetchall()
            return int(rows[0][0])
        except IndexError:
            return 0

    def get_concept_id(self, value):
        """
        Get the concept id out of the database by looking for the
        source value in the table mapping.
        :param value: Source value
        :return: The concept id
        """
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

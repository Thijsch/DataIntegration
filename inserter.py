# pyright: reportUnknownMemberType=false
import psycopg


class Inserter:
    def __init__(self, auto_commit: bool, person, condition_occurrence,
                 measurement):
        self.conn = psycopg.connect("dbname='onderwijs' user='DI_groep_7' "
                                    "host='postgres.biocentre.nl' "
                                    "password='blaat1234'")

        self.conn.autocommit = auto_commit

        self.data_to_insert = {
            "person": person,
            "condition_occurrence": condition_occurrence,
            "measurement": measurement
        }

        self.tables: dict[str, str] = {
            "person": "COPY person (person_id, gender_concept_id, year_of_birth, month_of_birth, race_concept_id, ethnicity_concept_id, person_source_value, gender_source_value, race_source_value, ethnicity_source_value) FROM STDIN",
            "condition_occurrence": "COPY condition_occurrence (condition_occurrence_id, person_id, condition_concept_id, condition_start_date, condition_type_concept_id) FROM STDIN",
            "measurement": "COPY measurement (measurement_id, person_id, measurement_concept_id, measurement_date, measurement_type_concept_id, unit_concept_id, range_low, range_high, measurement_source_value) FROM STDIN",
        }

    def insert_data(self) -> None:
        """Insert a copy into the database.

        Args:
            postgres_records (list[list]): List with data for every record.
            table (str): What table to insert the data into.
        """
        cursor = self.conn.cursor()
        for table, query in self.tables.items():
            postgres_records = self.data_to_insert[table]
            with cursor.copy(query) as copy:
                for record in postgres_records:
                    print(record)
                    copy.write_row(record)

    def close_connection(self):
        """Close connection to database."""
        self.conn.close()

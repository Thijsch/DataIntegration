# pyright: reportUnknownMemberType=false
import psycopg
import traceback


class Inserter:
    def _init_(self, auto_commit: bool, log_file: str | None = None):
        self.conn = psycopg.connect("")

        self.conn.autocommit = auto_commit

        self.log_file = log_file

        self.tables: dict[str, str] = {
            "person": "COPY person (person_id, gender_concept_id, year_of_birth, month_of_birth, race_concept_id, ethnicity_concept_id, person_source_value, gender_source_value, race_source_value, ethnicity_source_value) FROM STDIN",
        }

        self.properties: dict[str, tuple] = {
            "assembly": (
                "uuid",
                "organism",
                "date_added",
                "assembly_identifier",
            ),
            "molecule": (
                "uuid",
                "assembly_uuid",
                "accession",
                "molecule_type",
                "seq",
                "note",
            ),
            "feature": (
                "uuid",
                "molecule_uuid",
                "feature_type",
                "start_pos",
                "stop_pos",
                "strand",
                "locus_tag",
                "gene_name",
                "note",
                "labels",
            ),
            "component": (
                "uuid", 
                "feature_uuid", 
                "start_pos", 
                "stop_pos",
            )
        }
    
    def insert_data(self, input: dict[str, list]):
        """Insert data from grape opjects into database.

        Args:
            grape_data (dict[str, list]): List of grape objects for every table in the database.
        """
        for table, data in input.items():
            postgres_records = []
            for row in data:
                record = []
                for property in self.properties[table]:
                    record.append(getattr(row, property))
                postgres_records.append(record)
            self.insert_copy(postgres_records, table)

    def insert_copy(self, postgres_records: list[list], table: str) -> None:
        """Insert a copy into the database.

        Args:
            postgres_records (list[list]): List with data for every record.
            table (str): What table to insert the data into.
        """
        cursor = self.conn.cursor()
        with cursor.copy(self.tables[table]) as copy:
            for record in postgres_records:
                try:
                    copy.write_row(record)
                except psycopg.errors.BadCopyFileFormat:
                    full_traceback = traceback.format_exc()
                    if self.log_file:
                        with open(self.log_file, "a") as insert_errors:
                            insert_errors.write(f'Error occured during record: {record}')
                            insert_errors.write(f"{full_traceback}\n\n")
                    print(f"File record: {record}\nException occured: {full_traceback}")
    
    def close_connection(self):
        """Close connection to database."""
        self.conn.close()
        
from .diagram_results import DiagramResults
from ...db_models.database import Database
import os
import subprocess


# I'm trying to generate those diagrams and put in format like we have for the output folder of schemaspy
# So from eralchemy you can specify mode in render_er function to generate either graph or dot file.
# We want graph and dot file for each of the tables
# We also want the logic for handling error when generating diagrams
# Frontend might have some logic to handle compact, so we want to remove that, and we have to change the syntax of the html from mustache to jinja too


class DiagramFactory:
    def __init__(self, output_dir: str):
        self.diagram_dir = output_dir + "/diagrams"
        self.dirs = {
            "table": self.diagram_dir + "/tables",
            "summary": self.diagram_dir + "/summary",
            "orphan": self.diagram_dir + "/orphans",
        }
        self.create_dirs()

    def create_dirs(self):
        for path in self.dirs:
            try:
                os.mkdir(self.dirs[path])
                print("createdddddddddddd")
            except OSError as error:
                continue

    @staticmethod
    def generate_summary_diagram(database_url=None, dot_file_name=None, diagram_file_name=None):
        cmd = "eralchemy -i 'mysql+pymysql://root:password@localhost:3306/classicmodels'  -o erd_froms_sqlite.dot"
        cmd2 = "eralchemy -i 'mysql+pymysql://root:password@localhost:3306/classicmodels'  -o erd_froms_sqlite.png"
        subprocess.call(
            cmd, shell=True, cwd="dataprep/eda/create_db_report/output/diagrams/summary"
        )
        subprocess.call(
            cmd2, shell=True, cwd="dataprep/eda/create_db_report/output/diagrams/summary"
        )

    @staticmethod
    def generate_table_diagrams(database_object: Database):
        cmd3 = "eralchemy -i 'mysql+pymysql://root:password@localhost:3306/classicmodels' -o {file_name}.dot --exclude-tables {table_names}"
        cmd4 = "eralchemy -i 'mysql+pymysql://root:password@localhost:3306/classicmodels' -o {file_name}.png --exclude-tables {table_names}"
        database_tables = database_object.get_tables_dict()
        table_names = set(database_tables.keys())
        for table in table_names:
            related_table_names = set()
            related_table_names.add(table)
            ref = database_tables[table].get_referenced_by_tables()
            for j in ref:
                related_table_names.add(j)
            table_foreignkeys = database_tables[table].get_foreign_keys_dict()
            for foreign_key in table_foreignkeys:
                related_table_names.add(
                    table_foreignkeys[foreign_key].get_parent_table().get_name()
                )
            print("TABLE NAME: ", table)
            print("RELATED TBALES: ", related_table_names)
            filter_tables = list(table_names - related_table_names)
            filter_tables_string = " ".join(x for x in filter_tables)
            print(filter_tables_string)
            cmd3 = cmd3.format(file_name=table, table_names=filter_tables_string)
            cmd4 = cmd4.format(file_name=table, table_names=filter_tables_string)
            subprocess.call(
                cmd3, shell=True, cwd="dataprep/eda/create_db_report/output/diagrams/tables"
            )
            subprocess.call(
                cmd4, shell=True, cwd="dataprep/eda/create_db_report/output/diagrams/tables"
            )


"""
    def generate_diagram(self, diagram_type, dot_file, diagram_name):
        diagram_file = (
            f"{self.dirs[diagram_type]}/{diagram_name}.{self.diagram_producer.get_diagram_format()}"
        )
        diagram_map = self.diagram_producer.generate_diagram(dot_file, diagram_file)
        return DiagramResults(diagram_file, diagram_map, self.diagram_producer.get_diagram_format())
"""

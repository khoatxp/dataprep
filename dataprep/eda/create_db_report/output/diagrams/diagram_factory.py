import os
import shutil
from eralchemy import render_er
from ...db_models.database import Database


class DiagramFactory:
    def __init__(self, output_dir: str):
        self.cwd = os.getcwd()
        self.diagram_dir = output_dir + "/diagrams"
        self.dirs = {
            "table": self.diagram_dir + "/tables",
            "summary": self.diagram_dir + "/summary",
            "orphan": self.diagram_dir + "/orphans",
        }
        self.create_dirs()

    def create_dirs(self):
        if not os.path.exists(self.diagram_dir):
            os.mkdir(self.diagram_dir)
        for path in self.dirs:
            if os.path.exists(self.dirs[path]) and os.path.isdir(self.dirs[path]):
                shutil.rmtree(self.dirs[path])
            os.mkdir(self.dirs[path])

    @staticmethod
    def generate_summary_diagram(database_url, file_name):
        render_er(database_url, f"{file_name}.png")
        render_er(database_url, f"{file_name}.dot")

    def generate_table_diagrams(self, database_object: Database, database_url: str):
        database_tables = database_object.get_tables_dict()
        table_names = set(database_tables.keys())
        for table in table_names:
            related_table_names = set(table)
            related_table_names.update(database_tables[table].get_referenced_by_tables())
            table_foreign_keys = database_tables[table].get_foreign_keys_dict()
            for foreign_key in table_foreign_keys:
                related_table_names.add(
                    table_foreign_keys[foreign_key].get_parent_table().get_name()
                )
            exclude_tables = " ".join(list(table_names - related_table_names))
            os.chdir(self.dirs['table'])
            render_er(database_url, f"{table}.png", exclude_tables=exclude_tables)
            render_er(database_url, f"{table}.dot", exclude_tables=exclude_tables)
            os.chdir(self.cwd)


"""
    def generate_diagram(self, diagram_type, dot_file, diagram_name):
        diagram_file = (
            f"{self.dirs[diagram_type]}/{diagram_name}.{self.diagram_producer.get_diagram_format()}"
        )
        diagram_map = self.diagram_producer.generate_diagram(dot_file, diagram_file)
        return DiagramResults(diagram_file, diagram_map, self.diagram_producer.get_diagram_format())
"""

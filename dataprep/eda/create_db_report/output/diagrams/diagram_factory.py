from .diagram_results import DiagramResults
from eralchemy import render_er

class DiagramProducer:
    def get_implementation_details(self):
        pass

    @staticmethod
    def generate_diagram(dot_file, diagram_file):
        return 1

    def get_diagram_format(self):
        pass


# I'm trying to generate those diagrams and put in format like we have for the output folder of schemaspy
# So from eralchemy you can specify mode in render_er function to generate either graph or dot file.
# We want graph and dot file for each of the tables
# We also want the logic for handling error when generating diagrams
# Frontend might have some logic to handle compact, so we want to remove that, and we have to change the syntax of the html from mustache to jinja too

class DiagramFactory:
    def __init__(self, diagram_producer: DiagramProducer, output_dir):
        self.diagram_producer = diagram_producer
        self.diagram_dir = output_dir + "/diagrams"
        self.dirs = {
            "table": self.diagram_dir + "/tables",
            "summary": self.diagram_dir + "/summary",
            "orphan": self.diagram_dir + "/orphans"
        }
        self.create_dirs()

    def create_dirs(self):
        pass

    def generate_diagram(self, diagram_type, dot_file, diagram_name):
        diagram_file = f"{self.dirs[diagram_type]}/{diagram_name}.{self.diagram_producer.get_diagram_format()}"
        diagram_map = self.diagram_producer.generate_diagram(dot_file, diagram_file)
        return DiagramResults(diagram_file, diagram_map, self.diagram_producer.get_diagram_format())

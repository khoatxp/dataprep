class DiagramResults:
    def __init__(self, diagram_file, diagram_map, image_format):
        self.diagram_file = diagram_file
        if diagram_map is None:
            self.diagram_map = ""
            self.diagram_map_name = ""
        else:
            self.diagram_map = diagram_map
        self.image_format = image_format

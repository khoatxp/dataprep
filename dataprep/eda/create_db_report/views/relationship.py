from typing import List
from ..db_models.database import Database
from ..db_models.table import Table
from ..page_models.page_template import PageTemplate


class MainPage:
    def __init__(self, pystache_object: PageTemplate) -> None:
        self.pystache_object = pystache_object

    def page_writer(self, database: Database, tables: List[Table], new_file: str):
        """
        Compile the data needed by the pystache template for relationship page
        """
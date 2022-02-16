from abc import ABC, abstractmethod
from typing import Protocol

import pandas as pd



class BaseSource(ABC):
    """Basic representation of a Extractor class."""
    """
    Event handler which maintains a state machine for each path
    seen. When a file goes through the create, write, close sequence,
    notifies the created handler.
    """

    def __init__(self, filter, created_handler):
        self._files = {}
        self._filter = filter
        self._created_handler = created_handler

    @abstractmethod
    def process(self):
        pass

    # =======================================================
    # każdy page jest zapisywany w oddzielnym df
    def __init__(self, content):
        self.page_content = content
        self.extracted_data = pd.DataFrame

    def extract_websites(self):
        pass

    def extract_addresses(self):
        # odrazu dzielimy adres na ulicę, numer ulicy, numer mieszkania
        pass

    def extract_zip_codes(self):
        pass

    def extract_emails(self):
        pass

    def extract_mobile_phone_numbers(self):
        pass

    def extract_stationary_phone_numbers(self):
        pass

    def extract_nip(self):
        pass



if __name__ == '__main__':
    print(__package__)

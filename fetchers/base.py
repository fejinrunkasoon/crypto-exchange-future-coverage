from abc import ABC, abstractmethod
from typing import List, Dict


class BaseFetcher(ABC):
    
    @abstractmethod
    def fetch(self) -> List[Dict]:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass
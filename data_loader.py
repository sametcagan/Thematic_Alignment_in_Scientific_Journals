import arxiv
import pandas as pd
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
import os
import re
import time
import requests
from xml.etree import ElementTree as ET

class BaseJournalLoader(ABC):    
    def __init__(self, query: str, limit: int = 100):
        self.query = query
        self.limit = limit

    @abstractmethod
    def fetch_data(self, save_path = None) -> pd.DataFrame:
        """Fetch data from the source and return a cleaned DataFrame."""
        pass

class ArxivLoader(BaseJournalLoader):
    """
    Handles data acquisition from the arXiv API.
    """
    
    def __init__(self, query: str, limit: int = 500):
        # FIX: Only pass query and limit to the base class
        super().__init__(query, limit)
        self.client = arxiv.Client()

    def fetch_data(self, save_path = None) -> pd.DataFrame:
        """
        Executes search and parses results into a structured format.
        save_path : csv format, using sep as '|', and index = False
        """
        search = arxiv.Search(
            query=self.query,
            max_results=self.limit,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        results_list = []
        for result in self.client.results(search):
            results_list.append({
                "id": result.entry_id,
                "title": result.title,
                "abstract": result.summary.replace("\n", " "),
                "published": result.published,
                "year": result.published.year,
                "categories": result.categories
            })
        
        df = pd.DataFrame(results_list)
        
        if df.empty:
            print("No papers found for the given query.")
            return df

        print(f"Downloaded {len(df)} papers.")
        print(f"Time range: {df['year'].min()} to {df['year'].max()}")
        
        # Handle saving logic
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            df.to_csv(save_path, sep='|', index=False)
            
        return self._preprocess_dataframe(df)

    def _preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        if not df.empty:
            df['published'] = pd.to_datetime(df['published'])
        return df


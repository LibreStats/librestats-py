import requests
import pandas as pd
from io import StringIO

# GitHub repo config
ORG = "LibreStats"
REPO = "LibreStats"
BRANCH = "main"

# API & raw content URLs
API_BASE = f"https://api.github.com/repos/{ORG}/{REPO}/contents/datasets"
RAW_BASE = f"https://raw.githubusercontent.com/{ORG}/{REPO}/{BRANCH}/datasets"

def _fetch_json(url):
    """Fetch JSON metadata from the GitHub API."""
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

def list_domains():
    """
    List all dataset domains (folders) in the LibreStats repo.
    """
    data = _fetch_json(f"{API_BASE}?ref={BRANCH}")
    return [item["name"] for item in data if item["type"] == "dir"]

def list_datasets(domain=None):
    """
    List datasets inside a specific domain, or all datasets grouped by domain.

    Args:
        domain (str, optional): The dataset domain (folder). 
                                If None, returns all domains with datasets.
    """
    if domain:
        url = f"{API_BASE}/{domain}?ref={BRANCH}"
        data = _fetch_json(url)
        return [
            item["name"].replace(".csv", "")
            for item in data if item["type"] == "file" and item["name"].endswith(".csv")
        ]
    else:
        return {d: list_datasets(d) for d in list_domains()}

def load_dataset(domain, name):
    """
    Load a dataset from the LibreStats repo.

    Args:
        domain (str): The dataset domain (folder name).
        name (str): The dataset file name (without .csv).

    Returns:
        pd.DataFrame: The dataset with the first column set as the index.
    """
    url = f"{RAW_BASE}/{domain}/{name}.csv"
    resp = requests.get(url, timeout=10)

    if resp.status_code != 200:
        raise FileNotFoundError(f"Dataset not found: {domain}/{name}.csv")

    dataset = pd.read_csv(StringIO(resp.text))
    dataset.set_index(dataset.columns[0], inplace=True)
    return dataset

def get(df, row, col):
    """
    Get a value from the DataFrame by row & column.
    
    Args:
        df (variable): DataFrame where dataset is loaded.
        row (str): The Row name of the dataset
        col (str): The Column name of the dataset
    """
    try:
        value = df.loc[row, col]
        print(value)
    except KeyError:
        RED = "\033[91m"
        BLUE = "\x1b[34m"
        YELLOW = "\033[93m"
        RESET = "\033[0m"
        print(f"{RED}[ERROR] Data not Available{RESET}")
        print(f"{YELLOW}[INFO] Visit {BLUE}https://github.com/LibreStats/LibreStats{RESET} {YELLOW}to add data if you think it should be there!{RESET}")
 


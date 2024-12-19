# %%
import requests
from bs4 import BeautifulSoup
import os

# Local directory to save downloaded files
local_base_dir = "downloaded_gwas_data"

def download_file(file_url, local_path):
    """
    Download a file from a given URL to the specified local path.
    
    Parameters:
    -----------
    file_url : str
        The URL of the file to download.
    local_path : str
        The local filesystem path where the file should be saved.
    
    Returns:
    --------
    None
    """
    print(f"Downloading {file_url}...")
    response = requests.get(file_url, stream=True)
    # Open the file in binary-write mode
    with open(local_path, 'wb') as file:
        # Iterate over the response in chunks of 1024 bytes
        for chunk in response.iter_content(1024):
            file.write(chunk)
    print(f"Saved to {local_path}")

def parse_directory(url, local_dir):
    """
    Recursively parse an FTP/HTTP directory and download files of specified extensions.
    
    For each link found in the directory listing:
        - If it's a subdirectory (link ending with '/'), recursively parse that directory.
        - If it's a file with one of the specified extensions, download the file.
        - Otherwise, skip it.
    
    Parameters:
    -----------
    url : str
        The directory URL to parse.
    local_dir : str
        The local directory path where files or subdirectories will be saved.
    
    Returns:
    --------
    None
    """
    # Get the HTML content from the directory URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ensure the local directory structure exists
    os.makedirs(local_dir, exist_ok=True)

    # Iterate through all links (<a> tags) in the directory listing
    for link in soup.find_all("a"):
        name = link.get("href")
        
        # Skip links pointing to the parent directory
        if name in ("../", "Parent Directory"):
            continue

        # Construct the full URL and the local path
        full_url = url + name
        local_path = os.path.join(local_dir, os.path.basename(name))

        # Check if the link is a directory (ends with '/')
        if name.endswith("/"):
            parse_directory(full_url, local_path)
        # Download only specific file types
        elif any(name.endswith(ext) for ext in [".gz", ".txt", ".pdf", ".zip"]):
            download_file(full_url, local_path)
        else:
            print(f"Skipping non-downloadable link: {name}")

def main():
    base_url = input("Enter the URL: ")
    local_base_url = input()
    parse_directory(base_url, local_base_dir)
if __name__ == "__main__":
    main() 
# %%

# nPipeline: Nutrients Pipeline

## Overview

`nPipeline` is designed to facilitate the analysis of nutrient associations using GWAS data and current patient datasets. It includes scripts for mapping the closest associations (`map.py`) and validating these associations via the ChatGPT API (`gpt.py`).

## Repository Structure

Below is the structure of the `nPipeline` repository:

```
nPipeline/
|-- code/
|   |-- map.py            # Maps closest associations from GWAS data to patient data.
|   `-- gpt.py            # Validates associations using ChatGPT API.
|-- data/
|   |-- FormA706_20231010.xlsx      # The GUSTO dataset. It should be present in your own local directory, but due to data sensitivity, it is added to .gitignore
|   `-- gwas_catalog_v1.0.2-associations_e112_r2024-09-22.tsv
|   `-- gwas-catalog-v1.0.3.1-studies-r2024-09-22.tsv
|-- results/
|   |-- all_associations_traits.txt      
|   `-- formA_associations_50_matches.csv
|   `-- formA_description.txt
|-- requirements.txt      # Required libraries.
`-- README.md             # Documentation and setup instructions.
```

## Getting Started

### Prerequisites

To run the scripts in the `nPipeline` repository, you'll need to have Conda installed on your machine. If you do not have Conda installed, you can download it from [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution).

### Setting Up Your Environment

1. **Create a Conda Environment**: Open your terminal and create a new Conda environment by running:

   ```bash
   conda create --name your_env python=3.11
   ```

   Replace `python=3.8` with the version of Python you wish to use.

2. **Activate the Environment**:

   ```bash
   conda activate your_env
   ```

3. **Install Required Packages**:

   Navigate to the root directory of the `nPipeline` project where the `requirements.txt` file is located and run:

   ```bash
   conda install -r requirements.txt
   ```

### Running the Scripts

Once the environment is set up and all dependencies are installed, you can run the scripts as follows:

- **Map Associations**:

  ```bash
  python code/map.py
  ```

- **Validate Associations with GPT**:

  ```bash
  python code/gpt.py
  ```

## Contributing

Contributions to `nPipeline` are welcome! Please feel free to submit pull requests or open issues to suggest improvements or add new features.

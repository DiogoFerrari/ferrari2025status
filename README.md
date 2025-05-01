# Replication files 

This repository contains replication files for the article:

- Ferrari and Smith (2025) "Status Threat, Partisanship, and Voters' Conservative Shift toward Right-wing Candidates". *Journal of Experimental Political Science* (conditionally accepted)

# Citation

```latex
@article{ferrari2025status,
    author = {Ferrari, Diogo and Smith, Brianna},
    title = {Status Threat, Partisanship, and Voters' Conservative Shift toward Right-wing Candidates},
    year={2025},
    journal = {Journal of Experimental Political Science},
    volume = {(conditionally accepted)},
    issue = {},
    doi = {},
    url = {},
}
```

# This repository contains

1. Tables and figures
2. The scripts used to generate the analysis, tables, and figures
3. Data set(s) used in the analyses

# Pre-analysis plan

Available [here](https://osf.io/q5cha)

# Instructions for replication
### Option 1: Download the files manually

For replication, make sure you have the following folder structure in place
```ascii
.
├── man                              <- folder with the manuscript (limited if copyright applies)
│   ├── tables-and-figures           <- tables and figures (in .pdf, .png. etc) used in the manuscript
│   └── supp-material
│       └── tables-and-figures       <- tables and figures used in the online supplement
├── src                              <- scripts for replication
│   ├──data
│   │  └── final                     <- folder with data used in the analysis; codebook is here
│   └── model                        <- folder with the replication scripts
└── README.md                        <- this file
```

Follow the steps in the section [Replication](#replication)

### Option 2: Cloning from github

1. Donwload the replication files or clone the repository by running the following command in your terminal:

``` shell
git clone https://github.com/DiogoFerrari/ferrari2025status
```
2. Follow the steps in the section [Replication](#replication)

# Requirements and processing time

See `requiremente.txt` for modules used in the scripts.

The analysis was produced using the following hardware and software configuration:

```
System Information:
-------------------
Python implementation: CPython
Python version       : 3.12.3
IPython version      : 9.2.0

Compiler    : GCC 13.3.0
OS          : Linux
Release     : 6.8.0-57-generic
Machine     : x86_64
Processor   : x86_64
CPU cores   : 16
Architecture: 64bit

Memory available: 15.33 GB
Memory used: 1.69 GB

Modules used:
-------------
numpy         : 2.2.3
tidypolars4sci: 0.0.1.21
sys           : 3.12.3 (main, Feb  4 2025, 14:48:35) [GCC 13.3.0]
statsmodels   : 0.14.4
altair        : 5.5.0
tools4sci     : 0.0.1.22
json          : 2.0.9
psutil        : 7.0.0
watermark     : 2.5.0
re            : 2.2.1

Watermark: 2.5.0

```

Processing time:

```
Script: model.py
Code execution time: 0.9682 minutes
```

# Replication

Follow these steps to replicate the analysis:

##### 1. Navigate to the Project Folder
Open a terminal and change to the project `./src/` directory:
```bash
cd ./src/
```

##### 2. Create a Virtual Environment
Create a virtual environment named `.venv` inside `./src/`:
```bash
python -m venv .venv
```

##### 3. Activate the Virtual Environment
- **On Linux/macOS:**
```bash
source .venv/bin/activate
```
- **On Windows:**
```bash
.venv\Scripts\activate
```

You should see the virtual environment name `(venv)` in your terminal prompt.

##### 4. Install Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```
Also run:

```bash
pip install vl-convert-python xlsxwriter openpyxl
```

##### 6. Run the Python Script
Execute the script `model.py` located in `./src/model/`:
```bash
cd model
python model.py > model.log
```

##### 7. Deactivate the Virtual Environment (Optional)
When you are done running the script, you can deactivate the virtual environment:
```bash
deactivate
```


##### Summary of Commands

```bash
cd ./src/
python -m venv .venv
source .venv/bin/activate  # Use .venv\Scripts\activate on Windows
pip install -r requirements.txt
cd model
python model.py > model.log
deactivate  # Optional
```


from pathlib import Path
import os

print(f"Loading paths...", end='')

ROOT              = Path(os.path.abspath(os.curdir))
ROOT              = ROOT.parent.parent

# scripts
PATH_SRC          = ROOT / "src"
PATH_SRC_MODEL    = PATH_SRC / "model"
PATH_SRC_EDA      = PATH_SRC / "eda"
# data
PATH_DATA         = PATH_SRC / "data"
PATH_DATA_FINAL   = PATH_SRC / "data" / "final"
PATH_DATA_RAW     = PATH_SRC / "data" / "raw"
PATH_DATA_INTERIM = PATH_SRC / "data" / "interim"
# manuscript
PATH_MAN          = ROOT / "man"
PATH_FIGURES      = PATH_MAN / 'tables-and-figures'
PATH_TABLES       = PATH_MAN / 'tables-and-figures'
# online supplement
PATH_OS         = PATH_MAN / "supp-material"
PATH_OS_FIGURES = PATH_OS / 'tables-and-figures'
PATH_OS_TABLES  = PATH_OS / 'tables-and-figures'
# output
PATH_OUTPUTS      = ROOT / 'out'
# report
PATH_REPORTS      = ROOT / 'rep'
PATH_DOCS         = ROOT / 'docs'
# PRR
PATH_PRR          = PATH_DOCS / "prr"
PATH_PRR_FIGURES  = PATH_DOCS / "prr" / "tables-and-figures"
PATH_PRR_TABLES   = PATH_DOCS / "prr" / "tables-and-figures"
# PAP 
PATH_PAP          = PATH_DOCS / "pap"
PATH_PAP_FIGURES  = PATH_DOCS / "pap" / "tables-and-figures"
PATH_PAP_TABLES   = PATH_DOCS / "pap" / "tables-and-figures"

print('done!')

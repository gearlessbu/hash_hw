## Installation
```sh
conda env create -f environment.yml
conda activate hash
./install.sh
```
## Experiments
### Tabulation experiment
```sh
./build/Hash/dictionary/test_probing
python python/cum_frac.py
```
### Closest pair experiment
Download SIFT1M from http://corpus-texmex.irisa.fr. and unzip it in `datasets/`.
```sh
python python/nearest_neighbor.py
```
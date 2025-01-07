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
python python/histmap.py
```
### Closest pair experiment
Download SIFT1M from http://corpus-texmex.irisa.fr. and unzip it in `datasets/`.
```sh
python python/nearest_neighbor.py
```

## Compare LSH and DSH
```sh
python python/LSH.py
python python/DSH.py
python python/MAP_curve.py
```
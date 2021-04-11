# Make datasets

This task has 3 main steps:
1. feature engineering
2. make train test split(I don't use cross-val for simplicity)
3. save data to disk

```
Usage: dataset.py [OPTIONS]
OPTIONS
  --in-file - path to the raw downloaded file
  --out-dir - directory inside the container where the file should be saved to.
```
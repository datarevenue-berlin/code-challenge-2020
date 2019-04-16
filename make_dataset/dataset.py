import click
import dask.dataframe as dd
import numpy as np
from distributed import Client
from pathlib import Path


def _save_datasets(train, test, outdir: Path):
    """Save data sets into nice directory structure and write SUCCESS flag."""
    out_train = outdir / 'train.parquet/'
    out_test = outdir / 'test.parquet/'
    flag = outdir / '.SUCCESS'

    train.to_parquet(str(out_train))
    test.to_parquet(str(out_test))

    flag.touch()


@click.command()
@click.option('--in-csv')
@click.option('--out-dir')
def make_datasets(in_csv, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Connect to the dask cluster
    c = Client('dask-scheduler:8786')

    # load data as a dask Dataframe if you have trouble with dask
    # please fall back to pandas or numpy
    ddf = dd.read_csv(in_csv, blocksize=1e6)

    # we set the index so we can properly execute loc below
    ddf = ddf.set_index('Unnamed: 0')

    # trigger computation
    n_samples = len(ddf)

    # TODO: implement proper dataset creation here
    # http://docs.dask.org/en/latest/dataframe-api.html

    # split dataset into train test feel free to adjust test percentage
    idx = np.arange(n_samples)
    test_idx = idx[:n_samples // 10]
    test = ddf.loc[test_idx]

    train_idx = idx[n_samples // 10:]
    train = ddf.loc[train_idx]

    _save_datasets(train, test, out_dir)


if __name__ == '__main__':
    make_datasets()

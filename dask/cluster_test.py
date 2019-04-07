import logging
import time

import dask.dataframe as dd
import numpy as np
import pandas as pd
from distributed import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    logger.info("Wating for cluster to come online")

    time.sleep(30)

    logger.info("======= TESTING DASK CLUSTER ========")

    c = Client('dask-scheduler:8786')

    data = np.arange(10000)

    df = pd.DataFrame(dict(col1=data, col2=data[::-1]))

    ddf = dd.from_pandas(df, npartitions=10)

    c.scatter(ddf)

    logger.info("Submitting job...")

    res = dd.concat([ddf.sum(), ddf.loc[:500].sum()],
                    interleave_partitions=True).compute()

    logger.info("Result:\n{}".format(str(res)))

    logger.info("======= CLUSTER OK ========")

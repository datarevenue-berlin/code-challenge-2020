import os

import luigi
from pathlib import Path

from .util import DockerTask

data_root = Path(os.getenv('DATA_ROOT'))


class DownloadData(DockerTask):
    """Initial pipeline task downloads dataset"""

    name = luigi.Parameter(default='wine_dataset.csv')
    out_dir = luigi.Parameter(default=str(data_root/'raw'))
    url = luigi.Parameter(
        default='http://github.com/datarevenue-berlin/'
                'code-challenge-2019/dataset.csv'
    )

    @property
    def image(self):
        return 'code-challenge/download-data:v0.1'

    @property
    def command(self):
        return [
            'python', 'download_data.py',
            '--name', self.name,
            '--url', self.url,
            '--out-dir', self.out_dir
        ]

    def output(self):
        out_dir = Path(self.out_dir)
        out_dir.mkdir(parents=True)

        return luigi.LocalTarget(
            path=str(out_dir/f'{self.name}.csv')
        )

import logging

import luigi
import os
from pathlib import Path

from util import DockerTask

VERSION = os.getenv('PIPELINE_VERSION', '0.1')


class Debug(DockerTask):
    """Use this task with appropriate image to debug things."""

    @property
    def image(self):
        return f'code-challenge/download-data:{VERSION}'

    @property
    def command(self):
        return [
            'sleep', '3600'
        ]


class DownloadData(DockerTask):
    """Initial pipeline task downloads dataset."""

    fname = luigi.Parameter(default='wine_dataset')
    out_dir = luigi.Parameter(default='/usr/share/data/raw/')
    url = luigi.Parameter(
        default='https://github.com/datarevenue-berlin/code-challenge-2019/'
                'releases/download/0.1.0/dataset_sampled.csv'
    )

    @property
    def image(self):
        return f'code-challenge/download-data:{VERSION}'

    @property
    def command(self):
        return [
            'python', 'download_data.py',
            '--name', self.fname,
            '--url', self.url,
            '--out-dir', self.out_dir
        ]

    def output(self):
        out_dir = Path(self.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        return luigi.LocalTarget(
            path=str(out_dir/ f'{self.fname}.csv')
        )


class MakeDatasets(DockerTask):

    out_dir = luigi.Parameter(default='/usr/share/data/processed/')

    @property
    def image(self):
        return f'code-challenge/make-dataset:{VERSION}'

    def requires(self):
        return DownloadData()

    @property
    def command(self):
        return [
            'python', 'dataset.py',
            '--in-file',self.input().path,
            '--out-dir', self.out_dir
        ]


    def output(self):
        return luigi.LocalTarget(
            path=str(Path(self.out_dir) / '.SUCCESS')
        )

    
class TrainModels(DockerTask):

    out_dir = luigi.Parameter(default='/usr/share/data/models')
    config_path = luigi.Parameter(default='/usr/share/configs/train.json')

    @property
    def image(self):
        return f'code-challenge/train-models:{VERSION}'

    def requires(self):
        return MakeDatasets()

    @property
    def command(self):
        return [
            'python', 'train_models.py',
            '--data-directory', str(Path(self.input().path).parents[0]),
            '--config-path',self.config_path,
            '--out-dir', self.out_dir
        ]


    def output(self):
        return luigi.LocalTarget(
            path=str(Path(self.out_dir) / '.SUCCESS')
        )
    
class Evaluate(DockerTask):

    out_dir = luigi.Parameter(default='/usr/share/data/reports')

    @property
    def image(self):
        return f'code-challenge/evaluate:{VERSION}'

    def requires(self):
        return TrainModels()

    @property
    def command(self):
        out_dir = Path(self.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        
        return [
            'pypublish', 'report.py',
            '-o', str(out_dir / 'report.html')
        ]

    def output(self):
        return luigi.LocalTarget(
            path=str(Path(self.out_dir) / 'report.html')
        )
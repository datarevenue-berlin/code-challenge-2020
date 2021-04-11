import click
import json
from typing import Set, List, Tuple
from pathlib import Path
import pandas as pd
import pickle
from catboost import Pool, CatBoostRegressor

@click.command()
@click.option('--data-directory')
@click.option('--config-path')
@click.option('--out-dir')
def train_models(data_directory: str, config_path: str, out_dir: str):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    config = json.load(open(config_path, 'r'))
    train = pd.read_feather(Path(data_directory) / 'train.feather')
    test = pd.read_feather(Path(data_directory) / 'test.feather')
    for model_name, conf in config.items():
        columns = set(conf['categorical_features'] + conf['numeric_features'])
        if 'word_regex' in conf:
            columns.update([col for col in train.columns if conf['word_regex'] in col])
    
        train_pool = Pool(train[columns], label=train['points'], cat_features=conf['categorical_features'])
        test_pool = Pool(test[columns], label=test['points'], cat_features=conf['categorical_features'])
        model = CatBoostRegressor(**conf['model_config'])
        model.fit(train_pool, eval_set=test_pool)
        model.save_model(out_dir / (model_name + '.cbm'),
                           format="cbm",
                           export_parameters=None,
                           pool=test_pool)
        pickle.dump({'data': test[columns], 'labels': test['points']},
                    open(str(out_dir / (model_name + '_test_pool.pickle')), 'wb'))
    flag = out_dir / '.SUCCESS'
    flag.touch()
    
if __name__ == '__main__':
    train_models()

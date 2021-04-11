import click
import numpy as np
from pathlib import Path
import pandas as pd
from typing import Tuple
from pandarallel import pandarallel
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sacremoses import MosesTokenizer

def _save_datasets(train: pd.DataFrame, test: pd.DataFrame, outdir: Path) -> None:
    """Save data sets into nice directory structure and write SUCCESS flag."""
    out_train = outdir / 'train.feather/'
    out_test = outdir / 'test.feather/'
    flag = outdir / '.SUCCESS'

    train.reset_index(drop=True).to_feather(str(out_train))
    test.reset_index(drop=True).to_feather(str(out_test))

    flag.touch()

    
def extract_wine_year(train: pd.DataFrame, test: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    YEARS_START = set(['17', '18', '19', '20'])
    tokenizer = MosesTokenizer(lang='en')
    def extract_year(text):
        tokens = tokenizer.tokenize(text)
        res = [int(token) for token in tokens if token.isnumeric() and len(token) == 4 and token[0:2] in YEARS_START]
        if len(res) == 0:
            return np.NaN
        return np.float32(res[0])
    train['year'] = train['title'].parallel_apply(extract_year)
    test['year'] = test['title'].parallel_apply(extract_year)
    return (train, test)

def extract_words_from_description(train: pd.DataFrame, test: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    tfidf_vectorizer = TfidfVectorizer(analyzer='word', 
                                   stop_words= 'english',
                                   min_df=int(len(train) * 0.02))
    matrix = tfidf_vectorizer.fit_transform(train['description'].values)
    text_features = pd.DataFrame(matrix.todense(), 
                                 columns=[x + '_word' for x in tfidf_vectorizer.get_feature_names()])
    text_features = text_features.set_index(train.index)
    matrix = tfidf_vectorizer.transform(test['description'].values)
    text_features_test = pd.DataFrame(matrix.todense(), 
                                      columns=[x + '_word' for x in tfidf_vectorizer.get_feature_names()])
    text_features_test = text_features_test.set_index(test.index)
    
    train = pd.concat([train, text_features], axis=1)
    test = pd.concat([test, text_features_test], axis=1)
    return(train, test)

def extract_features(train: pd.DataFrame, test: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    functions = [extract_wine_year, 
                 extract_words_from_description]
    for func in functions:
        train, test = func(train, test)
    return (train, test)
    
def standartize_categorical_columns(data: pd.DataFrame) -> None:
    categorical_features = ['country', 'designation',
                            'province', 'region_1',
                            'region_2', 'taster_name',
                            'taster_twitter_handle', 'variety',
                            'winery']
    for col in data.dtypes[data.dtypes == object].index:
        data[col] = data[col].apply(str)
        
        
        
@click.command()
@click.option('--in-file')
@click.option('--out-dir')
def make_datasets(in_file, out_dir):
    pandarallel.initialize()
    
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    data = pd.read_csv(in_file)
    data = data.drop('Unnamed: 0', axis=1)
    standartize_categorical_columns(data)
    train, test = train_test_split(data, random_state=1305)
    train, test = extract_features(train, test)
    
    _save_datasets(train, test, out_dir)


if __name__ == '__main__':
    make_datasets()

# Train models

This task trains N models. Every model is described as an item in the config file.

```
Usage: train_models.py [OPTIONS]
OPTIONS
  --data-directory - path to the featured train and test data
  --config-path - path to the config file
  --out-dir - out directory of models
  
CONFIG_FILE is JSON file contains dict where the key is a model name and value is description
categorical_features - describe names of columns that should be used as categorical data(trained on unbiased counters)
numeric_features - describe names of columns that should be used as usual numeric columns
word_regex - should we use 1-gram textual data extracted from the description column 
model_config - parameters of gradient boosting training

"model_full": {
   "categorical_features":[
      "country",
      "designation",
      "province",
      "region_1",
      "region_2",
      "taster_name",
      "taster_twitter_handle",
      "variety",
      "winery"
   ],
   "numeric_features":[
      "price",
      "year"
   ],
   "word_regex": "_word",
   "model_config": {
       "iterations": 1000,
       "loss_function": "Quantile:alpha=0.5",
       "learning_rate": 0.1,
       "random_seed": 1305,
       "depth": 4,
       "l2_leaf_reg": 9
   }
},
```
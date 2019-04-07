# Datarevenue Code Challenge

Congratulations for making it to the Data Revenue Code Challenge 2019. This coding challenge will be used to evaluate your technical as well as your communication skills.

You will need docker an docker-compose to run this repository: 

* [How to install docker](https://docs.docker.com/engine/installation/)
* [How to install docker-compose](https://docs.docker.com/compose/install/)

## Goals
The repository you see here is a minimal local version of our usual task orchestration pipeline. We run everything in docker containers. So each task must expose its functionality via a CLI. We the use luigi to spin up the containers and pass the necessary arguments to each container. See more details [here](https://www.datarevenue.com/en/blog/how-to-scale-your-machine-learning-pipeline).

The repository already comes with the a leaf task implemented which will download the data set for you.

The goal of this challenge is to implement a complete machine learning pipeline. This pipeline should build a proof of concept machine learning model and evaluate it on test data set.

An important part of the goal is to explain the data set as well as the model to a fictional client. So your evaluation should include some plots on how your model makes the predictions.

### Challenge
To put things into the right perspective consider the following fictional scenario: 

You are a AI Consultant at Data Revenue. One of our clients is a big online wine seller. After a successful strategic consulting we advice the client to optimize his portfolio by creating a rating predictor for his inventory. We receive a sample dataset (10k rows) from the client and will come back in a week to evaluate our model on a bigger data set that is only accessible from on-premise servers (>100k rows).

The task now is to proof that this is possible to reduce risk before implementing a production solution. Our mini pipeline should later be able to run on their on premise machine which has only docker and docker-compose installed.

### Prerequisites
Before strating this challenge you should know:
1. How to train and evaluate a ML model
1. Have solid understanding of the [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html) library and ideally with [dask](http://docs.dask.org/en/latest/dataframe.html)
1. how to run [docker containers](https://docs.docker.com/get-started/)
1. how to specify tasks and dependencies in Spotify's [luigi](https://luigi.readthedocs.io/en/stable/example_top_artists.html)

### Requirements

To specify requirements better let's break this down into individual tasks.

#### 1. DownloadData
We already got you covered and implemented this task for you.

#### 2. Make(Train|Test)Dataset
Read the csv provided by DownloadData and transform it into a numerical matrix read for your ML models. 

Be aware that you dataset is just a sample from the whole dataset so your columns might not represent all possible values. 

Here at Data Revenue we use dask to parallelize Pandas operations. So we include also a running dask cluster which you *can* (you don't need to) use. Remember to partition you're csv if you plan on using dask (by using [blocksize](http://docs.dask.org/en/latest/dataframe-api.html#dask.dataframe.read_csv)).

Don't forget to split your dataset. So you might need more than a single task for this to run.

#### 3. TrainModel
Choose a suitable model type and train it on your previously built dataset. We like models that don't take forever to train. The final data set will have more than 100k rows.

#### 4. EvaluateModel
Here you can get creative! Pick a good metric and show your communication and presentation skills. Load your model and evaluate it on a held out part of the data set. This task should have a concrete outcome e.g. a zip of plots or even better a whole report (check the [pweave](http://mpastell.com/pweave/) package).

#### Other requirements
- Each task:
    - Needs to be callable via the command line
    - Needs to be documented
    - Should have **single** file as output
- Task images that aren't handled by docker-compose should be build and tagged in `./build-task-images.sh`
- Task images should be minimal to complete the task
- The data produced by your tasks should be structured (directories and filename) sensible inside `./data_root`
- Don't commit anything in `./data_root`, use `.gitignore`
- Your code should be PEP8 conform


## Evaluation Criteria
Your solution will be evaluated against following criteria:

* Is it runnable? **25 points**
* ML Best Practices **20 points**
* Code Quality (incl. Documentation and PEP8) **15 points**
* Presentation of results **20 points**
* Correct use of linux tools **10 points**
* Performance (concurrency, correct use of docker cache) **10 points**

## FAQ

> Can I use notebooks?

Yes you are encouraged to use notebooks to do ad-hoc analysis. Please include them in your submission. Having a pipeline set up in a notebook does not free you from submitting a working task pipeline.

> Can I use other technologies? Such as R, Spark, Pyspark, Modin, etc.

Yes you can as long as you can provision the docker containers and spin up all the necessary services with docker-compose.

> Do you accept partial submissions?

Yes you can submit you coding challenge partially finished in case you don't finish in time or have trouble with all the docker stuff. Unfinished challenges will be reviewed if some kind of model evaluation report is included (notebook or similar). You will loose points though as it is not runnable.

> I found a bug! What should I do?

Please contact us! We wrote this in a hurry and also make mistakes. PRs on bugs get you some extra points ;)

> I have another question!

Feel free to create an issue!


## Submission
Please zip your solution including all files and send to us with
the following naming schema:
```
cc19_<first_name>_<last_name>.zip
```


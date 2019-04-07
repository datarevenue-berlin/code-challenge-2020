# Datarevenue Code Challenge

Congratulations for making it to the Code Challenge. In this challenge the goal is to provision a docker container sucht that it is able to run a dask-cluster. This might sound complicated but it the challenge comes with a run configuration already.

Of course this won't start multiple machines in the cloud and run a actual real cluster but instead it uses docker-compose and docker to emulate this situation. You need both installed on your system before you can proceed (We use this tools on a daily basis at datarevenue so it won't be in vain).

* [How to install docker](https://docs.docker.com/engine/installation/)
* [How to install docker-compose](https://docs.docker.com/compose/install/)

You only have to provision the docker container by implementing the dockerfile and run the bootstrap bash script. The solution can be expressed in as little as 5 lines.

This should be straightforward on all linux and osx systems. Windows users are probably better off running a virtual machine with a linux distro but theoretically docker and docker-compose should also run native on Windows.


## Notes
- This should take you between 20-60 minutes depending on your linux experience
- Use python3
- The dockerfile should inherit from for minimal image size `alpine:latest` but `ubuntu:16:04` is also accepted
- You are not allowed to change any files (except the Dockerfile).

Due to use the base image `alpine:latest` you will run into some problems especially concerning glibc compatibility in case you can't find a solution for this you may switch to using `ubuntu:16:04` as the base image or check dockerhub there are plenty of images on dockerhub that deal with the problem. The references should help you to fix problems regarding glibc. You will need experience in compiling and installing programs from source though. Don't forget to set your locales after successful installtion.



## Evaluation
Your solution will be evaluated against following criteria:
* Is it runnable?
* Security
* Correct use of linux tools
* Image size
* Readability


## Submission
Please zip your solution including all files and send to us with
the following naming schema:
```
dc_<name>_<last_name>.zip
```

## References
* [alpine apk](https://wiki.alpinelinux.org/wiki/Alpine_Linux_package_management)
* [glibc-compat](https://github.com/sgerrand/alpine-pkg-glibc)
* [dockerfile reference](https://docs.docker.com/engine/reference/builder/)
* [dask distributed](http://distributed.readthedocs.io/en/latest/install.html)
* [dask](https://dask.readthedocs.io/en/latest/install.html)
* [psutil (dask dependency)](https://pythonhosted.org/psutil/)

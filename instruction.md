# Instruction for CEDAR



## Step 1: Pull docker image to local

```
docker pull dnxie/cedar
```


## Step 2: Start CEDAR

There are two ways to run CEDAR: fully-automated or semi-automated.


### 2.1: Fully automated

#### 2.1.1: Download our script
Copy script `start.sh` from the repo.

#### 2.1.2: Push the button

Run fuzzer with command:

```
bash start.sh <library> <workdir>
```
 - `library` is either `pytorch` or `tensorflow`
 - `workdir` is the path to the work directory to store outputs, logs, and bug-triggering inputs. 
  
  
For example, the following command starts CEDAR on PyTorch, and stores the results in `/home/foo/bar` (**absolute path**).
```
bash start.sh pytorch /home/foo/bar
```


What CEDAR will do by running the above command:
  - Create `/home/foo/bar/pytorch/pytorch-05-20-2023-13-33-22` folder for you if the time is 13:33:22 on 05/20/2023, and store all outputs there;  
  - Start a docker container named `pytorch-05-20-2023-13-33-22`;
  - Pull the latest nightly version of PyTorch and install it in the container;
  - Run C-DocTer and C-EAGLE in the background.
  
After running this command, you will see logs like this:
```
===== Create workdir /home/foo/bar/pytorch/pytorch/pytorch-05-20-2023-13-33-22 =====
===== Start the container =====
5a22058abc2bad7c2f274dc58f955b935eb7c7de383e7a5eeb55856f84662ba1
===== Start DocTer and EAGLE =====
===== DocTer and EAGLE running in the background. You are all set! =====
```

 
#### Schedule CEDAR to continuous test

 Alternatively, you can skip Step3 and schedule the continuous testing with `cron` instead. 
 
 1. Make sure `cron` is installed. 
 
 2. Run `crontab -e` to add the cron task. 
 
 Example task: 
 ```
59 23 2-30/2 * * bash /path/to/start.sh tensorflow /path/to/workdir 
59 23 1-31/2 * * bash /path/to/start.sh pytorch /path/to/workdir 
 ```
These two lines of task will automatically start CEDAR to test PyTorch on all the even days and TensorFlow on all the odd days at 23:59.

3. You are all set! The job will start automatically everyday. 
 
### 2.2: Semi automated


#### 2.2.1: Start the docker container
```
docker run -v <workdir>:/home/workdir -it dnxie/cedar
```

`<workdir>` is the path to the work directory to store outputs, logs, and bug-triggering inputs. 
For example, the following command starts CEDAR and stores the results in `/home/foo/bar` (**absolute path**).
```
docker run -v /home/foo/bar:/home/workdir -it dnxie/cedar
```

#### 2.2.2: 

You could either run 
```
bash run.sh <library> /home/workdir
```
where `<library>` is either `pytorch` or `tensorflow`, or run `bash run_DocTer.sh ....` and `bash run_EAGLE.sh ...` separately. The usage of these scripts can be found in `run.sh`.


#### Troubleshoot (Last update on March 1st, 2024)
Due to the rapid changes of pytorch/tensorflow codebase, the nightly version may have compatible issues with other packages. 

Currently, to test on PyTorch, one need to manually downgrade `mpmath` from `1.4.0a` to `1.3.0` **after `run_DocTer.sh` and before `run_EAGLE.sh`** by running 
```
pip uninstall mpmath
pip install mpmath==1.3.0
```


## Step 4: Checkout the result!

  After CEDAR finishes, you would see the following files in the work directory (e.g., `/home/foo/bar/pytorch/pytorch-05-20-2023-13-33-22`)
  
- The crash C-DocTer detected can be found in file `bug_list`
- The inconsistencies C-EAGLE detected can be found in file `pytorch_pytorch-05-20-2023-13-33-22_output_file.csv`
- The environment info can be found in `env.log` and `pip.log`
- The C-DocTer log can be found in `docter.log`
- The C-EAGLE log can be found in `eagle.log`


 
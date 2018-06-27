## RoboMobSF

Robot Framework Library for MobSF (SAST) Tool

**Supports Python 2.7.x for now**

### Install Instructions
* You need docker to run this program
* Pull the MobSF docker image: `docker pull we45/mobsf`
* Run the command `python setup.py install`  
* Create a `.robot` file that includes the keywords used by RoboMobSF Library


### Keywords

`run mobsf against file`  

`| run mobsf against file  | target file  | report path`

* target file:  taget file location i.e apk, zip, ipa, or appx 
* report path: where your results will be stored. An `.pdf` file and `.json` are generated as outputs

**Note:**

- Set Custom API Key in the `.robot` file to access the MobSF Rest API Endpoints (Required)
        
    **Example:** <br>
    `| Library | RoboMobSF  |  http://127.0.0.1:8000/ | 8000 | MobSF_API_Key` 

- Report path should be an absolute path
- If any exception is caused while executing robot file, MobSF docker container will automatically stopped and removed. 
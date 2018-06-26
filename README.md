## RoboMobSF

Robot Framework Library for MobSF (SAST) Tool

**Supports Python 2.7.x for now**

### Install Instructions
* You need docker to run this program
* Pull the MobSF docker image: `docker pull opensecurity/mobile-security-framework-mobsf`
* Run the command `python setup.py install`  
* Create a `.robot` file that includes the keywords used by RoboMobSF Library


### Keywords

`run mobsf against file`  

`| run mobsf against file  | target file  | report path`

* target file:  taget file location i.e apk, zip, ipa, or appx 
* report path: where your results will be stored. An `.pdf` file and `.json` are generated as outputs

**Note:**

- Report path should be an absolute path
- If any exception is caused while executing robot file, MobSF docker container will automatically stopped and removed. 
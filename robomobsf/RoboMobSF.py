import docker
import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from robot.api import logger
import hashlib
import time
import sys

reload(sys)
sys.setdefaultencoding('UTF8')



class RoboMobSF(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self,url,port,api_key):
        '''
        RoboMobSF Library should be imported with two argument

         Arguments:
            - ``url``:  is required to access the MobSF API to upload, run scan and generate report
            - ``port``: is required to expose the service to host machine 
            - ``api_key`` is required to access the MobSF API endpoint

        Examples:

        | = Keyword Definition =  | = Description =  |

        | Library | RoboMobSF | proxy | port | api_key |

        '''

        self.client = docker.from_env()
        self.url = url
        self.port = port
        self.api_key = api_key
        self.mobsf_docker = "we45/mobsf"

    def start_mobsf_docker(self):

        '''
            Start MobSF Docker for running Static Analysis against the Target File i.e apk, zip, ipa, or appx
        '''
        try:
            container_obj=self.client.containers.run(image=self.mobsf_docker,ports={'8000/tcp':self.port},environment={"MOBSF_API_KEY": self.api_key },detach=True)
            self.container_obj = container_obj

            time.sleep(20)
            while True:
                self.container_obj = self.client.containers.get(self.container_obj.id)
                if(self.container_obj.status == "running"):
                    break
                elif(self.container_obj.status == "exited"):
                    self.kill_mobsf_container()

        except BaseException as e:
            # self.kill_mobsf_container()
            logger.info("crt+c")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))


    # def get_api_key(self):
    #     docker_exec = self.container_obj.exec_run('sh -c "cat ~/.MobSF/secret"')
    #     if(docker_exec.exit_code == 0):
    #         secret_key = docker_exec.output
    #         hash_object = hashlib.sha256(secret_key.encode('utf-8'))
    #         self.api_key =  hash_object.hexdigest()
    #         logger.info(self.api_key)

    #     else:
    #         logger.info("Error :{}".format(docker_exec.output))
    #         self.kill_mobsf_container()

    def upload_file(self,target_file):

        '''Upload File'''
        multipart_data = MultipartEncoder(fields={'file': (target_file, open(target_file, 'rb'), 'application/octet-stream')})
        headers = {'Content-Type': multipart_data.content_type, 'Authorization': self.api_key}
       
        try:    
            response = requests.post(self.url + 'api/v1/upload', data=multipart_data, headers=headers)
            if(response.status_code == 200):
                self.target_file_info = json.loads(response.content)
                logger.info("Fie Upload Sucessfully!")
                logger.info("Filename: {} \n Hash: {} \n Scan Type: {} ".format(self.target_file_info['file_name'],self.target_file_info['hash'], self.target_file_info['scan_type']))

        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))
            self.kill_mobsf_container()


    def run_scan(self):
        
        '''Scan the file'''

        headers = {'Authorization': self.api_key}

        try:
            response = requests.post(self.url + 'api/v1/scan', data=self.target_file_info, headers=headers)
            if(response.status_code == 200):
                logger.info("Scan Completed!")

        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))
            self.kill_mobsf_container()


    def generate_pdf(self,report_path):

        '''Generate PDF Report'''

        headers = {'Authorization': self.api_key}
        data = {"hash": self.target_file_info["hash"], "scan_type": self.target_file_info["scan_type"]}
        
        try:
            response = requests.post(self.url + 'api/v1/download_pdf', data=data, headers=headers, stream=True)
            if(response.status_code == 200):
                with open(report_path+"/report.pdf", 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                logger.info("Report saved as report.pdf in the report directory")
            else:
                logger.info("Error: " + json.loads(response.content)['error'])


        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))
            self.kill_mobsf_container()


    def generate_json(self,report_path):

        '''Generate JSON Report'''

        headers = {'Authorization': self.api_key}
        data = {"hash": self.target_file_info["hash"], "scan_type": self.target_file_info["scan_type"]}
        
        try:
            response = requests.post(self.url + 'api/v1/report_json', data=data, headers=headers)
            if(response.status_code == 200):
                with open(report_path+"/report.json", 'wb') as file:
                    file.write(response.content)
                logger.info("Report saved as report.json in the report directory")
            else:
                logger.info("Error: " + json.loads(response.content)['error'])

        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))
            self.kill_mobsf_container()


    def delete_scan(self):

        '''Delete Scan Result'''

        headers = {'Authorization': self.api_key}
        data = {"hash":self.target_file_info["hash"]}

        try:
            response = requests.post(self.url + 'api/v1/delete_scan', data=data, headers=headers)
            if(response.status_code == 200):
                logger.info("File & Scan results are deleted for {} with hash id:{} and scan_type: {}".format(self.target_file_info['file_name'],self.target_file_info['hash'], self.target_file_info['scan_type']))

        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))
            self.kill_mobsf_container() 


    def kill_mobsf_container(self):

        '''Stop and remove the container'''

        try:
            target_container = self.client.containers.get(self.container_obj.id)
            target_container.stop()
            target_container.remove()
            logger.info("MobSF docker container is stopped and removed sucessfully")

        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))

    def run_mobsf_against_file(self,target_file,report_path):

        '''Automate all the MobSF task by grouping all function call into a single method '''

        
        self.start_mobsf_docker()
        # self.get_api_key()
        self.upload_file(target_file)
        self.run_scan()
        self.generate_pdf(report_path)
        self.generate_json(report_path)
        # self.delete_scan()
        self.kill_mobsf_container()
        
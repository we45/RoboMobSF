*** Settings ***
Library  RoboMobSF  http://127.0.0.1:8000/   8000

*** Variables ***
${TARGET_FILE}  /home/umar/Downloads/InsecureBankv2.apk
${REPORT_PATH}  /home/umar/Desktop/RobotFramework-Dev/RoboMobSF/test

*** Test Cases ***
Run MobSF against target file
    run mobsf against file  ${TARGET_FILE}  ${REPORT_PATH}
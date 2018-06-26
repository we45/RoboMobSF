from setuptools import setup
from codecs import open
from os import path

current_path = path.abspath(path.dirname(__file__))

with open(path.join(current_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='RoboMobSF',
    version='1.0',
    packages=[''],
    package_dir={'': 'robomobsf'},
    url='https://github.com/we45/RoboMobSF',
    license='MIT',
    author='we45',
    author_email='info@we45.com',
    description='Robot Framework Library for MobSF (SAST) Tool' ,
    install_requires=[
        'docker',
        'robotframework==3.0.4',
        'requests==2.19.1',
        'requests-toolbelt==0.8.0'
    ],
    long_description = long_description,
    long_description_content_type='text/markdown'
)
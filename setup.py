
from setuptools import setup, find_packages

setup(
    name='neuriomqtt',
    version='0.1',
    author='Lars Kellogg-Stedman',
    author_email='lars@oddbit.com',
    url='https://github.com/larsks/neuriomqtt',
    packages=find_packages(),
    install_requires=[
        'neurio',
        'paho_mqtt',
    ],
    entry_points={
        'console_scripts': [
            'neurio-export-mqtt = neuriomqtt.main:main',
        ],
    }
)

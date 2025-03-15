import os
from dotenv import set_key, load_dotenv
from setuptools import setup, find_packages


def configure_api_keys():
    """
    Configures the API keys for the project.
    """
    load_dotenv()
    
    if not os.path.exists('.env'):
        print('Creating .env file...')
        with open('.env', 'w') as f:
            f.write("")

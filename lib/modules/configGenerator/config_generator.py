import configparser
import os
from enum import Enum  
from configparser import ConfigParser, SectionProxy
from typing import Union

class ConfigGenerator():
    class ConfigSection(Enum):
        UserAutentication = 'UserAutentication'

    def __init__(self) -> None:
        self.configFile = f'{os.environ.get('HOME')}/.config/gitHubHelperPy.ini'

    def generate_config_file(self,configSection: ConfigSection,configSet):
        config = configparser.ConfigParser()
        config[configSection.value] = configSet
        with open(self.configFile,'w') as configfile:
            config.write(configfile)

    def read_config_file(self) -> ConfigParser:
        config = configparser.ConfigParser()
        config.read(self.configFile)
        return config

    def get_config(self, configSection: ConfigSection) -> Union[SectionProxy, None]:
        config = self.read_config_file()
        if config.has_section(configSection.value):
            return config[configSection.value]
        else:
            return None

from modules.validators import validator
from modules.configGenerator import config_generator

def config():
    token = input('token: ')
    user = input('user: ')
    if validator.strEmpty(user) and validator.strEmpty(token):
        return
    config = {'user': user, 'token': token}
    configGenerator = config_generator.ConfigGenerator()
    configSection = configGenerator.ConfigSection.UserAutentication
    configGenerator.generate_config_file(configSection,config)

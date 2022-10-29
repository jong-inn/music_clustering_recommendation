"""
    Create config directory and config.ini file
    After that, put client_id and client_secret given from Spotify
    
    Usage:

        python spotify_config.py
"""


import os
from configparser import ConfigParser
from configparser import ExtendedInterpolation

home_dir = os.getcwd()

def config_generator():
    
    if os.path.exists("./config"):
        pass
    else:
        os.mkdir("./config")
    
    config = ConfigParser(interpolation=ExtendedInterpolation())
    
    config["DEFAULT"] = {
          "home_dir": home_dir
    }
    
    config["authentication"] = {
          "client_id"    : ""
        , "client_secret": ""
    }
    
    with open("./config/config.ini", "w", encoding="utf-8") as configfile:
        config.write(configfile)
        print("create config.ini")
        
def config_read(section, key):
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read("./config/config.ini", encoding="utf-8")
    
    return config[section][key]

if __name__ == "__main__":
    config_generator()

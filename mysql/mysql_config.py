
import os
from configparser import ConfigParser
from configparser import ExtendedInterpolation

home_dir = os.getcwd()

def config_generator():
    
    config = ConfigParser(interpolation=ExtendedInterpolation())
    
    config["DEFAULT"] = {
          "home_dir": home_dir
    }
    
    config["authentication"] = {
          "password"    : ""
    }
    
    with open("./config.ini", "w", encoding="utf-8") as configfile:
        config.write(configfile)
        print("create config.ini")
        
def config_read(section, key):
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read("./config.ini", encoding="utf-8")
    
    return config[section][key]

if __name__ == "__main__":
    config_generator()

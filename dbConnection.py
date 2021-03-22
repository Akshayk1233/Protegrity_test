import yaml
import mysql.connector
def dbConnect():    
    #yaml.warnings({'YAMLLoadWarning': False})
    with open("config/config.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    

       
    
# Get target value

        host = cfg.get('mysql').get('host')
        user = cfg.get('mysql').get('user')
        password = cfg.get('mysql').get('passwd')
        db = cfg.get('mysql').get('db')
          
    mydb = mysql.connector.connect(
             host=host,
             user=user,
             passwd=password,
             database=db
             
             )
   
    return mydb







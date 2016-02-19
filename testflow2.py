#!env python
from flowthings import API, Token, mem
from subprocess import PIPE, Popen
from time import sleep
import psutil
from random import randint

ACCOUNT_NAME = "citynorman"
ACCOUNT_TOKEN = "8LAwINnfYCnXTljnTR1x2F3zwNqm"
FLOW_PATH = "/citynorman/test1"

# get the cpu temperature

def cpu_temp():
    return float(randint(90,100))

# define a drop

def drop():
    drop = {
        "elems": {
            "cpu_temp": {
                "type": "float",
                "value": cpu_temp()
            },
            "ram": {
                "type": "map",
                "value": {}
            },
            "disk": {
                "type": "map",
                "value": {}
            }
        }
    }

    ram = psutil.phymem_usage()
    drop['elems']['ram']['value']['total'] = 100.0
    drop['elems']['ram']['value']['used'] = float(randint(90,100))
    drop['elems']['ram']['value']['free'] = float(randint(0,10))

    disk = psutil.disk_usage('/')
    drop['elems']['disk']['value']['total'] = 100.0
    drop['elems']['disk']['value']['used'] = float(randint(90,100))
    drop['elems']['disk']['value']['free'] = float(randint(0,10))

    return drop

# set up your credentials, with the account name and a token
creds = Token(ACCOUNT_NAME, ACCOUNT_TOKEN)

# have the api use your credentials
api = API(creds)

# here's an example of using the find api, if we already had the
# id of the Flow that we are interested in we could exclude this step
flows = api.flow.find(mem.path == FLOW_PATH)
flow_id = flows[0]['id']

# a simple loop to create a drop in the telemetry flow, once per minute
# for an hour
for i in range(5):
    iDrop=drop()
    print i,iDrop
    new_drop = api.drop(flow_id).create(iDrop)
    sleep(1)

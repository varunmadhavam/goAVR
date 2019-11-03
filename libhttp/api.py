import flask
from flask import request
from fsm import fsm
class api:
    def __init__(self, mode, port, avr):
        self.mode = mode
        self.app = flask.Flask(__name__)
        self.port = port
        self.avr  = avr
        self.fsm = fsm(self.avr)

        @self.app.route("/connect")
        def connect():
            return self.impl_connect()

        @self.app.route("/setdevice",methods=['POST'])
        def setdevice():
            json = request.get_json()
            return self.impl_setdevice(json)

        @self.app.route("/")
        def root():
            return self.impl_root()

    def start(self):
        self.app.run(host='0.0.0.0',port=self.port)

    def impl_connect(self):
        ret, id=self.fsm.run(1)
        if (ret==0):
            return '{"return":0,"message":"Connected to goAVR","mode":"'+self.mode+'","deviceid":"'+id+'"}'
        else:
            return '{"return":1,"message":"'+id+'"}'
    
    def impl_setdevice(self,chip):
        if(self.avr.init(chip["pagesize_flash"],chip["pagesize_eeprom"],chip["flash_size"],chip["eeprom_size"],chip["twd_fuse"],chip["twd_flash"],chip["twd_eeprom"],chip["twd_erase"])==0):
            return '{"return":0,"message":"Chip Parameters set successfully"}'
        else:
            return '{"return":1,"message":"Chip Parameters Could Not Be Set"}'

    def impl_root(self):
        return '{"return":1,"message":"Not Implemented"}'
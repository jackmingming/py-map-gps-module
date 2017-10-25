from Queue import Queue
from threading import Thread
from subprocess import Popen
from flask import Flask, render_template, send_from_directory, jsonify, Response, request
import time
import socket

from gps import gps

gps_connetion = None
UART = '/dev/ttyAMA0'

fapp = Flask(__name__)

socket.socket._bind = socket.socket.bind
def my_socket_bind(self, *args, **kwargs):
    self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return socket.socket._bind(self, *args, **kwargs)

socket.socket.bind = my_socket_bind

@fapp.route("/")
def home():
    return render_template('map.html', branding=False)

@fapp.route("/api/position")
def api_sse_location():
    def gen():
        q = Queue()
        listeners_location.append(q)
        try:
            while True:
                result = q.get()
                ev = sse_encode(result)
                yield ev.encode()
        except GeneratorExit: # Or maybe use flask signals
            listeners_location.remove(q)

    return Response(gen(), mimetype="text/event-stream")

def run_server():
    fapp.run(threaded=True, host='0.0.0.0', port=3000)

def connect_to_gps():
    global gps_connetion

    while not gps_connetion:
        try:
            gps_connetion = gps(UART, 9600)
            
            if gps_connetion:
                filter_data_from_GPS()
        except Exception as e:
            print 'waiting for connection... (%s)' % str(e)
            time.sleep(2)
    print 'Connection is created'

def filter_data_from_GPS():
    while True:
        time.sleep(.25)
        try:
            data = gps_connetion.init_data()
            for k in data:
                if k:
                    if k['latDir'] == 'S':
                        k['lat'] = k['lat'] * -1
                    if k['lonDir'] == 'W':
                        k['lon'] = k['lon'] * -1
            print 'position_info: ', data
        except Exception as e:
            print e
            pass

gps_signal_thread = Thread(target=connect_to_gps)
gps_signal_thread.daemon = True
gps_signal_thread.start()

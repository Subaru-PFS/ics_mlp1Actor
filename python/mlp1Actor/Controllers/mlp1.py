import logging
import serial
import threading
import time
import mlp1Actor.mlp1


class mlp1(object):

    def __init__(self, actor, name, logLevel=logging.DEBUG):

        self.actor = actor
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logLevel)
        self.com = None
        self.receiver = None
        self.transmitter = None

    def __del__(self):

        self.logger.info('mlp1.__del__:')

    def start(self, cmd=None):

        self.logger.info('starting mlp1...')
        try:
            self.com = serial.Serial()
            self.com.baudrate = 38400
            self.com.port = '/dev/ttyUSB1'
            self.com.parity = serial.PARITY_EVEN
            self.com.timeout = 0
            self.com.bytesize = serial.SEVENBITS
            self.com.stopbits = serial.STOPBITS_TWO
            self.com.xonxoff = False
            self.com.rtscts = False
            self.com.dsrdtr = False
            self.com.open()
        except serial.SerialException as e:
            logger.warn('{}'.format(e))
            raise
        self.receiver = Receiver(actor=self.actor, logger=self.logger, com=self.com)
        self.transmitter = Transmitter(logger=self.logger, com=self.com)
        self.receiver.start()
        self.transmitter.start()

    def stop(self, cmd=None):

        self.logger.info('stopping mlp1...')
        self.transmitter.stop()
        self.receiver.stop()
        self.transmitter.join()
        self.transmitter = None
        self.receiver.join()
        self.receiver = None
        self.com.close()
        self.com = None


class Receiver(threading.Thread):

    _SWAIT = 0.005
    _STIMEOUT = 220
    _LWAIT = 0.1
    _LTIMEOUT = 11

    def __init__(self, actor=None, logger=None, com=None):

        super().__init__()

        self.actor = actor
        self.logger = logger
        self.com = com
        self.agcntrl = mlp1Actor.mlp1.AGControl()
        self.__stop = threading.Event()

    def __del__(self):

        self.logger.info('Receiver.__del__:')

    def stop(self):

        self.__stop.set()

    def run(self):

        while True:

            # Stop?
            if self.__stop.is_set():
                break

            data = bytearray()
            size = self.agcntrl.size
            sync = False  # True after STX (0x02) is received
            count = 0
            while 1:
                buf = self.com.read(min(size, self.com.in_waiting))
                n = len(buf)
                if sync:
                    if n > 0:
                        data += buf
                        size -= n
                        if size == 0:
                            break
                    else:
                        count += 1
                        if count >= Receiver._STIMEOUT:
                            break
                    time.sleep(Receiver._SWAIT)
                else:
                    if n > 0:
                        i = buf.find(b'\x02')
                        if i >= 0:
                            data += buf[i:]
                            size -= len(data)
                            if size == 0:
                                break
                            sync = True
                            count = 0
                            continue
                    count += 1
                    if count >= Receiver._LTIMEOUT:
                        break
                    time.sleep(Receiver._LWAIT)
            try:
                self.agcntrl.data = data
                #self.logger.info('data received')

                def logFunc(result):

                    if result.didFail:
                        self.logger.error('command failed')
                    else:
                        self.logger.info('command succeeded')

                _SVCS = ('vgw', 'tws1', 'tws2')
                # Check momentary signals for VLAN commands
                for svc in _SVCS:
                    output = self.agcntrl.get_video_output_on(svc)
                    interval = self.agcntrl.get_output_interval(svc)
                    if output is not None or interval is not None:
                        cmdStr = svc
                        if output is not None:
                            cmdStr += ' on' if output else ' off'
                        if interval is not None:
                            cmdStr += ' interval={}'.format(interval)
                        self.actor.sendCommand(actor='vlan', cmdStr=cmdStr, callFunc=logFunc)
            except mlp1Actor.mlp1.DecodeError as e:
                self.logger.warn('data validation error')
            if self.agcntrl.fault:
                self.logger.warn('serial receive error')


class Transmitter(threading.Thread):

    _INTERVAL = 1.0

    def __init__(self, logger=None, com=None):

        super().__init__()

        self.logger = logger
        self.com = com
        self.agcntrl = mlp1Actor.mlp1.AGControl()
        self.agstate = mlp1Actor.mlp1.AGState()
        self.__stop = threading.Event()

    def __del__(self):

        self.logger.info('Transmitter.__del__:')

    def stop(self):

        self.__stop.set()

    def run(self):

        while True:

            stop = self.__stop.wait(Transmitter._INTERVAL - time.time() % Transmitter._INTERVAL)
            if stop:
                break
            self.agstate.mlp1_if_alarm = self.agcntrl.fault
            self.com.write(self.agstate.data)
            #self.logger.info('data transmitted')

from datetime import datetime
import logging
import serial
import threading
import time
import mlp1Actor.mlp1


class mlp1:

    def __init__(self, actor, name, logLevel=logging.DEBUG):

        self.actor = actor
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logLevel)

    def __del__(self):

        self.logger.info('mlp1.__del__:')

    def start(self, cmd=None):

        self.logger.info('starting mlp1...')
        self.xcvr = Transceiver(actor=self.actor, logger=self.logger)
        self.xcvr.start()

    def stop(self, cmd=None):

        self.logger.info('stopping mlp1...')
        self.xcvr.stop()
        self.xcvr.join()
        del self.xcvr


class Transceiver(threading.Thread):

    _INTERVAL = 1.0

    def __init__(self, actor=None, logger=None):

        super().__init__()
        self.actor = actor
        self.logger = logger
        self.agcontrol = mlp1Actor.mlp1.AGControl()
        self.__stop = threading.Event()

    def __del__(self):

        self.logger.info('Transceiver.__del__:')

    def stop(self):

        self.__stop.set()

    def run(self):

        from contextlib import contextmanager

        @contextmanager
        def _managed_thread(_class, *args, **kwargs):

            _thread = _class(*args, **kwargs)
            self.logger.info('xcvr: {}: (re)start'.format(_class.__name__))
            _thread.start()
            try:
                yield _thread
            except Exception as e:
                self.logger.warn('xcvr: {}: {}'.format(_class.__name__, e))
            finally:
                self.logger.info('xcvr: {}: stop'.format(_class.__name__))
                _thread.stop()
                _thread.join()
                del _thread

        while 1:
            self.logger.info('xcvr: (re)start')
            stop = False
            try:
                with serial.serial_for_url('socket://133.40.164.127:4001') as comm:
                    #comm = serial.Serial()
                    #comm.baudrate = 38400
                    #comm.port = '/dev/ttyUSB1'
                    #comm.parity = serial.PARITY_EVEN
                    #comm.timeout = 0
                    #comm.bytesize = serial.SEVENBITS
                    #comm.stopbits = serial.STOPBITS_TWO
                    #comm.xonxoff = False
                    #comm.rtscts = False
                    #comm.dsrdtr = False
                    #comm.open()
                    with _managed_thread(Receiver, actor=self.actor, logger=self.logger, comm=comm, agcontrol=self.agcontrol) as rcvr, _managed_thread(Transmitter, actor=self.actor, logger=self.logger, comm=comm, agcontrol=self.agcontrol) as xmtr:
                        while 1:
                            stop = self.__stop.wait(Transceiver._INTERVAL - time.time() % Transceiver._INTERVAL)
                            if stop:
                                break
                            if not rcvr.is_alive():
                                self.logger.warn('xcvr: {} not alive'.format(rcvr.__class__.__name__))
                                break
                            if not xmtr.is_alive():
                                self.logger.warn('xcvr: {} not alive'.format(xmtr.__class__.__name__))
                                break
            except serial.SerialException as e:
                self.logger.warn('xcvr: {}'.format(e))
            if stop:
                break
            time.sleep(Transceiver._INTERVAL)


class Receiver(threading.Thread):

    _SWAIT = 0.005
    _STIMEOUT = 220
    _LWAIT = 0.1
    _LTIMEOUT = 11

    def __init__(self, actor=None, logger=None, comm=None, agcontrol=None):

        super().__init__()
        self.actor = actor
        self.logger = logger
        self.comm = comm
        self.agcontrol = agcontrol
        self.__stop = threading.Event()

    def __del__(self):

        self.logger.info('Receiver.__del__:')

    def stop(self):

        self.__stop.set()

    def run(self):

        while 1:
            if self.__stop.is_set():
                break
            data = bytearray()
            size = self.agcontrol.size
            sync = False  # True after STX (0x02) is received
            count = 0
            while 1:
                buf = self.comm.read(min(size, self.comm.in_waiting))
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
                            self.logger.warn('rcvr: STIMEOUT')
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
                        self.logger.warn('rcvr: LTIMEOUT')
                        break
                    time.sleep(Receiver._LWAIT)
            try:
                self.agcontrol.data = data
                self.logger.info('rcvr: {}'.format(datetime.now()))
                cmd = self.actor.bcast
                cmd.inform('telescopeState={},{},{},{},{},{},{},{}'.format(
                    int(self.agcontrol.mount_if_fault),
                    int(self.agcontrol.rotator_if_fault),
                    self.agcontrol.az_el_detect_time,
                    self.agcontrol.az_real_angle,
                    self.agcontrol.el_real_angle,
                    self.agcontrol.rotator_real_angle,
                    int(self.agcontrol.ag_if_alarm),
                    int(self.agcontrol.tsc_fault),
                ))

                def logFunc(result):

                    if result.didFail:
                        self.logger.error('rcvr: command failed')
                    else:
                        self.logger.info('rcvr: command succeeded')

                _SVCS = ('vgw', 'tws1', 'tws2')
                # Check momentary signals for VLAN commands
                for svc in _SVCS:
                    output = self.agcontrol.get_video_output_on(svc)
                    interval = self.agcontrol.get_output_interval(svc)
                    if output is not None or interval is not None:
                        cmdStr = svc
                        if output is not None:
                            cmdStr += ' on' if output else ' off'
                        if interval is not None:
                            cmdStr += ' interval={}'.format(interval)
                        self.actor.sendCommand(actor='vlan', cmdStr=cmdStr, callFunc=logFunc)
            except mlp1Actor.mlp1.DecodeError as e:
                self.logger.warn('rcvr: data validation error')
            if self.agcontrol.fault:
                self.logger.warn('rcvr: serial communication error')


class Transmitter(threading.Thread):

    _INTERVAL = 1.0

    def __init__(self, actor=None, logger=None, comm=None, agcontrol=None):

        super().__init__()
        self.actor = actor
        self.logger = logger
        self.comm = comm
        self.agcontrol = agcontrol
        self.agstate = self.actor.agstate
        self.__stop = threading.Event()

    def __del__(self):

        self.logger.info('Transmitter.__del__:')

    def stop(self):

        self.__stop.set()

    def run(self):

        while 1:
            stop = self.__stop.wait(Transmitter._INTERVAL - time.time() % Transmitter._INTERVAL)
            if stop:
                break
            self.agstate.mlp1_if_alarm = self.agcontrol.fault
            self.comm.write(self.agstate.data)
            self.logger.info('xmtr: {}'.format(datetime.now()))

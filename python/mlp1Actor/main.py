#!/usr/bin/env python

import argparse
import queue
from actorcore.ICC import ICC
from mlp1Actor.mlp1 import AGState
from mlp1Actor.ag import Ag
from mlp1Actor.agcam import Agcam
from mlp1Actor.pfilamps import Pfilamps
from mlp1Actor.vlan import Vlan


class Mlp1Actor(ICC):

    # Keyword arguments for this class
    _kwargs = {
    }

    def __init__(self, name, **kwargs):

        # Consume keyword arguments for this class
        for k in Mlp1Actor._kwargs:
            if k in kwargs:
                setattr(self, '_' + k, kwargs[k])
                del kwargs[k]
            else:
                setattr(self, '_' + k, Mlp1Actor._kwargs[k])

        super().__init__(name, **kwargs)

        self._everConnected = False

    # override
    def shutdown(self):

        self.stopAllControllers()
        super()._shutdown()

    def reloadConfiguration(self, cmd):

        pass

    # override
    def connectionMade(self):

        if not self._everConnected:

            self._everConnected = True

            self.allControllers = ['mlp1']
            self.attachAllControllers()

            self.agstate = AGState()
            self.ag = Ag(actor=self, logger=self.logger)
            self.agcam = Agcam(actor=self, logger=self.logger)
            self.pfilamps = Pfilamps(actor=self, logger=self.logger)
            self.vlan = Vlan(actor=self, logger=self.logger)
            #self.mlp1 = Mlp1(actor=self, logger=self.logger)

            _models = ('ag', 'agcam', 'pfilamps', 'vlan',)
            self.addModels(_models)
            self.models['ag'].keyVarDict['guideReady'].addCallback(self.ag.receiveStatusKeys, callNow=False)
            self.models['agcam'].keyVarDict['exposureState'].addCallback(self.agcam.receiveStatusKeys, callNow=False)
            self.models['agcam'].keyVarDict['exposureTime'].addCallback(self.agcam.receiveStatusKeys, callNow=False)
            self.models['agcam'].keyVarDict['cameraState1'].addCallback(self.agcam.receiveStatusKeys, callNow=False)
            self.models['agcam'].keyVarDict['cameraState2'].addCallback(self.agcam.receiveStatusKeys, callNow=False)
            self.models['agcam'].keyVarDict['cameraState3'].addCallback(self.agcam.receiveStatusKeys, callNow=False)
            self.models['agcam'].keyVarDict['cameraState4'].addCallback(self.agcam.receiveStatusKeys, callNow=False)
            self.models['agcam'].keyVarDict['cameraState5'].addCallback(self.agcam.receiveStatusKeys, callNow=False)
            self.models['agcam'].keyVarDict['cameraState6'].addCallback(self.agcam.receiveStatusKeys, callNow=False)
            self.models['pfilamps'].keyVarDict['lampStatus'].addCallback(self.pfilamps.receiveStatusKeys, callNow=False)
            for key in ('vgw', 'tws1', 'tws2'):
                self.models['vlan'].keyVarDict[key].addCallback(self.vlan.receiveStatusKeys, callNow=False)

    # override
    def connectionLost(self, reason):

        pass

    # override
    def commandFailed(self, cmd):

        pass

    def sendCommand(self, actor=None, cmdStr=None, timeLim=0, callFunc=None, **kwargs):

        if callFunc is None:
            self.logger.info('calling Cmdr.cmdq...')
            q = self.cmdr.cmdq(actor=actor, cmdStr=cmdStr, timeLim=timeLim, **kwargs)
            while True:
                try:
                    result = q.get(timeout=1)
                    break
                except queue.Empty:
                    if not self.cmdr.connector.activeConnection:
                        raise Exception('connection lost: actor={},cmdStr="{}",timeLim={},kwargs={}'.format(actor, cmdStr, timeLim, str(kwargs)))
            for reply in result.replyList:
                self.logger.info('reply={}'.format(reply.canonical()))
            self.logger.info('didFail={}'.format(result.didFail))
            if result.didFail:
                raise Exception('command failed: actor={},cmdStr="{}",timeLim={},kwargs={}'.format(actor, cmdStr, timeLim, str(kwargs)))
            return result
        else:
            self.logger.info('calling Cmdr.bgCall...')
            self.cmdr.bgCall(callFunc=callFunc, actor=actor, cmdStr=cmdStr, timeLim=timeLim, **kwargs)
            return None


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--configFile', default=None)
    args = parser.parse_args()

    actor = Mlp1Actor(
        'mlp1',
        productName='mlp1Actor',
        configFile=args.configFile
    )
    try:
        actor.run()
    except:
        raise
    finally:
        actor.shutdown()


if __name__ == '__main__':

    main()

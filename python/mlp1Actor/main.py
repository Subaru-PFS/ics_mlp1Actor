#!/usr/bin/env python

import argparse
from actorcore.ICC import ICC
from opscore.actor.keyvar import AllCodes
from mlp1Actor.mlp1 import AGState
from mlp1Actor.ag import Ag
from mlp1Actor.agcam import Agcam
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
    def versionString(self, cmd):

        return '1.0.0'

    # override
    def connectionMade(self):

        if not self._everConnected:

            self._everConnected = True

            self.allControllers = ['mlp1']
            self.attachAllControllers()

            self.agstate = AGState()
            self.ag = Ag(actor=self, logger=self.logger)
            self.agcam = Agcam(actor=self, logger=self.logger)
            self.vlan = Vlan(actor=self, logger=self.logger)
            #self.mlp1 = Mlp1(actor=self, logger=self.logger)

            _models = ('ag', 'agcam', 'vlan',)
            self.addModels(_models)
            self.models['ag'].keyVarDict['guideReady'].addCallback(self.ag.receiveStatusKeys, callNow=False)
            self.models['agcam'].keyVarDict['exposureState'].addCallback(self.agcam.receiveStatusKeys, callNow=False)
            for key in ('vgw', 'tws1', 'tws2'):
                self.models['vlan'].keyVarDict[key].addCallback(self.vlan.receiveStatusKeys, callNow=False)

    # override
    def connectionLost(self, reason):

        pass

    # override
    def commandFailed(self, cmd):

        pass

    def sendCommand(self, actor=None, cmdStr=None, timeLim=0, callFunc=None):

        if callFunc is None:
            self.logger.info('calling self.cmdr.call...')
            result = self.cmdr.call(actor=actor, cmdStr=cmdStr, timeLim=timeLim)
            for reply in result.replyList:
                self.logger.info('reply={}'.format(reply.canonical()))
            self.logger.info('didFail={}'.format(result.didFail))
            if result.didFail:
                raise Exception('sendCommand: command failed: actor={},cmdStr={},timeLim={}'.format(actor, cmdStr, timeLim))
            return result
        else:
            self.logger.info('calling self.cmdr.bgCall...')
            self.cmdr.bgCall(callFunc=callFunc, actor=actor, cmdStr=cmdStr, timeLim=timeLim, callCodes=AllCodes)
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

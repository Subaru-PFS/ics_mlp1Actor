from mlp1Actor.mlp1 import AGState


class Pfilamps:

    def __init__(self, actor=None, logger=None):

        self.actor = actor
        self.logger = logger
        self.agstate = AGState()

    def receiveStatusKeys(self, key):

        self.logger.info('receiveStatusKeys: {},{},{},{},{},{}'.format(
            key.actor,
            key.name,
            key.timestamp,
            key.isCurrent,
            key.isGenuine,
            [x.__class__.baseType(x) for x in key.valueList]
        ))

        lampTime = [float(x) for x in self.actor.models['pfilamps'].keyVarDict.get('lampRequest', (0, 0, 0, 0, 0, 0))]

        if all((key.name == 'lampStatus', key.isCurrent, key.isGenuine)):
            status = str(key.valueList[0])
            if status == 'off':
                self.agstate.halogen_on = False
                self.agstate.rare_gas_blue_on = False
                self.agstate.rare_gas_red_on = False
            elif status in ('warming', 'ready'):
                if lampTime[1] > 0:
                    self.agstate.rare_gas_blue_on = True
            elif status == 'on':
                if any((lampTime[0] > 0, lampTime[2] > 0, lampTime[3] > 0, lampTime[4] > 0)):
                    self.agstate.rare_gas_red_on = True
                if lampTime[5] > 0:
                    self.agstate.halogen_on = True
            elif status == 'unknown':
                pass

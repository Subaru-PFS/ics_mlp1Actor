class Pfilamps:

    def __init__(self, actor=None, logger=None):

        self.actor = actor
        self.logger = logger

    def receiveStatusKeys(self, key):

        self.logger.info('receiveStatusKeys: {},{},{},{},{},{}'.format(
            key.actor,
            key.name,
            key.timestamp,
            key.isCurrent,
            key.isGenuine,
            [x.__class__.baseType(x) if x is not None else None for x in key.valueList]
        ))

        lampTime = [float(x) for x in self.actor.models['pfilamps'].keyVarDict.get('lampRequest', (0, 0, 0, 0, 0, 0))]

        if all((key.name == 'lampStatus', key.isCurrent, key.isGenuine)):
            status = str(key.valueList[0])
            if status == 'off':
                self.actor.agstate.halogen_on = False
                self.actor.agstate.rare_gas_blue_on = False
                self.actor.agstate.rare_gas_red_on = False
            elif status in ('warming', 'ready'):
                if lampTime[1] > 0:
                    self.actor.agstate.rare_gas_blue_on = True
            elif status == 'on':
                if any((lampTime[0] > 0, lampTime[2] > 0, lampTime[3] > 0, lampTime[4] > 0)):
                    self.actor.agstate.rare_gas_red_on = True
                if lampTime[5] > 0:
                    self.actor.agstate.halogen_on = True
            elif status == 'unknown':
                pass

    def _getValues(self, key):

        valueList = self.actor.models['pfilamps'].keyVarDict[key].valueList
        return {x.name: x.__class__.baseType(x) if x is not None else None for x in valueList} if len(valueList) > 1 else valueList[0].__class__.baseType(valueList[0]) if valueList[0] is not None else None

    @property
    def lampStatus(self):

        return self._getValues('lampStatus')

    @property
    def lampRequest(self):

        return self._getValues('lampRequest')

    @property
    def lampIntensity(self):

        return self._getValues('lampIntensity')

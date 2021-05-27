class Ag:

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
            [x.__class__.baseType(x) for x in key.valueList]
        ))

        if all((key.name == 'guideReady', key.isCurrent, key.isGenuine)):
            ready = bool(key.valueList[0])
            self.actor.agstate.guide_ready = ready
        elif all((key.name == 'detectionState', key.isCurrent, key.isGenuine)):
            state = bool(key.valueList[0])
            self.actor.agstate.star_posn_detect = state
        elif all((key.name == 'exposureTime', key.isCurrent, key.isGenuine)):
            time = int(key.valueList[0])
            self.actor.agstate.exposure_time = time

    def _getValues(self, key):

        valueList = self.actor.models['ag'].keyVarDict[key].valueList
        return {x.name: x.__class__.baseType(x) for x in valueList} if len(valueList) > 1 else valueList[0].__class__.baseType(valueList[0])

    @property
    def guideReady(self):

        return self._getValues('guideReady')

    @property
    def detectionState(self):

        return self._getValues('detectionState')

    @property
    def exposureTime(self):

        return self._getValues('exposureTime')

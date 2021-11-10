class Agcc:

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

        if all((key.name == 'agc_exposing', key.isCurrent, key.isGenuine)):
            state = int(key.valueList[0])
            on = state > 0
            self.actor.agstate.exposure_on = on
        elif all((key.name.startswith('agc'), key.name.endswith('_stat', 4), key.isCurrent, key.isGenuine)):
            camera_id = int(key.name[3])
            state = str(key.valueList[0])
            used = state in ('BUSY',)
            alarm = state not in ('READY', 'BUSY',)  # ABSENT
            self.actor.agstate.set_ccd_used(camera_id, used)
            self.actor.agstate.set_ccd_alarm(camera_id, alarm)

    def _getValues(self, key):

        valueList = self.actor.models['agcc'].keyVarDict[key].valueList
        return {x.name: x.__class__.baseType(x) if x is not None else None for x in valueList} if len(valueList) > 1 else valueList[0].__class__.baseType(valueList[0]) if valueList[0] is not None else None

    @property
    def filepath(self):

        return self._getValues('agc_fitsfile')['filename']

    @property
    def frameId(self):

        return self._getValues('agc_frameid')

    @property
    def dataTime(self):

        return self._getValues('agc_fitsfile')['timestamp']

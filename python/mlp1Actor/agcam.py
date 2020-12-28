class Agcam:

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

        if all((key.name == 'exposureState', key.isCurrent, key.isGenuine)):
            state = str(key.valueList[0])
            if state == 'exposing':
                self.actor.agstate.exposure_on = True
            elif state == 'done':
                self.actor.agstate.exposure_on = False
        elif all((key.name == 'exposureTime', key.isCurrent, key.isGenuine)):
            time = int(key.valueList[0])
            self.actor.agstate.exposure_time = time
        elif all((key.name.startswith('cameraState'), key.isCurrent, key.isGenuine)):
            camera_id = int(key.name[11:])
            used, alarm = bool(key.valueList[0]), bool(key.valueList[1])
            self.actor.agstate.set_ccd_used(camera_id, used)
            self.actor.agstate.set_ccd_alarm(camera_id, alarm)
        elif all((key.name == 'detectionState', key.isCurrent, key.isGenuine)):
            state = bool(key.valueList[0])
            self.actor.agstate.star_posn_detect = state

    def _getValues(self, key):

        valueList = self.actor.models['agcam'].keyVarDict[key].valueList
        return {x.name: x.__class__.baseType(x) for x in valueList} if len(valueList) > 1 else valueList[0].__class__.baseType(valueList[0])

    @property
    def exposureState(self):

        return self._getValues('exposureState')

    @property
    def exposureTime(self):

        return self._getValues('exposureTime')

    @property
    def frameId(self):

        return self._getValues('frameId')

    @property
    def filepath(self):

        return self._getValues('filepath')

    @property
    def cameraState1(self):

        return self._getValues('cameraState1')

    @property
    def cameraState2(self):

        return self._getValues('cameraState2')

    @property
    def cameraState3(self):

        return self._getValues('cameraState3')

    @property
    def cameraState4(self):

        return self._getValues('cameraState4')

    @property
    def cameraState5(self):

        return self._getValues('cameraState5')

    @property
    def cameraState6(self):

        return self._getValues('cameraState6')

    @property
    def dataTime(self):

        return self._getValues('dataTime')

    @property
    def detectionState(self):

        return self._getValues('detectionState')

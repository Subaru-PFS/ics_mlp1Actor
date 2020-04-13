from mlp1Actor.mlp1 import AGState


class Agcam(object):

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

        if all((key.name == 'exposureState', key.isCurrent, key.isGenuine)):
            state = str(key.valueList[0])
            if state == 'exposing':
                self.agstate.exposure_on = True
            elif state == 'done':
                self.agstate.exposure_on = False
        elif all((key.name == 'cameraState1', key.isCurrent, key.isGenuine)):
            used, alarm = bool(key.valueList[0]), bool(key.valueList[1])
            self.agstate.ccd1_used = used
            self.agstate.ccd1_alarm = alarm
        elif all((key.name == 'cameraState2', key.isCurrent, key.isGenuine)):
            used, alarm = bool(key.valueList[0]), bool(key.valueList[1])
            self.agstate.ccd2_used = used
            self.agstate.ccd2_alarm = alarm
        elif all((key.name == 'cameraState3', key.isCurrent, key.isGenuine)):
            used, alarm = bool(key.valueList[0]), bool(key.valueList[1])
            self.agstate.ccd3_used = used
            self.agstate.ccd3_alarm = alarm
        elif all((key.name == 'cameraState4', key.isCurrent, key.isGenuine)):
            used, alarm = bool(key.valueList[0]), bool(key.valueList[1])
            self.agstate.ccd4_used = used
            self.agstate.ccd4_alarm = alarm
        elif all((key.name == 'cameraState5', key.isCurrent, key.isGenuine)):
            used, alarm = bool(key.valueList[0]), bool(key.valueList[1])
            self.agstate.ccd5_used = used
            self.agstate.ccd5_alarm = alarm
        elif all((key.name == 'cameraState6', key.isCurrent, key.isGenuine)):
            used, alarm = bool(key.valueList[0]), bool(key.valueList[1])
            self.agstate.ccd6_used = used
            self.agstate.ccd6_alarm = alarm

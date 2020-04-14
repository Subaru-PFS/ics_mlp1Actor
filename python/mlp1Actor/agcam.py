from mlp1Actor.mlp1 import AGState


class Agcam:

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
        elif all((key.name == 'exposureTime', key.isCurrent, key.isGenuine)):
            time = int(key.valueList[0])
            self.agstate.exposure_time = time
        elif all((key.name.startswith('cameraState'), key.isCurrent, key.isGenuine)):
            camera_id = int(key.name[11:])
            used, alarm = bool(key.valueList[0]), bool(key.valueList[1])
            self.agstate.set_ccd_used(camera_id, used)
            self.agstate.set_ccd_alarm(camera_id, alarm)

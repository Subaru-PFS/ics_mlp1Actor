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
        elif all((key.name == 'detectionState', key.isCurrent, key.isGenuine)):
            state = bool(key.valueList[0])
            if state:
                self.actor.agstate.star_posn_detect = state
        elif all((key.name == 'exposureTime', key.isCurrent, key.isGenuine)):
            time = int(key.valueList[0])
            self.actor.agstate.exposure_time = time
        elif all((key.name.startswith('cameraState'), key.isCurrent, key.isGenuine)):
            camera_id = int(key.name[11:])
            used, alarm = bool(key.valueList[0]), bool(key.valueList[1])
            self.actor.agstate.set_ccd_used(camera_id, used)
            self.actor.agstate.set_ccd_alarm(camera_id, alarm)

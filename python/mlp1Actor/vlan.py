class Vlan:

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

        if all((key.name in ('vgw', 'tws1', 'tws2'), key.isCurrent, key.isGenuine)):
            output, interval, alarm = bool(key.valueList[0]), int(key.valueList[1]), bool(key.valueList[2])
            self.actor.agstate.set_if_alarm(key.name, alarm)
            self.actor.agstate.set_output_interval(key.name, interval)
            self.actor.agstate.set_video_output_on(key.name, output)

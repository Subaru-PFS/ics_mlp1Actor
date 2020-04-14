from mlp1Actor.mlp1 import AGState


class Vlan:

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

        if all((key.name in ('vgw', 'tws1', 'tws2'), key.isCurrent, key.isGenuine)):
            output, interval, alarm = bool(key.valueList[0]), int(key.valueList[1]), bool(key.valueList[2])
            self.agstate.set_if_alarm(key.name, alarm)
            self.agstate.set_output_interval(key.name, interval)
            self.agstate.set_video_output_on(key.name, output)

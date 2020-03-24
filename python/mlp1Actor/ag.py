from mlp1Actor.mlp1 import AGState


class Ag(object):

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

        if all((key.name == 'guideReady', key.isCurrent, key.isGenuine)):
            ready = bool(key.valueList[0])
            self.agstate.guide_ready = ready

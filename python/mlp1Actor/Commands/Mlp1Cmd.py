#!/usr/bin/env python

from twisted.internet import reactor
import opscore.protocols.keys as keys
import opscore.protocols.types as types


class Mlp1Cmd:

    def __init__(self, actor):

        self.actor = actor
        self.vocab = [
            ('ping', '', self.ping),
            ('status', '', self.status),
            ('show', '', self.show),
            ('guide', '[<azel>] [<delay>] [<flux>] [<intensity>] [<ready>] [<size>] [<time>] [<xy>]', self.guide),
        ]
        self.keys = keys.KeysDictionary(
            'mlp1_mlp1',
            (1, 1),
            keys.Key('azel', types.Float()*2, help=''),
            keys.Key('delay', types.Float(), help=''),
            keys.Key('flux', types.Float(), help=''),
            keys.Key('intensity', types.Float(), help=''),
            keys.Key('ready', types.Bool('0', '1'), help=''),
            keys.Key('size', types.Float(), help=''),
            keys.Key('time', types.Float(), help=''),
            keys.Key('xy', types.Float()*2, help=''),
        )

    def ping(self, cmd):
        """Return a product name."""

        cmd.inform('text="{}"'.format(self.actor.productName))
        cmd.finish()

    def status(self, cmd):
        """Return status keywords."""

        self.actor.sendVersionKey(cmd)
        # self.actor.mlp1.sendStatusKeys(cmd, force=True)
        cmd.finish()

    def show(self, cmd):
        """Show status keywords from all models."""

        for n in self.actor.models:
            try:
                d = self.actor.models[n].keyVarDict
                for k, v in d.items():
                    cmd.inform('text="{}"'.format(repr(v)))
            except Exception as e:
                cmd.warn('text="Mlp1Cmd.show: {}: {}"'.format(n, e))
        cmd.finish()

    def guide(self, cmd):

        try:
            if 'azel' in cmd.cmd.keywords:
                eaz = float(cmd.cmd.keywords['azel'].values[0])
                eel = float(cmd.cmd.keywords['azel'].values[1])
                if eaz < -60.0 or 60.0 < eaz:
                    raise RuntimeError('eaz={}'.format(eaz))
                if eel < -60.0 or 60.0 < eel:
                    raise RuntimeError('eel={}'.format(eel))
                self.actor.agstate.star_posn_error_azel = eaz, eel
            if 'delay' in cmd.cmd.keywords:
                delay = float(cmd.cmd.keywords['delay'].values[0])
                self.actor.agstate.image_data_delay_time = delay
            if 'flux' in cmd.cmd.keywords:
                flux = float(cmd.cmd.keywords['flux'].values[0])
                self.actor.agstate.star_total_intensity = flux
            if 'intensity' in cmd.cmd.keywords:
                intensity = float(cmd.cmd.keywords['intensity'].values[0])
                self.actor.agstate.star_posn_intensity = intensity
            if 'ready' in cmd.cmd.keywords:
                ready = bool(cmd.cmd.keywords['ready'].values[0])
                self.actor.agstate.guide_ready = ready
            if 'size' in cmd.cmd.keywords:
                size = float(cmd.cmd.keywords['size'].values[0])
                self.actor.agstate.image_size = size
            if 'time' in cmd.cmd.keywords:
                time = float(cmd.cmd.keywords['time'].values[0])
                self.actor.agstate.data_time = time
            if 'xy' in cmd.cmd.keywords:
                ex = float(cmd.cmd.keywords['xy'].values[0])
                ey = float(cmd.cmd.keywords['xy'].values[1])
                if ex < -999999.99 or 999999.99 < ex:
                    raise RuntimeError('ex={}'.format(ex))
                if ey < -999999.99 or 999999.99 < ey:
                    raise RuntimeError('ey={}'.format(ey))
                self.actor.agstate.star_posn_error_xy = ex, ey
        except Exception as e:
            cmd.fail('text="guide: {}"'.format(e))
            return
        cmd.finish()

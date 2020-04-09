#!/usr/bin/env python

from twisted.internet import reactor
import opscore.protocols.keys as keys
import opscore.protocols.types as types


class Mlp1Cmd(object):

    def __init__(self, actor):

        self.actor = actor
        self.vocab = [
            ('ping', '', self.ping),
            ('status', '', self.status),
            ('show', '', self.show),
            ('set_offsets', '[<altaz>] [<xy>]', self.set_offsets),
        ]
        self.keys = keys.KeysDictionary(
            'mlp1_mlp1',
            (1, 1),
            keys.Key('altaz', types.Float()*2, help=''),
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

    def set_offsets(self, cmd):

        try:
            if 'altaz' in cmd.cmd.keywords:
                daz = float(cmd.cmd.keywords['altaz'].values[0])
                dalt = float(cmd.cmd.keywords['altaz'].values[1])
                if daz < -60.0 or 60.0 < daz:
                    raise RuntimeError('daz={}'.format(daz))
                if dalt < -60.0 or 60.0 < dalt:
                    raise RuntimeError('dalt={}'.format(dalt))
                self.actor.agstate.star_posn_error_azel = daz, dalt
            if 'xy' in cmd.cmd.keywords:
                dx = float(cmd.cmd.keywords['xy'].values[0])
                dy = float(cmd.cmd.keywords['xy'].values[1])
                if dx < -999999.99 or 999999.99 < dx:
                    raise RuntimeError('dx={}'.format(dx))
                if dy < -999999.99 or 999999.99 < dy:
                    raise RuntimeError('dy={}'.format(dy))
                self.actor.agstate.star_posn_error_xy = dx, dy
        except Exception as e:
            cmd.fail('text="set_offsets: {}"'.format(e))
            return
        cmd.finish()

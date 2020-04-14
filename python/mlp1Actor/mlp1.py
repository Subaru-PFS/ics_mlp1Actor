from datetime import datetime, time
from AGData import MLP1Data, PFSData


class DecodeError(Exception):

    pass


class AGState(object):

    def __init__(self):
        self._m = PFSData()

    @property
    def size(self):

        return self._m.GetEncodedDataLen()

    @property
    def fault(self):

        return self._m.CheckSerialError()

    @property
    def data(self):

        return self._m.EncodeSerialData()

    @data.setter
    def data(self, data):

        if not self._m.DecodeSerialData(data):
            raise DecodeError()

    ###################################################################

    @staticmethod
    def _bool_or_none(x):

        return bool(x) if x is not None else None

    # continuum
    @property
    def halogen_on(self):

        return self._m.GetFlagById('halogen', 0)

    @halogen_on.setter
    def halogen_on(self, value):

        self._m.SetFlagById('halogen', 0, self._bool_or_none(value))

    # Hg/Cd
    @property
    def rare_gas_blue_on(self):

        return self._m.GetFlagById('raregas', 0)

    @rare_gas_blue_on.setter
    def rare_gas_blue_on(self, value):

        self._m.SetFlagById('raregas', 0, self._bool_or_none(value))

    # Ne/Ar/Kr/Xe
    @property
    def rare_gas_red_on(self):

        return self._m.GetFlagById('raregas', 1)

    @rare_gas_red_on.setter
    def rare_gas_red_on(self, value):

        self._m.SetFlagById('raregas', 1, self._bool_or_none(value))

    continuum_lamp_on = halogen_on
    hg_cd_lamp_on = rare_gas_blue_on
    rare_gas_lamp_on = rare_gas_red_on

    @property
    def exposure_on(self):

        return self._m.GetFlagById('agstat', 0)

    @exposure_on.setter
    def exposure_on(self, value):

        self._m.SetFlagById('agstat', 0, self._bool_or_none(value))

    @property
    def star_posn_detect(self):

        return self._m.GetFlagById('agstat', 1)

    @star_posn_detect.setter
    def star_posn_detect(self, value):

        self._m.SetFlagById('agstat', 1, self._bool_or_none(value))

    @property
    def guide_ready(self):

        return self._m.GetFlagById('agready', 0)

    @guide_ready.setter
    def guide_ready(self, value):

        self._m.SetFlagById('agready', 0, bool(value))

    @property
    def exposure_time(self):

        return self._m.GetDataFromSHM('agexptime')

    @exposure_time.setter
    def exposure_time(self, value):

        self._m.SetDataToSHM('agexptime', int(value))

    @property
    def star_posn_error_x(self):

        return self._m.GetDataFromSHM('agdx')

    @star_posn_error_x.setter
    def star_posn_error_x(self, value):

        self._m.SetDataToSHM('agdx', float(value))

    @property
    def star_posn_error_y(self):

        return self._m.GetDataFromSHM('agdy')

    @star_posn_error_y.setter
    def star_posn_error_y(self, value):

        self._m.SetDataToSHM('agdy', float(value))

    @property
    def star_posn_error_xy(self):

        return self.star_posn_error_x, self.star_posn_error_y

    @star_posn_error_xy.setter
    def star_posn_error_xy(self, value):

        self.star_posn_error_x, self.star_posn_error_y = value

    @property
    def star_posn_error_az(self):

        return self._m.GetDataFromSHM('agaz')

    @star_posn_error_az.setter
    def star_posn_error_az(self, value):

        self._m.SetDataToSHM('agaz', float(value))

    @property
    def star_posn_error_el(self):

        return self._m.GetDataFromSHM('agel')

    @star_posn_error_el.setter
    def star_posn_error_el(self, value):

        self._m.SetDataToSHM('agel', float(value))

    @property
    def star_posn_error_azel(self):

        return self.star_posn_error_az, self.star_posn_error_el

    @star_posn_error_azel.setter
    def star_posn_error_azel(self, value):

        self.star_posn_error_az, self.star_posn_error_el = value

    @property
    def image_size(self):

        return self._m.GetDataFromSHM('agsize')

    @image_size.setter
    def image_size(self, value):

        self._m.SetDataToSHM('agsize', float(value))

    @property
    def star_posn_intensity(self):

        return self._m.GetDataFromSHM('agpint')

    @star_posn_intensity.setter
    def star_posn_intensity(self, value):

        self._m.SetDataToSHM('agpint', int(value))

    @property
    def star_total_intensity(self):

        return self._m.GetDataFromSHM('agtint')

    @star_total_intensity.setter
    def star_total_intensity(self, value):

        self._m.SetDataToSHM('agtint', int(value))

    @property
    def data_time(self):

        return self._m.GetDataFromSHM('agtime')

    @data_time.setter
    def data_time(self, value):

        self._m.SetDataToSHM('agtime', datetime(value).strftime('%y%m%d%H%M%S%f'))

    @property
    def image_data_delay_time(self):

        return self._m.GetDataFromSHM('agdelay')

    @image_data_delay_time.setter
    def image_data_delay_time(self, value):

        self._m.SetDataToSHM('agdelay', int(value))

    @property
    def camera_if_alarm(self):

        return self._m.GetFlagById('agifarm', 0)

    @camera_if_alarm.setter
    def camera_if_alarm(self, value):

        self._m.SetFlagById('agifarm', 0, bool(value))

    @property
    def mlp1_if_alarm(self):

        return self._m.GetFlagById('serarm', 0)

    @mlp1_if_alarm.setter
    def mlp1_if_alarm(self, value):

        self._m.SetFlagById('serarm', 0, bool(value))

    @property
    def vgw_video_output_on(self):

        return self._m.GetFlagById('vlvgw', 0)

    @vgw_video_output_on.setter
    def vgw_video_output_on(self, value):

        self._m.SetFlagById('vlvgw', 0, self._bool_or_none(value))

    @property
    def tws1_video_output_on(self):

        return self._m.GetFlagById('vltws', 0)

    @tws1_video_output_on.setter
    def tws1_video_output_on(self, value):

        self._m.SetFlagById('vltws', 0, self._bool_or_none(value))

    @property
    def tws2_video_output_on(self):

        return self._m.GetFlagById('vltws', 1)

    @tws2_video_output_on.setter
    def tws2_video_output_on(self, value):

        self._m.SetFlagById('vltws', 1, self._bool_or_none(value))

    def get_video_output_on(self, svc):

        attribute = svc.lower() + '_video_output_on'
        return getattr(self, attribute)

    def set_video_output_on(self, svc, value):

        attribute = svc.lower() + '_video_output_on'
        _value = getattr(self, attribute)
        setattr(self, attribute, value)
        return _value

    @property
    def vgw_output_interval(self):

        return self._m.GetDataFromSHM('vlintvgw')

    @vgw_output_interval.setter
    def vgw_output_interval(self, value):

        self._m.SetDataToSHM('vlintvgw', int(value))

    @property
    def tws1_output_interval(self):

        return self._m.GetDataFromSHM('vlinttws1')

    @tws1_output_interval.setter
    def tws1_output_interval(self, value):

        self._m.SetDataToSHM('vlinttws1', int(value))

    @property
    def tws2_output_interval(self):

        return self._m.GetDataFromSHM('vlinttws2')

    @tws2_output_interval.setter
    def tws2_output_interval(self, value):

        self._m.SetDataToSHM('vlinttws2', int(value))

    def get_output_interval(self, svc):

        attribute = svc.lower() + '_output_interval'
        return getattr(self, attribute)

    def set_output_interval(self, svc, value):

        attribute = svc.lower() + '_output_interval'
        _value = getattr(self, attribute)
        setattr(self, attribute, value)
        return _value

    @property
    def vgw_if_alarm(self):

        return self._m.GetFlagById('vlifarm', 0)

    @vgw_if_alarm.setter
    def vgw_if_alarm(self, value):

        self._m.SetFlagById('vlifarm', 0, bool(value))

    @property
    def tws1_if_alarm(self):

        return self._m.GetFlagById('vlifarm', 1)

    @tws1_if_alarm.setter
    def tws1_if_alarm(self, value):

        self._m.SetFlagById('vlifarm', 1, bool(value))

    @property
    def tws2_if_alarm(self):

        return self._m.GetFlagById('vlifarm', 2)

    @tws2_if_alarm.setter
    def tws2_if_alarm(self, value):

        self._m.SetFlagById('vlifarm', 2, bool(value))

    def get_if_alarm(self, svc):

        attribute = svc.lower() + '_if_alarm'
        return getattr(self, attribute)

    def set_if_alarm(self, svc, value):

        attribute = svc.lower() + '_if_alarm'
        _value = getattr(self, attribute)
        setattr(self, attribute, value)
        return _value

    @property
    def ccd1_used(self):

        return self._m.GetFlagById('agused', 0)

    @ccd1_used.setter
    def ccd1_used(self, value):

        self._m.SetFlagById('agused', 0, bool(value))

    @property
    def ccd2_used(self):

        return self._m.GetFlagById('agused', 1)

    @ccd2_used.setter
    def ccd2_used(self, value):

        self._m.SetFlagById('agused', 1, bool(value))

    @property
    def ccd3_used(self):

        return self._m.GetFlagById('agused', 2)

    @ccd3_used.setter
    def ccd3_used(self, value):

        self._m.SetFlagById('agused', 2, bool(value))

    @property
    def ccd4_used(self):

        return self._m.GetFlagById('agused', 3)

    @ccd4_used.setter
    def ccd4_used(self, value):

        self._m.SetFlagById('agused', 3, bool(value))

    @property
    def ccd5_used(self):

        return self._m.GetFlagById('agused', 4)

    @ccd5_used.setter
    def ccd5_used(self, value):

        self._m.SetFlagById('agused', 4, bool(value))

    @property
    def ccd6_used(self):

        return self._m.GetFlagById('agused', 5)

    @ccd6_used.setter
    def ccd6_used(self, value):

        self._m.SetFlagById('agused', 5, bool(value))

    @property
    def ccd_used(self):

        return self.ccd1_used, self.ccd2_used, self.ccd3_used, self.ccd4_used, self.ccd5_used, self.ccd6_used

    @ccd_used.setter
    def ccd_used(self, value):

        self.ccd1_used, self.ccd2_used, self.ccd3_used, self.ccd4_used, self.ccd5_used, self.ccd6_used = value

    def get_ccd_used(self, camera_id):

        attribute = 'ccd{}_used'.format(camera_id)
        return getattr(self, attribute)

    def set_ccd_used(self, camera_id, value):

        attribute = 'ccd{}_used'.format(camera_id)
        _value = getattr(self, attribute)
        setattr(self, attribute, value)
        return _value

    @property
    def ccd1_alarm(self):

        return self._m.GetFlagById('agarm', 0)

    @ccd1_alarm.setter
    def ccd1_alarm(self, value):

        self._m.SetFlagById('agarm', 0, bool(value))

    @property
    def ccd2_alarm(self):

        return self._m.GetFlagById('agarm', 1)

    @ccd2_alarm.setter
    def ccd2_alarm(self, value):

        self._m.SetFlagById('agarm', 1, bool(value))

    @property
    def ccd3_alarm(self):

        return self._m.GetFlagById('agarm', 2)

    @ccd3_alarm.setter
    def ccd3_alarm(self, value):

        self._m.SetFlagById('agarm', 2, bool(value))

    @property
    def ccd4_alarm(self):

        return self._m.GetFlagById('agarm', 3)

    @ccd4_alarm.setter
    def ccd4_alarm(self, value):

        self._m.SetFlagById('agarm', 3, bool(value))

    @property
    def ccd5_alarm(self):

        return self._m.GetFlagById('agarm', 4)

    @ccd5_alarm.setter
    def ccd5_alarm(self, value):

        self._m.SetFlagById('agarm', 4, bool(value))

    @property
    def ccd6_alarm(self):

        return self._m.GetFlagById('agarm', 5)

    @ccd6_alarm.setter
    def ccd6_alarm(self, value):

        self._m.SetFlagById('agarm', 5, bool(value))

    @property
    def ccd_alarm(self):

        return self.ccd1_alarm, self.ccd2_alarm, self.ccd3_alarm, self.ccd4_alarm, self.ccd5_alarm, self.ccd6_alarm

    @ccd_alarm.setter
    def ccd_alarm(self, value):

        self.ccd1_alarm, self.ccd2_alarm, self.ccd3_alarm, self.ccd4_alarm, self.ccd5_alarm, self.ccd6_alarm = value

    def get_ccd_alarm(self, camera_id):

        attribute = 'ccd{}_alarm'.format(camera_id)
        return getattr(self, attribute)

    def set_ccd_alarm(self, camera_id, value):

        attribute = 'ccd{}_alarm'.format(camera_id)
        _value = getattr(self, attribute)
        setattr(self, attribute, value)
        return _value


class AGControl(object):

    def __init__(self):

        self._m = MLP1Data()

    @property
    def size(self):

        return self._m.GetEncodedDataLen()

    @property
    def fault(self):

        return self._m.CheckSerialError()

    @property
    def data(self):

        return self._m.EncodeSerialData()

    @data.setter
    def data(self, data):

        if not self._m.DecodeSerialData(data):
            raise DecodeError()

    ###################################################################

    @property
    def mount_if_fault(self):

        return self._m.GetFlagById('fault', 0)

    @mount_if_fault.setter
    def mount_if_fault(self, value):

        self._m.SetFlagById('fault', 0, bool(value))

    @property
    def rotator_if_fault(self):

        return self._m.GetFlagById('fault', 1)

    @rotator_if_fault.setter
    def rotator_if_fault(self, value):

        self._m.SetFlagById('fault', 1, bool(value))

    @property
    def az_el_detect_time(self):

        return self._m.GetDataFromSHM('time')

    @az_el_detect_time.setter
    def az_el_detect_time(self, value):

        self._m.SetDataToSHM('time', time(value).strftime('%H%M%S%f'))

    @property
    def az_real_angle(self):

        return self._m.GetDataFromSHM('realaz')

    @az_real_angle.setter
    def az_real_angle(self, value):

        self._m.SetDataToSHM('realaz', float(value))

    @property
    def el_real_angle(self):

        return self._m.GetDataFromSHM('realel')

    @el_real_angle.setter
    def el_real_angle(self, value):

        self._m.SetDataToSHM('realel', float(value))

    @property
    def rotator_real_angle(self):

        return self._m.GetDataFromSHM('realrot')

    @rotator_real_angle.setter
    def rotator_real_angle(self, value):

        self._m.SetDataToSHM('realrot', float(value))

    @property
    def ag_if_alarm(self):

        return self._m.GetFlagById('serarm', 0)

    @ag_if_alarm.setter
    def ag_if_alarm(self, value):

        self._m.SetFlagById('serarm', 0, bool(value))

    @property
    def tsc_fault(self):

        return self._m.GetFlagById('tscarm', 0)

    @tsc_fault.setter
    def tsc_fault(self, value):

        self._m.SetFlagById('tscarm', 0, bool(value))

    ### momentary data

    @property
    def vgw_video_output_on(self):

        return self._m.GetFlagById('vlvgw', 0)

    @vgw_video_output_on.setter
    def vgw_video_output_on(self, value):

        self._m.SetFlagById('vlvgw', 0, self._bool_or_none(value))

    @property
    def tws1_video_output_on(self):

        return self._m.GetFlagById('vltws', 0)

    @tws1_video_output_on.setter
    def tws1_video_output_on(self, value):

        self._m.SetFlagById('vltws', 0, self._bool_or_none(value))

    @property
    def tws2_video_output_on(self):

        return self._m.GetFlagById('vltws', 1)

    @tws2_video_output_on.setter
    def tws2_video_output_on(self, value):

        self._m.SetFlagById('vltws', 1, self._bool_or_none(value))

    def get_video_output_on(self, svc):

        attribute = svc.lower() + '_video_output_on'
        return getattr(self, attribute)

    def set_video_output_on(self, svc, value):

        attribute = svc.lower() + '_video_output_on'
        _value = getattr(self, attribute)
        setattr(self, attribute, value)
        return _value

    @property
    def vgw_output_interval(self):

        return self._m.GetDataFromSHM('vlintvgw')

    @vgw_output_interval.setter
    def vgw_output_interval(self, value):

        self._m.SetDataToSHM('vlintvgw', int(value))

    @property
    def tws1_output_interval(self):

        return self._m.GetDataFromSHM('vlinttws1')

    @tws1_output_interval.setter
    def tws1_output_interval(self, value):

        self._m.SetDataToSHM('vlinttws1', int(value))

    @property
    def tws2_output_interval(self):

        return self._m.GetDataFromSHM('vlinttws2')

    @tws2_output_interval.setter
    def tws2_output_interval(self, value):

        self._m.SetDataToSHM('vlinttws2', int(value))

    def get_output_interval(self, svc):

        attribute = svc.lower() + '_output_interval'
        return getattr(self, attribute)

    def set_output_interval(self, svc, value):

        attribute = svc.lower() + '_output_interval'
        _value = getattr(self, attribute)
        setattr(self, attribute, value)
        return _value

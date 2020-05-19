import datetime
import threading
import AGData


class DecodeError(Exception):

    pass


class AGState:

    def __init__(self):
        self._data = AGData.PFSData()
        self._lock = threading.Lock()

    @property
    def size(self):
        with self._lock:
            return self._data.GetEncodedDataLen()

    @property
    def fault(self):
        with self._lock:
            return self._data.CheckSerialError()

    @property
    def data(self):
        with self._lock:
            return self._data.EncodeSerialData()

    @data.setter
    def data(self, data):
        with self._lock:
            if not self._data.DecodeSerialData(data):
                raise DecodeError()

    ###################################################################

    @staticmethod
    def _bool_or_none(x):
        return bool(x) if x is not None else None

    # continuum
    @property
    def halogen_on(self):
        with self._lock:
            return self._data.GetFlagById('halogen', 0)

    @halogen_on.setter
    def halogen_on(self, value):
        with self._lock:
            self._data.SetFlagById('halogen', 0, self._bool_or_none(value))

    # Hg/Cd
    @property
    def rare_gas_blue_on(self):
        with self._lock:
            return self._data.GetFlagById('raregas', 0)

    @rare_gas_blue_on.setter
    def rare_gas_blue_on(self, value):
        with self._lock:
            self._data.SetFlagById('raregas', 0, self._bool_or_none(value))

    # Ne/Ar/Kr/Xe
    @property
    def rare_gas_red_on(self):
        with self._lock:
            return self._data.GetFlagById('raregas', 1)

    @rare_gas_red_on.setter
    def rare_gas_red_on(self, value):
        with self._lock:
            self._data.SetFlagById('raregas', 1, self._bool_or_none(value))

    continuum_lamp_on = halogen_on
    hg_cd_lamp_on = rare_gas_blue_on
    rare_gas_lamp_on = rare_gas_red_on

    @property
    def exposure_on(self):
        with self._lock:
            return self._data.GetFlagById('agstat', 0)

    @exposure_on.setter
    def exposure_on(self, value):
        with self._lock:
            self._data.SetFlagById('agstat', 0, self._bool_or_none(value))

    @property
    def star_posn_detect(self):
        with self._lock:
            return self._data.GetFlagById('agstat', 1)

    @star_posn_detect.setter
    def star_posn_detect(self, value):
        with self._lock:
            self._data.SetFlagById('agstat', 1, self._bool_or_none(value))

    @property
    def guide_ready(self):
        with self._lock:
            return self._data.GetFlagById('agready', 0)

    @guide_ready.setter
    def guide_ready(self, value):
        with self._lock:
            self._data.SetFlagById('agready', 0, bool(value))

    @property
    def exposure_time(self):
        with self._lock:
            return self._data.GetDataFromSHM('agexptime')

    @exposure_time.setter
    def exposure_time(self, value):
        with self._lock:
            self._data.SetDataToSHM('agexptime', int(value))

    @property
    def star_posn_error_x(self):
        with self._lock:
            return self._data.GetDataFromSHM('agdx')

    @star_posn_error_x.setter
    def star_posn_error_x(self, value):
        with self._lock:
            self._data.SetDataToSHM('agdx', float(value))

    @property
    def star_posn_error_y(self):
        with self._lock:
            return self._data.GetDataFromSHM('agdy')

    @star_posn_error_y.setter
    def star_posn_error_y(self, value):
        with self._lock:
            self._data.SetDataToSHM('agdy', float(value))

    @property
    def star_posn_error_xy(self):
        with self._lock:
            return (
                self._data.GetDataFromSHM('agdx'),
                self._data.GetDataFromSHM('agdy')
            )

    @star_posn_error_xy.setter
    def star_posn_error_xy(self, value):
        with self._lock:
            self._data.SetDataToSHM('agdx', float(value[0]))
            self._data.SetDataToSHM('agdy', float(value[1]))

    @property
    def star_posn_error_az(self):
        with self._lock:
            return self._data.GetDataFromSHM('agaz')

    @star_posn_error_az.setter
    def star_posn_error_az(self, value):
        with self._lock:
            self._data.SetDataToSHM('agaz', float(value))

    @property
    def star_posn_error_el(self):
        with self._lock:
            return self._data.GetDataFromSHM('agel')

    @star_posn_error_el.setter
    def star_posn_error_el(self, value):
        with self._lock:
            self._data.SetDataToSHM('agel', float(value))

    @property
    def star_posn_error_azel(self):
        with self._lock:
            return (
                self._data.GetDataFromSHM('agaz'),
                self._data.GetDataFromSHM('agel')
            )

    @star_posn_error_azel.setter
    def star_posn_error_azel(self, value):
        with self._lock:
            self._data.SetDataToSHM('agaz', float(value[0]))
            self._data.SetDataToSHM('agel', float(value[1]))

    @property
    def image_size(self):
        with self._lock:
            return self._data.GetDataFromSHM('agsize')

    @image_size.setter
    def image_size(self, value):
        with self._lock:
            self._data.SetDataToSHM('agsize', float(value))

    @property
    def star_posn_intensity(self):
        with self._lock:
            return self._data.GetDataFromSHM('agpint')

    @star_posn_intensity.setter
    def star_posn_intensity(self, value):
        with self._lock:
            self._data.SetDataToSHM('agpint', int(value))

    @property
    def star_total_intensity(self):
        with self._lock:
            return self._data.GetDataFromSHM('agtint')

    @star_total_intensity.setter
    def star_total_intensity(self, value):
        with self._lock:
            self._data.SetDataToSHM('agtint', int(value))

    # seconds since unix epoch
    @property
    def data_time(self):
        with self._lock:
            return self._data.GetDataFromSHM('agtime').timestamp()

    # seconds since unix epoch
    @data_time.setter
    def data_time(self, value):
        with self._lock:
            self._data.SetDataToSHM('agtime', datetime.datetime.fromtimestamp(value))

    @property
    def image_data_delay_time(self):
        with self._lock:
            return self._data.GetDataFromSHM('agdelay')

    @image_data_delay_time.setter
    def image_data_delay_time(self, value):
        with self._lock:
            self._data.SetDataToSHM('agdelay', int(value))

    @property
    def camera_if_alarm(self):
        with self._lock:
            return self._data.GetFlagById('agifarm', 0)

    @camera_if_alarm.setter
    def camera_if_alarm(self, value):
        with self._lock:
            self._data.SetFlagById('agifarm', 0, bool(value))

    @property
    def mlp1_if_alarm(self):
        with self._lock:
            return self._data.GetFlagById('serarm', 0)

    @mlp1_if_alarm.setter
    def mlp1_if_alarm(self, value):
        with self._lock:
            self._data.SetFlagById('serarm', 0, bool(value))

    @property
    def vgw_video_output_on(self):
        with self._lock:
            return self._data.GetFlagById('vlvgw', 0)

    @vgw_video_output_on.setter
    def vgw_video_output_on(self, value):
        with self._lock:
            self._data.SetFlagById('vlvgw', 0, self._bool_or_none(value))

    @property
    def tws1_video_output_on(self):
        with self._lock:
            return self._data.GetFlagById('vltws', 0)

    @tws1_video_output_on.setter
    def tws1_video_output_on(self, value):
        with self._lock:
            self._data.SetFlagById('vltws', 0, self._bool_or_none(value))

    @property
    def tws2_video_output_on(self):
        with self._lock:
            return self._data.GetFlagById('vltws', 1)

    @tws2_video_output_on.setter
    def tws2_video_output_on(self, value):
        with self._lock:
            self._data.SetFlagById('vltws', 1, self._bool_or_none(value))

    def get_video_output_on(self, svc):
        attribute = svc.lower() + '_video_output_on'
        return getattr(self, attribute)

    def set_video_output_on(self, svc, value):
        attribute = svc.lower() + '_video_output_on'
        setattr(self, attribute, value)

    @property
    def vgw_output_interval(self):
        with self._lock:
            return self._data.GetDataFromSHM('vlintvgw')

    @vgw_output_interval.setter
    def vgw_output_interval(self, value):
        with self._lock:
            self._data.SetDataToSHM('vlintvgw', int(value))

    @property
    def tws1_output_interval(self):
        with self._lock:
            return self._data.GetDataFromSHM('vlinttws1')

    @tws1_output_interval.setter
    def tws1_output_interval(self, value):
        with self._lock:
            self._data.SetDataToSHM('vlinttws1', int(value))

    @property
    def tws2_output_interval(self):
        with self._lock:
            return self._data.GetDataFromSHM('vlinttws2')

    @tws2_output_interval.setter
    def tws2_output_interval(self, value):
        with self._lock:
            self._data.SetDataToSHM('vlinttws2', int(value))

    def get_output_interval(self, svc):
        attribute = svc.lower() + '_output_interval'
        return getattr(self, attribute)

    def set_output_interval(self, svc, value):
        attribute = svc.lower() + '_output_interval'
        setattr(self, attribute, value)

    @property
    def vgw_if_alarm(self):
        with self._lock:
            return self._data.GetFlagById('vlifarm', 0)

    @vgw_if_alarm.setter
    def vgw_if_alarm(self, value):
        with self._lock:
            self._data.SetFlagById('vlifarm', 0, bool(value))

    @property
    def tws1_if_alarm(self):
        with self._lock:
            return self._data.GetFlagById('vlifarm', 1)

    @tws1_if_alarm.setter
    def tws1_if_alarm(self, value):
        with self._lock:
            self._data.SetFlagById('vlifarm', 1, bool(value))

    @property
    def tws2_if_alarm(self):
        with self._lock:
            return self._data.GetFlagById('vlifarm', 2)

    @tws2_if_alarm.setter
    def tws2_if_alarm(self, value):
        with self._lock:
            self._data.SetFlagById('vlifarm', 2, bool(value))

    def get_if_alarm(self, svc):
        attribute = svc.lower() + '_if_alarm'
        return getattr(self, attribute)

    def set_if_alarm(self, svc, value):
        attribute = svc.lower() + '_if_alarm'
        setattr(self, attribute, value)

    @property
    def ccd1_used(self):
        with self._lock:
            return self._data.GetFlagById('agused', 0)

    @ccd1_used.setter
    def ccd1_used(self, value):
        with self._lock:
            self._data.SetFlagById('agused', 0, bool(value))

    @property
    def ccd2_used(self):
        with self._lock:
            return self._data.GetFlagById('agused', 1)

    @ccd2_used.setter
    def ccd2_used(self, value):
        with self._lock:
            self._data.SetFlagById('agused', 1, bool(value))

    @property
    def ccd3_used(self):
        with self._lock:
            return self._data.GetFlagById('agused', 2)

    @ccd3_used.setter
    def ccd3_used(self, value):
        with self._lock:
            self._data.SetFlagById('agused', 2, bool(value))

    @property
    def ccd4_used(self):
        with self._lock:
            return self._data.GetFlagById('agused', 3)

    @ccd4_used.setter
    def ccd4_used(self, value):
        with self._lock:
            self._data.SetFlagById('agused', 3, bool(value))

    @property
    def ccd5_used(self):
        with self._lock:
            return self._data.GetFlagById('agused', 4)

    @ccd5_used.setter
    def ccd5_used(self, value):
        with self._lock:
            self._data.SetFlagById('agused', 4, bool(value))

    @property
    def ccd6_used(self):
        with self._lock:
            return self._data.GetFlagById('agused', 5)

    @ccd6_used.setter
    def ccd6_used(self, value):
        with self._lock:
            self._data.SetFlagById('agused', 5, bool(value))

    @property
    def ccd_used(self):
        with self._lock:
            return (
                self._data.GetFlagById('agused', 0),
                self._data.GetFlagById('agused', 1),
                self._data.GetFlagById('agused', 2),
                self._data.GetFlagById('agused', 3),
                self._data.GetFlagById('agused', 4),
                self._data.GetFlagById('agused', 5)
            )

    @ccd_used.setter
    def ccd_used(self, value):
        with self._lock:
            self._data.SetFlagById('agused', 0, bool(value[0]))
            self._data.SetFlagById('agused', 1, bool(value[1]))
            self._data.SetFlagById('agused', 2, bool(value[2]))
            self._data.SetFlagById('agused', 3, bool(value[3]))
            self._data.SetFlagById('agused', 4, bool(value[4]))
            self._data.SetFlagById('agused', 5, bool(value[5]))

    def get_ccd_used(self, camera_id):
        attribute = 'ccd{}_used'.format(camera_id)
        return getattr(self, attribute)

    def set_ccd_used(self, camera_id, value):
        attribute = 'ccd{}_used'.format(camera_id)
        setattr(self, attribute, value)

    @property
    def ccd1_alarm(self):
        with self._lock:
            return self._data.GetFlagById('agarm', 0)

    @ccd1_alarm.setter
    def ccd1_alarm(self, value):
        with self._lock:
            self._data.SetFlagById('agarm', 0, bool(value))

    @property
    def ccd2_alarm(self):
        with self._lock:
            return self._data.GetFlagById('agarm', 1)

    @ccd2_alarm.setter
    def ccd2_alarm(self, value):
        with self._lock:
            self._data.SetFlagById('agarm', 1, bool(value))

    @property
    def ccd3_alarm(self):
        with self._lock:
            return self._data.GetFlagById('agarm', 2)

    @ccd3_alarm.setter
    def ccd3_alarm(self, value):
        with self._lock:
            self._data.SetFlagById('agarm', 2, bool(value))

    @property
    def ccd4_alarm(self):
        with self._lock:
            return self._data.GetFlagById('agarm', 3)

    @ccd4_alarm.setter
    def ccd4_alarm(self, value):
        with self._lock:
            self._data.SetFlagById('agarm', 3, bool(value))

    @property
    def ccd5_alarm(self):
        with self._lock:
            return self._data.GetFlagById('agarm', 4)

    @ccd5_alarm.setter
    def ccd5_alarm(self, value):
        with self._lock:
            self._data.SetFlagById('agarm', 4, bool(value))

    @property
    def ccd6_alarm(self):
        with self._lock:
            return self._data.GetFlagById('agarm', 5)

    @ccd6_alarm.setter
    def ccd6_alarm(self, value):
        with self._lock:
            self._data.SetFlagById('agarm', 5, bool(value))

    @property
    def ccd_alarm(self):
        with self._lock:
            return (
                self._data.GetFlagById('agarm', 0),
                self._data.GetFlagById('agarm', 1),
                self._data.GetFlagById('agarm', 2),
                self._data.GetFlagById('agarm', 3),
                self._data.GetFlagById('agarm', 4),
                self._data.GetFlagById('agarm', 5)
            )

    @ccd_alarm.setter
    def ccd_alarm(self, value):
        with self._lock:
            self._data.SetFlagById('agarm', 0, bool(value[0]))
            self._data.SetFlagById('agarm', 1, bool(value[1]))
            self._data.SetFlagById('agarm', 2, bool(value[2]))
            self._data.SetFlagById('agarm', 3, bool(value[3]))
            self._data.SetFlagById('agarm', 4, bool(value[4]))
            self._data.SetFlagById('agarm', 5, bool(value[5]))

    def get_ccd_alarm(self, camera_id):
        attribute = 'ccd{}_alarm'.format(camera_id)
        return getattr(self, attribute)

    def set_ccd_alarm(self, camera_id, value):
        attribute = 'ccd{}_alarm'.format(camera_id)
        setattr(self, attribute, value)


class AGControl:

    def __init__(self):
        self._data = AGData.MLP1Data()
        self._lock = threading.Lock()

    @property
    def size(self):
        with self._lock:
            return self._data.GetEncodedDataLen()

    @property
    def fault(self):
        with self._lock:
            return self._data.CheckSerialError()

    @property
    def data(self):
        with self._lock:
            return self._data.EncodeSerialData()

    @data.setter
    def data(self, data):
        with self._lock:
            if not self._data.DecodeSerialData(data):
                raise DecodeError()

    ###################################################################

    @property
    def mount_if_fault(self):
        with self._lock:
            return self._data.GetFlagById('fault', 0)

    @mount_if_fault.setter
    def mount_if_fault(self, value):
        with self._lock:
            self._data.SetFlagById('fault', 0, bool(value))

    @property
    def rotator_if_fault(self):
        with self._lock:
            return self._data.GetFlagById('fault', 1)

    @rotator_if_fault.setter
    def rotator_if_fault(self, value):
        with self._lock:
            self._data.SetFlagById('fault', 1, bool(value))

    # seconds since midnight utc
    @property
    def az_el_detect_time(self):
        with self._lock:
            return self._data.GetDataFromSHM('time').replace(year=1970, month=1, day=1).timestamp()

    # seconds since midnight utc
    @az_el_detect_time.setter
    def az_el_detect_time(self, value):
        with self._lock:
            self._data.SetDataToSHM('time', datetime.datetime.fromtimestamp(value % 86400))

    @property
    def az_real_angle(self):
        with self._lock:
            return self._data.GetDataFromSHM('realaz')

    @az_real_angle.setter
    def az_real_angle(self, value):
        with self._lock:
            self._data.SetDataToSHM('realaz', float(value))

    @property
    def el_real_angle(self):
        with self._lock:
            return self._data.GetDataFromSHM('realel')

    @el_real_angle.setter
    def el_real_angle(self, value):
        with self._lock:
            self._data.SetDataToSHM('realel', float(value))

    @property
    def rotator_real_angle(self):
        with self._lock:
            return self._data.GetDataFromSHM('realrot')

    @rotator_real_angle.setter
    def rotator_real_angle(self, value):
        with self._lock:
            self._data.SetDataToSHM('realrot', float(value))

    @property
    def ag_if_alarm(self):
        with self._lock:
            return self._data.GetFlagById('serarm', 0)

    @ag_if_alarm.setter
    def ag_if_alarm(self, value):
        with self._lock:
            self._data.SetFlagById('serarm', 0, bool(value))

    @property
    def tsc_fault(self):
        with self._lock:
            return self._data.GetFlagById('tscarm', 0)

    @tsc_fault.setter
    def tsc_fault(self, value):
        with self._lock:
            self._data.SetFlagById('tscarm', 0, bool(value))

    ### momentary data

    @property
    def vgw_video_output_on(self):
        with self._lock:
            return self._data.GetFlagById('vlvgw', 0)

    @vgw_video_output_on.setter
    def vgw_video_output_on(self, value):
        with self._lock:
            self._data.SetFlagById('vlvgw', 0, self._bool_or_none(value))

    @property
    def tws1_video_output_on(self):
        with self._lock:
            return self._data.GetFlagById('vltws', 0)

    @tws1_video_output_on.setter
    def tws1_video_output_on(self, value):
        with self._lock:
            self._data.SetFlagById('vltws', 0, self._bool_or_none(value))

    @property
    def tws2_video_output_on(self):
        with self._lock:
            return self._data.GetFlagById('vltws', 1)

    @tws2_video_output_on.setter
    def tws2_video_output_on(self, value):
        with self._lock:
            self._data.SetFlagById('vltws', 1, self._bool_or_none(value))

    def get_video_output_on(self, svc):
        attribute = svc.lower() + '_video_output_on'
        return getattr(self, attribute)

    def set_video_output_on(self, svc, value):
        attribute = svc.lower() + '_video_output_on'
        setattr(self, attribute, value)

    @property
    def vgw_output_interval(self):
        with self._lock:
            return self._data.GetDataFromSHM('vlintvgw')

    @vgw_output_interval.setter
    def vgw_output_interval(self, value):
        with self._lock:
            self._data.SetDataToSHM('vlintvgw', int(value))

    @property
    def tws1_output_interval(self):
        with self._lock:
            return self._data.GetDataFromSHM('vlinttws1')

    @tws1_output_interval.setter
    def tws1_output_interval(self, value):
        with self._lock:
            self._data.SetDataToSHM('vlinttws1', int(value))

    @property
    def tws2_output_interval(self):
        with self._lock:
            return self._data.GetDataFromSHM('vlinttws2')

    @tws2_output_interval.setter
    def tws2_output_interval(self, value):
        with self._lock:
            self._data.SetDataToSHM('vlinttws2', int(value))

    def get_output_interval(self, svc):
        attribute = svc.lower() + '_output_interval'
        return getattr(self, attribute)

    def set_output_interval(self, svc, value):
        attribute = svc.lower() + '_output_interval'
        setattr(self, attribute, value)

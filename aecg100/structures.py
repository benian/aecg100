"""The structure defined in C type from official SDK.

  Further reference document about the fields definition can be found in the
  official AECG100 User Manual page 21, which can be found in the following
  link:
  https://www.whaleteq.com/en/Products/Detail/31/AECG100
"""
import ctypes
import enum

from typing import Any, Dict

OutputSignalCallback = ctypes.CFUNCTYPE(None, ctypes.c_double, ctypes.c_int, ctypes.c_int)


#
# AECG SDK Enumeration
#
@enum.unique
class PPGChannel(enum.IntEnum):
  Channel1 = 1
  Channel2 = 2


@enum.unique
class ECGWaveformType(enum.IntEnum):
  Sine = 0
  Triangle = 1
  Square = 2
  RectanglePulse = 3
  TrianglePulse = 4
  Exponential = 5
  ECG = 6


@enum.unique
class Electrode(enum.IntEnum):
  RightArm = 0  # RA
  LeftArm = 0xff  # LA


@enum.unique
class ECGImpedance(enum.IntEnum):
  Off = 0  # Disable impedance
  On = 0xff  # Enable 620K impedance


@enum.unique
class ECGPacingEnable(enum.IntEnum):
  Off = 0
  On = 0xff


@enum.unique
class ECGRespirationEnable(enum.IntEnum):
  Off = 0
  On = 0xff


@enum.unique
class ECGNoiseFrequency(enum.IntEnum):
  FrequencyOff = 0
  Frequency50Hz = 1
  Frequency60Hz = 2
  Frequency100Hz = 3
  Frequency120Hz = 4


@enum.unique
class PPGWaveformType(enum.IntEnum):
  Sine = 0
  Triangle = 1
  Square = 2
  PPG = 3


@enum.unique
class PPGNoiseFrequency(enum.IntEnum):
  FrequencyOff = 0
  Frequency50Hz = 1
  Frequency60Hz = 2
  Frequency1KHz = 3
  Frequency5KHz = 4
  Frequency100Hz = 5
  Frequency120Hz = 6
  FrequencyWhiteNoise = 7


@enum.unique
class LEDMode(enum.IntEnum):
  Off = 0
  On = 1


@enum.unique
class LEDType(enum.IntEnum):
  Green = 0
  Red = 1
  IR = 2
  NONE = 3


@enum.unique
class SyncPulse(enum.IntEnum):
  LEDOff = 0
  On = 1
  Off = 2


@enum.unique
class PPGInverted(enum.IntEnum):
  Off = 0
  On = 1


@enum.unique
class PPGSampling(enum.IntEnum):
  Channel1PD = 0
  Channel2PD = 1
  Channel1Switch = 2
  Channel2Switch = 3
  Max = 4


class StructBase(ctypes.Structure):

  def update(self, attributes: Dict[str, Any]):
    for key, value in attributes.items():
      if hasattr(self, key):
        setattr(self, key, value)
      else:
        raise KeyError(f'{key} is invalid')

  def dump(self) -> Dict[str, Any]:
    struct_data = {}
    for field_name, field_type in self.__class__._fields_:
      data = getattr(self, field_name)

      if issubclass(field_type, ctypes.Array) and field_type._type_ is ctypes.c_char:
        data = data.decode('ascii')

      struct_data[field_name] = data

    return struct_data


#
# AECG SDK Structure
#
class HWInformation(StructBase):
  _fields_ = [
      ('fw_main_version', ctypes.c_int),
      ('fw_sub_version', ctypes.c_int),
      ('hw_version', ctypes.c_int),
      ('pcb_version', ctypes.c_int),
  ]


class ModelInformation(StructBase):
  _fields_ = [
      ('product_name', ctypes.c_char * 2),
      ('generation_number', ctypes.c_char),
      ('model_number', ctypes.c_char),
      ('serial_number', ctypes.c_int),
      ('year', ctypes.c_int),
      ('attr_1', ctypes.c_int),
      ('attr_2', ctypes.c_int),
      ('attr_3', ctypes.c_int),
  ]


class ECGWaveform(StructBase):
  _fields_ = [
      ('waveform_type', ctypes.c_int),
      ('frequency', ctypes.c_double),
      ('amplitude', ctypes.c_double),
      ('t_wave', ctypes.c_double),
      ('p_wave', ctypes.c_double),
      ('st_segment', ctypes.c_double),
      ('dc_offset_variable', ctypes.c_int),
      ('dc_offset', ctypes.c_int),
      ('time_period', ctypes.c_int),
      ('pr_interval', ctypes.c_int),
      ('qrs_duration', ctypes.c_int),
      ('t_duration', ctypes.c_int),
      ('qt_interval', ctypes.c_int),
      ('impedance', ctypes.c_int),
      ('sync_pulse', ctypes.c_int),
      ('pulse_width', ctypes.c_int),
      ('noise_amplitude', ctypes.c_double),
      ('noise_frequency', ctypes.c_int),
      ('pacing_enabled', ctypes.c_int),
      ('pacing_amplitude', ctypes.c_double),
      ('pacing_duration', ctypes.c_double),
      ('pacing_rate', ctypes.c_int),
      ('respiration_enabled', ctypes.c_int),
      ('respiration_amplitude', ctypes.c_int),
      ('respiration_rate', ctypes.c_int),
      ('respiration_ratio', ctypes.c_int),
      ('respiration_baseline', ctypes.c_int),
      ('respiration_apnea_duration', ctypes.c_int),
      ('respiration_apnea_cycle', ctypes.c_int),
      ('reserved', ctypes.c_char * 12),
  ]


class PPGWaveForm(StructBase):
  _fields_ = [
      ('waveform_type', ctypes.c_int),
      ('frequency', ctypes.c_double),
      ('vol_dc', ctypes.c_double),
      ('vol_sp', ctypes.c_double),
      ('vol_dn', ctypes.c_double),
      ('vol_dp', ctypes.c_double),
      ('ac_offset', ctypes.c_double),
      ('time_sp', ctypes.c_int),
      ('time_dn', ctypes.c_int),
      ('time_dp', ctypes.c_int),
      ('time_period', ctypes.c_int),
      ('sync_pulse', ctypes.c_int),
      ('inverted', ctypes.c_int),
      ('noise_amplitude', ctypes.c_double),
      ('noise_frequency', ctypes.c_int),
      ('respiration_enabled', ctypes.c_int),
      ('respiration_rate', ctypes.c_int),
      ('respiration_variation', ctypes.c_int),
      ('respiration_in_exhale_ratio', ctypes.c_int),
      ('reserved', ctypes.c_char * 16),
  ]


class FrequencyScan(StructBase):
  _fields_ = [
      ('amplitude', ctypes.c_double),
      ('frequency_start', ctypes.c_double),
      ('frequency_finish', ctypes.c_double),
      ('duration', ctypes.c_int),
  ]


class FrequencyScan2(StructBase):
  _fields_ = [
      ('amplitude', ctypes.c_double),
      ('dc', ctypes.c_double),
      ('sync_pulse', ctypes.c_int),
      ('frequency_start', ctypes.c_double),
      ('frequency_finish', ctypes.c_double),
      ('duration', ctypes.c_int),
  ]


class RawData(StructBase):
  _fields_ = [
      ('sample_rate', ctypes.c_double),
      ('size', ctypes.c_int),
      ('sync_pulse', ctypes.c_int),
      ('ac', ctypes.c_void_p),
      ('dc', ctypes.c_void_p),
      ('output_signal_callback', OutputSignalCallback),
  ]

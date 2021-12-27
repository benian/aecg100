import aecg100
from aecg100.client import Aecg100Client
from aecg100.structures import PPGChannel


def get_info(aecg: aecg100.Aecg100Client):
  print(aecg.module_info)
  print(aecg.ppg_module_info)
  print(aecg.device_info)
  print(aecg.ppg_device_info)


def play_ppg_waveform(aecg: aecg100.Aecg100Client):
  waveform = aecg100.structures.PPGWaveForm(**{
      'frequency': 1,
      'waveform_type': aecg100.structures.PPGWaveformType.PPG,
      'vol_dc': 300,
      'vol_sp': 15,
      'vol_dn': 8.4,
      'vol_dp': 9.6,
      'ac_offset': 0,
      'time_period': 750,
      'time_sp': 112,
      'time_dn': 270,
      'time_dp': 345,
      'sync_pulse': aecg100.structures.SyncPulse.On,
      'inverted': aecg100.structures.PPGInverted.On,
      'noise_amplitude': 0,
      'noise_frequency': aecg100.structures.PPGNoiseFrequency.FrequencyOff,
      'respiration_enabled': 0,
      'respiration_rate': 20,
      'respiration_variation': 0,
      'respiration_in_exhale_ratio': 1,
  })
  aecg.play_ppg_waveform((aecg100.structures.PPGChannel.Channel1, waveform))


if __name__ == '__main__':
  aecg = aecg100.Aecg100Client('./SDK/libaecgx64.so')
  aecg.connect()
  get_info(aecg)
  play_ppg_waveform(aecg)

  aecg.disconnect()

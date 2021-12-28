import platform
import time

import aecg100


def get_aecg_client():
  if platform.machine() == 'aarch64':
    client = aecg100.Aecg100Client("sdk/libaecgrpix64.so")
  elif platform.machine() == 'armv7l':
    client = aecg100.Aecg100Client("sdk/libaecgrpix86.so")
  elif platform.machine() == 'x86_64':
    client = aecg100.Aecg100Client("sdk/libaecgx64.so")
  else:
    client = aecg100.Aecg100Client("sdk/libaecgx86.so")

  return client


def test_get_main_module_model_information(client: aecg100.Aecg100Client):
  print("get main module model information", client.module_info)


def test_get_ppg_module_model_information(client: aecg100.Aecg100Client):
  print("get ppg module model information", client.ppg_module_info)


def test_get_main_module_device_information(client: aecg100.Aecg100Client):
  print("get main module device information", client.device_info)


def test_get_ppg_module_device_information(client: aecg100.Aecg100Client):
  print("get ppg module device information", client.ppg_device_info)


def test_output_ppg60bpm(aecg: aecg100.Aecg100Client):
  print('output PPG (60BPM, 12.5mV, SyncOff) ...')
  waveform = aecg100.structures.PPGWaveForm(
      **{
          'frequency': 1,
          'waveform_type': aecg100.structures.PPGWaveformType.PPG,
          'vol_dc': 625,
          'vol_sp': 12.5,
          'vol_dn': 7.0,
          'vol_dp': 8.0,
          'ac_offset': 0,
          'time_period': 1000,
          'time_sp': 150,
          'time_dn': 360,
          'time_dp': 460,
          'sync_pulse': aecg100.structures.SyncPulse.Off,
          'inverted': aecg100.structures.PPGInverted.On,
          'noise_amplitude': 0,
          'noise_frequency': aecg100.structures.PPGNoiseFrequency.FrequencyOff,
          'respiration_enabled': 0,
          'respiration_rate': 30,
          'respiration_variation': 1,
          'respiration_in_exhale_ratio': 1,
      })
  aecg.play_ppg_waveform((aecg100.structures.PPGChannel.Channel1, waveform))
  time.sleep(10)
  aecg.stop()


def test_output_ppg60bpm_ac_offset_added(aecg: aecg100.Aecg100Client):
  print('output PPG (60BPM, 12.5mV, SyncOff, AC Offset=2mV) ...')
  waveform = aecg100.structures.PPGWaveForm(
      **{
          'frequency': 1,
          'waveform_type': aecg100.structures.PPGWaveformType.PPG,
          'vol_dc': 625,
          'vol_sp': 12.5,
          'vol_dn': 7.0,
          'vol_dp': 8.0,
          'ac_offset': 2,
          'time_period': 1000,
          'time_sp': 150,
          'time_dn': 360,
          'time_dp': 460,
          'sync_pulse': aecg100.structures.SyncPulse.Off,
          'inverted': aecg100.structures.PPGInverted.On,
          'noise_amplitude': 0,
          'noise_frequency': aecg100.structures.PPGNoiseFrequency.FrequencyOff,
          'respiration_enabled': 0,
          'respiration_rate': 30,
          'respiration_variation': 1,
          'respiration_in_exhale_ratio': 1,
      })
  aecg.play_ppg_waveform((aecg100.structures.PPGChannel.Channel1, waveform))
  time.sleep(10)
  aecg.stop()


def test_output_ppg60bpm_noise(aecg: aecg100.Aecg100Client):
  print('output PPG (60BPM, 12.5mV, SyncOff, Noise: 50Hz, 2mV) ...')
  waveform = aecg100.structures.PPGWaveForm(
      **{
          'frequency': 1,
          'waveform_type': aecg100.structures.PPGWaveformType.PPG,
          'vol_dc': 625,
          'vol_sp': 12.5,
          'vol_dn': 7.0,
          'vol_dp': 8.0,
          'ac_offset': 0,
          'time_period': 1000,
          'time_sp': 150,
          'time_dn': 360,
          'time_dp': 460,
          'sync_pulse': aecg100.structures.SyncPulse.Off,
          'inverted': aecg100.structures.PPGInverted.On,
          'noise_amplitude': 2,
          'noise_frequency': aecg100.structures.PPGNoiseFrequency.Frequency50Hz,
          'respiration_enabled': 0,
          'respiration_rate': 30,
          'respiration_variation': 1,
          'respiration_in_exhale_ratio': 1,
      })
  aecg.play_ppg_waveform((aecg100.structures.PPGChannel.Channel1, waveform))
  time.sleep(10)
  aecg.stop()


if __name__ == '__main__':
  client = get_aecg_client()
  client.connect()

  for func in [
      test_get_main_module_model_information,
      test_get_ppg_module_model_information,
      test_get_main_module_device_information,
      test_get_ppg_module_device_information,
      test_output_ppg60bpm,
      test_output_ppg60bpm_ac_offset_added,
      test_output_ppg60bpm_noise,
  ]:
    func(client)
    print(f'{func.__name__} is finished')

  client.disconnect()
  print('all tests finished')

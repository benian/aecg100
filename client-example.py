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


def test_output_ecg_waveform_1hz_ecg(aecg: aecg100.Aecg100Client):
  print('output ECG (1Hz, 1mV, ECG, RA) ...')
  waveform = aecg100.structures.ECGWaveform(
      **{
          'waveform_type': aecg100.structures.ECGWaveformType.ECG,
          'frequency': 1,
          'amplitude': 1.0,
          't_wave': 0.2,
          'p_wave': 0.2,
          'st_segment': 0,
          'dc_offset_variable': 0,
          'dc_offset': 0,
          'time_period': 1000,
          'pr_interval': 160,
          'qrs_duration': 100,
          't_duration': 180,
          'qt_interval': 350,
          'impedance': aecg100.structures.ECGImpedance.Off,
          'electrode': aecg100.structures.Electrode.RightArm,
          'pulse_width': 100,
          'noise_amplitude': 0,
          'noise_frequency': aecg100.structures.ECGNoiseFrequency.FrequencyOff,
          'pacing_enabled': 0,
          'pacing_amplitude': 2,
          'pacing_duration': 2,
          'pacing_rate': 60,
          'respiration_enabled': 0,
          'respiration_amplitude': 1000,
          'respiration_rate': 20,
          'respiration_baseline': 1000,
          'respiration_ratio': 1,
          'respiration_apnea_duration': 10,
          'respiration_apnea_cycle': 1,
      })
  aecg.play_ecg_waveform(waveform)
  time.sleep(10)
  aecg.stop()


def test_output_ecg_waveform_1hz_ecg_noise(aecg: aecg100.Aecg100Client):
  print('output ECG (1Hz, 4mV, ECG, RA, Noise: 50Hz, 0.5mV) ...')
  waveform = aecg100.structures.ECGWaveform(
      **{
          'waveform_type': aecg100.structures.ECGWaveformType.ECG,
          'frequency': 1,
          'amplitude': 4.0,
          't_wave': 0.2,
          'p_wave': 0.2,
          'st_segment': 0,
          'dc_offset_variable': 0,
          'dc_offset': 0,
          'time_period': 1000,
          'pr_interval': 160,
          'qrs_duration': 100,
          't_duration': 180,
          'qt_interval': 350,
          'impedance': aecg100.structures.ECGImpedance.Off,
          'electrode': aecg100.structures.Electrode.RightArm,
          'pulse_width': 100,
          'noise_amplitude': 0.5,
          'noise_frequency': aecg100.structures.ECGNoiseFrequency.Frequency50Hz,
          'pacing_enabled': 0,
          'pacing_amplitude': 2,
          'pacing_duration': 2,
          'pacing_rate': 60,
          'respiration_enabled': 0,
          'respiration_amplitude': 1000,
          'respiration_rate': 20,
          'respiration_baseline': 1000,
          'respiration_ratio': 1,
          'respiration_apnea_duration': 10,
          'respiration_apnea_cycle': 1,
      })
  aecg.play_ecg_waveform(waveform)
  time.sleep(10)
  aecg.stop()


def test_output_ecg_waveform_1hz_sine(aecg: aecg100.Aecg100Client):
  print('output ECG (1Hz, 1mV, Sine, RA) ...')
  waveform = aecg100.structures.ECGWaveform(
      **{
          'waveform_type': aecg100.structures.ECGWaveformType.Sine,
          'frequency': 1,
          'amplitude': 1.0,
          't_wave': 0.2,
          'p_wave': 0.2,
          'st_segment': 0,
          'dc_offset_variable': 0,
          'dc_offset': 0,
          'time_period': 1000,
          'pr_interval': 160,
          'qrs_duration': 100,
          't_duration': 180,
          'qt_interval': 350,
          'impedance': aecg100.structures.ECGImpedance.Off,
          'electrode': aecg100.structures.Electrode.RightArm,
          'pulse_width': 100,
          'noise_amplitude': 0,
          'noise_frequency': aecg100.structures.ECGNoiseFrequency.FrequencyOff,
          'pacing_enabled': 0,
          'pacing_amplitude': 2,
          'pacing_duration': 2,
          'pacing_rate': 60,
          'respiration_enabled': 0,
          'respiration_amplitude': 1000,
          'respiration_rate': 20,
          'respiration_baseline': 1000,
          'respiration_ratio': 1,
          'respiration_apnea_duration': 10,
          'respiration_apnea_cycle': 1,
      })
  aecg.play_ecg_waveform(waveform)
  time.sleep(10)
  aecg.stop()


def test_output_ecg_waveform_0_5hz_rectangle(aecg: aecg100.Aecg100Client):
  print('output ECG (0.5Hz, 1mv, Rectangle, RA) ...')
  waveform = aecg100.structures.ECGWaveform(
      **{
          'waveform_type': aecg100.structures.ECGWaveformType.Square,
          'frequency': 0.5,
          'amplitude': 1.0,
          't_wave': 0.2,
          'p_wave': 0.2,
          'st_segment': 0,
          'dc_offset_variable': 0,
          'dc_offset': 0,
          'time_period': 2000,
          'pr_interval': 160,
          'qrs_duration': 100,
          't_duration': 180,
          'qt_interval': 350,
          'impedance': aecg100.structures.ECGImpedance.Off,
          'electrode': aecg100.structures.Electrode.RightArm,
          'pulse_width': 100,
          'noise_amplitude': 0,
          'noise_frequency': aecg100.structures.ECGNoiseFrequency.FrequencyOff,
          'pacing_enabled': 0,
          'pacing_amplitude': 2,
          'pacing_duration': 2,
          'pacing_rate': 60,
          'respiration_enabled': 0,
          'respiration_amplitude': 1000,
          'respiration_rate': 20,
          'respiration_baseline': 1000,
          'respiration_ratio': 1,
          'respiration_apnea_duration': 10,
          'respiration_apnea_cycle': 1,
      })
  aecg.play_ecg_waveform(waveform)
  time.sleep(10)
  aecg.stop()


def test_output_ecg_frequency_scan(aecg: aecg100.Aecg100Client):
  print('output ECG frequency scan (0.5Hz-150Hz, 30sec) ...')
  scan = aecg100.structures.ECGFrequencyScan(
      **{
          'amplitude': 1,
          'frequency_start': 0.5,
          'frequency_finish': 150,
          'duration': 30,
      })
  aecg.scan_ecg_frequency(scan)
  time.sleep(30)
  aecg.stop()


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


def test_output_ppg_frequency_scan(aecg: aecg100.Aecg100Client):
  print('output PPG frequency scan (1Hz-30Hz, 30sec) ...')
  scan = aecg100.structures.PPGFrequencyScan(
      **{
          'amplitude': 12.5,
          'dc': 625,
          'sync_pulse': aecg100.structures.SyncPulse.Off,
          'frequency_start': 1,
          'frequency_finish': 30,
          'duration': 30,
      })
  aecg.scan_ppg_frequency(scan)
  time.sleep(30)
  aecg.stop()


if __name__ == '__main__':
  client = get_aecg_client()
  client.connect()

  for func in [
      test_get_main_module_model_information,
      test_get_ppg_module_model_information,
      test_get_main_module_device_information,
      test_get_ppg_module_device_information,
      test_output_ecg_waveform_1hz_ecg,
      test_output_ecg_waveform_1hz_ecg_noise,
      test_output_ecg_waveform_1hz_sine,
      test_output_ecg_waveform_0_5hz_rectangle,
      test_output_ecg_frequency_scan,
      test_output_ppg60bpm,
      test_output_ppg60bpm_ac_offset_added,
      test_output_ppg60bpm_noise,
      test_output_ppg_frequency_scan,
  ]:
    func(client)
    print(f'{func.__name__} is finished')

  client.disconnect()
  print('all tests finished')

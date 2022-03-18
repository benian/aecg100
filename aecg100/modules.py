import ctypes

from typing import Sequence, Tuple
from aecg100 import structures

_SamplingCallback = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
_SamplingErrorCallback = ctypes.CFUNCTYPE(None, ctypes.c_int)


class _PpgModule:
  """PPG module API implementation."""

  def play_ppg_waveform(self, *waveforms: Tuple[structures.PPGChannel, structures.PPGWaveForm]) -> None:
    """Plays PPG waveform."""
    ch_nums = len(waveforms)
    if ch_nums == 1:
      self.handle.WTQOutputPPG(waveforms[0][0], ctypes.pointer(waveforms[0][1]), None)
    elif ch_nums == 2:
      self.handle.WTQOutputPPGEx(waveforms[0][1], waveforms[1][1], None, None)
    elif ch_nums == 3:
      self.handle.WTQOutputPPG3(waveforms[0][1], waveforms[1][1], waveforms[2][1], None, None, None)
    else:
      raise ValueError('the PPG has 3 channels at most')

  def play_ppg_rawdata(self, channel: structures.PPGChannel,
      sample_rate: int,
      ac: Sequence[float],
      dc: Sequence[float],
      sync_pulse: structures.SyncPulse,
      loop: bool,
      callback: structures.OutputSignalCallback = structures.OutputSignalCallback(0)) -> None:
    """Play PPG Raw data waveform."""
    if len(ac) != len(dc):
      raise ValueError('the number of AC and DC data is not equal')

    size = len(ac)
    SampleArray = ctypes.c_double * size
    ac_array = SampleArray(*ac)
    dc_array = SampleArray(*dc)

    raw_data = structures.RawData(
        sample_rate=sample_rate,
        size=size,
        ac=ctypes.addressof(ac_array),
        dc=ctypes.addressof(dc_array),
        output_signal_callback=callback)

    self.handle.WTQWaveformPlayerLoop(ctypes.c_bool(loop))
    self.handle.WTQWaveformPlayerOutputPPG(channel, ctypes.pointer(raw_data))

  def scan_ppg_frequency(self, scan: structures.PPGFrequencyScan) -> None:
    """Scans the PPG frequency."""
    self.handle.WTQOutputFrequencyScanPPG(structures.PPGChannel.Channel1, ctypes.pointer(scan), None)


class _EcgModule:
  """ECG module API implementation."""

  def play_ecg_waveform(self, waveform: structures.ECGWaveform) -> None:
    """Plays ECG waveform."""
    self.handle.WTQOutputECG(ctypes.pointer(waveform), None)

  def play_ecg_rawdata(
      self,
      sample_rate: int,
      ac: Sequence[float],
      dc: Sequence[float],
      loop: bool,
      callback: structures.OutputSignalCallback = structures.OutputSignalCallback(0)) -> None:
    """Play ECG Raw data waveform."""
    if len(ac) != len(dc):
      raise ValueError('the number of AC and DC data is not equal')

    size = len(ac)
    SampleArray = ctypes.c_double * size
    ac_array = SampleArray(*ac)
    dc_array = SampleArray(*dc)

    raw_data = structures.RawData(
        sample_rate=sample_rate,
        size=size,
        ac=ctypes.addressof(ac_array),
        dc=ctypes.addressof(dc_array),
        output_signal_callback=callback)

    self.handle.WTQWaveformPlayerLoop(ctypes.c_bool(loop))
    self.handle.WTQWaveformPlayerOutputECG(ctypes.pointer(raw_data))

  def scan_ecg_frequency(self, scan: structures.ECGFrequencyScan) -> None:
    """Scans the ECG frequency."""
    self.handle.WTQOutputFrequencyScan(ctypes.pointer(scan), None)


class _PwttModule:
  """PWTT module API implementation."""

  def play_ecg_ppg_waveform(
      self,
      diff_ptt_peak: int,
      ecg_waveform: structures.ECGWaveform,
      ppg_waveform: structures.PPGWaveForm,
  ) -> None:
    """Plays ECG and PPG waveform to compose PWTT outputs."""
    self.handle.WTQOutputECGAndPPG(
        diff_ptt_peak, ctypes.pointer(ecg_waveform), ctypes.pointer(ppg_waveform), None, None)

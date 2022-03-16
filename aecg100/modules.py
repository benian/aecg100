import ctypes

from typing import Tuple
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

  def scan_ppg_frequency(self, scan: structures.PPGFrequencyScan):
    """Scans the PPG frequency."""
    self.handle.WTQOutputFrequencyScanPPG(structures.PPGChannel.Channel1, ctypes.pointer(scan), None)


class _EcgModule:
  """ECG module API implementation."""

  def play_ecg_waveform(self, waveform: structures.ECGWaveform) -> None:
    """Plays ECG waveform."""
    self.handle.WTQOutputECG(ctypes.pointer(waveform), None)

  def scan_ecg_frequency(self, scan: structures.ECGFrequencyScan):
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

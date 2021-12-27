import ctypes
import logging
import threading
import time

from typing import Dict, Optional

from aecg100 import structures

logger = logging.getLogger('aecg100')

#
# AECG SDK Callback Types
#
_ConnectedCallback = ctypes.CFUNCTYPE(None, ctypes.c_bool)


def _load_cdll(sdk_path: str):
  """Loads SDK dynamic library."""
  handle = ctypes.cdll.LoadLibrary(sdk_path)
  handle.WTQInit.restype = ctypes.c_bool
  handle.WTQGetDeviceInformation.restype = ctypes.c_bool
  handle.WTQGetHWInformation.restype = ctypes.c_bool
  handle.WTQGetPPGDeviceInformation.restype = ctypes.c_bool
  handle.WTQGetPPGHWInformation.restype = ctypes.c_bool
  handle.WTQGetSerialNumber.restype = ctypes.c_char_p
  handle.WTQGetPPGSerialNumber.restype = ctypes.c_char_p
  return handle


class _Aecg100Base:
  """AECG100 client base.

  Attributes:
    is_connected: indicates the device is connected.
    handle: the device handle object to access the device.
    module_info: the main module info.
    ppg_module_info: the PPG module info.
    device_info: the main device info.
    ppg_device_info the ppg device info.
  """

  def __init__(self, sdk_path: str):
    self._handle = _load_cdll(sdk_path)
    self._connection_cb = _ConnectedCallback(self._connection_handler)
    self._is_connected = threading.Event()
    self._wait_cb = threading.Event()

  def _connection_handler(self, connected: bool) -> None:
    if connected:
      self._is_connected.set()
    self._wait_cb.set()

  @property
  def is_connected(self):
    return self._is_connected.is_set()

  @property
  def handle(self):
    if not self.is_connected:
      raise RuntimeError('device is not connected')
    return self._handle

  def connect(self, timeout: Optional[float] = 15) -> None:
    """Connects to the device.

    Raises:
      RuntimeError: failed to connect to the device.
    """
    if self.is_connected:
      logging.warning('AECG100 is already connected.')
      return

    if not self._handle.WTQInit(self._connection_cb):
      self._handle.WTQFree()
      raise RuntimeError('Failed to initialize the device')

    if not self._wait_cb.wait(timeout):
      raise RuntimeError('AECG device is not response')

    if not self.is_connected:
      raise RuntimeError('Failed connecting to the device')

    self._wait_cb.clear()
    logging.info('AECG100 is connected.')

  def disconnect(self) -> None:
    """Disconnects from the device."""
    if not self.is_connected:
      logging.warning('AECG100 is not connected.')
      return

    self.stop()
    self._handle.WTQFree()
    # Uses workaround to sleep 1s here due to the limitation of AECG100 SDK.
    # We currently do not have better way to handle the disconnect() callback
    # function since the AECG100 SDK does not support blocking on disconnect()
    # There is a problem observed when disconnect() and re-connect() is very
    # close in terms of invoked time. Thus here I experimented a workaround
    # and figured out that sleep 1s is enough to keep the re-connect() safe.
    # For reference, I have tested 100 times disconnect() re-connect() and
    # this workaround 100% pass on my local workstation.
    time.sleep(1)
    self._is_connected.clear()
    logging.info('AECG100 is disconnected.')

  def stop(self) -> None:
    """Stops output waveform."""
    self.handle.WTQStopOutputWaveform()
    logging.info('AECG100 stopped output waveform.')

  @property
  def module_info(self) -> Dict[str, str]:
    info = structures.HWInformation()
    self.handle.WTQGetHWInformation(ctypes.pointer(info))

    return {
        'serial': self.handle.WTQGetSerialNumber().decode('ascii'),
        'firmware': f'{info.fw_main_version}.{info.fw_sub_version}',
        'hardware': f'{info.pcb_version}.{info.hw_version}'
    }

  @property
  def ppg_module_info(self) -> Dict[str, str]:
    info = structures.HWInformation()
    self.handle.WTQGetPPGHWInformation(ctypes.pointer(info))

    return {
        'serial': self.handle.WTQGetPPGSerialNumber().decode('ascii'),
        'firmware': f'{info.fw_main_version}.{info.fw_sub_version}',
        'hardware': f'{info.pcb_version}.{info.hw_version}'
    }

  @property
  def device_info(self) -> Dict[str, str]:
    info = structures.ModelInformation()
    self.handle.WTQGetDeviceInformation(ctypes.pointer(info))
    return info.dump()

  @property
  def ppg_device_info(self) -> Dict[str, str]:
    info = structures.ModelInformation()
    self.handle.WTQGetPPGDeviceInformation(ctypes.pointer(info))
    return info.dump()

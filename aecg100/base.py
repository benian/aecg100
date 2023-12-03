import ctypes
import logging
import time

from typing import Any, Dict, Optional

from aecg100 import structures

logger = logging.getLogger('aecg100')


def _load_cdll(sdk_path: str) -> ctypes.CDLL:
  """Loads SDK dynamic library."""
  handle = ctypes.cdll.LoadLibrary(sdk_path)
  handle.WTQConnect.restype = ctypes.c_bool
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
    """Initiates the client instance.

    Args:
      sdk_path: the fullpath of the sdk dynamic library.
    """
    self._handle = _load_cdll(sdk_path)
    self._is_connected = False

  @property
  def is_connected(self):
    return self._is_connected

  @property
  def handle(self):
    if not self.is_connected:
      raise RuntimeError('device is not connected')
    return self._handle

  def connect(self,
              port: Optional[int] = -1,
              timeout: Optional[float] = 15) -> None:
    """Connects to the device.

    Args:
      port: ttyACM port number, -1 means the port is auto-selected
      timeout: the number of seconds to connect
    Raises:
      RuntimeError: failed to connect to the device.
    """
    if self.is_connected:
      logging.warning('AECG100 is already connected.')
      return

    if not self._handle.WTQConnect(port, timeout * 1000):
      self._handle.WTQFree()
      raise RuntimeError('Failed to connect to the device')

    self._is_connected = True

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
    self._is_connected = False
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
  def device_info(self) -> Dict[str, Any]:
    info = structures.ModelInformation()
    self.handle.WTQGetDeviceInformation(ctypes.pointer(info))
    return info.dump()

  @property
  def ppg_device_info(self) -> Dict[str, Any]:
    info = structures.ModelInformation()
    self.handle.WTQGetPPGDeviceInformation(ctypes.pointer(info))
    return info.dump()

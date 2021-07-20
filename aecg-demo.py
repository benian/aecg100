from ctypes import *
import struct
import threading
from enum import Enum
import time
import sys
import platform

pd1 = []
completedEvent = threading.Event()


#
# AECG SDK
#
ConnectedCallback = CFUNCTYPE(None, c_bool)
OutputSignalCallback = CFUNCTYPE(None, c_double, c_int, c_int)
SamplingCallback = CFUNCTYPE(None, c_int, c_int)
SamplingErrorCallback = CFUNCTYPE(None, c_int)


class PPGChannel(Enum):
    PPGChannel1 = 1
    PPGChannel2 = 2


class ECGWaveformType (Enum):
    ECGWaveformTypeSine = 0
    ECGWaveformTypeTriangle = 1
    ECGWaveformTypeSquare = 2
    ECGWaveformTypeRectanglePulse = 3
    ECGWaveformTypeTrianglePulse = 4
    ECGWaveformTypeExponential = 5
    ECGWaveformTypeECG = 6


class Electrode (Enum):
    ElectrodeRightArm = 0     # RA
    ElectrodeLeftArm = 0xff   # LA


class ECGImpedance (Enum):
    ECGImpedanceOff = 0       # Disable impedance
    ECGImpedanceOn = 0xff     # Enable 620K impedance


class ECGPacingEnable (Enum):
    ECGPacingOff = 0
    ECGPacingOn = 0xff


class ECGRespirationEnable (Enum):
    ECGRespirationOff = 0
    ECGRespirationOn = 0xff


class ECGNoiseFrequency (Enum):
    ECGNoiseFrequencyOff = 0
    ECGNoiseFrequency50Hz = 1
    ECGNoiseFrequency60Hz = 2
    ECGNoiseFrequency100Hz = 3
    ECGNoiseFrequency120Hz = 4


class PPGWaveformType (Enum):
    PPGWaveformTypeSine = 0
    PPGWaveformTypeTriangle = 1
    PPGWaveformTypeSquare = 2
    PPGWaveformTypePPG = 3


class PPGNoiseFrequency (Enum):
    PPGNoiseFrequencyOff = 0
    PPGNoiseFrequency50Hz = 1
    PPGNoiseFrequency60Hz = 2
    PPGNoiseFrequency1KHz = 3
    PPGNoiseFrequency5KHz = 4
    PPGNoiseFrequency100Hz = 5
    PPGNoiseFrequency120Hz = 6
    PPGNoiseFrequencyWhiteNoise = 7


class LEDMode (Enum):
    LEDModeOff = 0
    LEDModeOn = 1


class LEDType (Enum):
    LEDTypeGreen = 0
    LEDTypeRed = 1
    LEDTypeIR = 2
    LEDTypeNone = 3


class SyncPulse (Enum):
    SyncPulseLEDOff = 0
    SyncPulseSync = 1
    SyncPulseSyncOff = 2


class PPGInverted (Enum):
    PPGInvertedOff = 0
    PPGInvertedOn = 1


class PPGSampling (Enum):
    PPGSamplingChannel1PD = 0
    PPGSamplingChannel2PD = 1
    PPGSamplingChannel1Switch = 2
    PPGSamplingChannel2Switch = 3
    PPGSamplingMax = 4


class HW_INFORMATION (Structure):
    _fields_ = [
        ('FWMainVersion', c_int),
        ('FWSubVersion', c_int),
        ('HWVersion', c_int),
        ('PCBVersion', c_int)
    ]


class MODEL_INFORMATION (Structure):
    _fields_ = [
        ('ProductName', c_char * 2),
        ('GenerationNumber', c_char),
        ('ModelNumber', c_char),
        ('SerialNumber', c_int),
        ('Year', c_int),
        ('LEDType1', c_int),
        ('LEDType2', c_int),
        ('LEDType3', c_int)
    ]


class ECG_WAVEFORM (Structure):
    _fields_ = [
        ('WaveformType', c_int),
        ('Frequency', c_double),
        ('Amplitude', c_double),
        ('TWave', c_double),
        ('PWave', c_double),
        ('STSegment', c_double),
        ('DCOffsetVariable', c_int),
        ('DCOffset', c_int),
        ('TimePeriod', c_int),
        ('PRInterval', c_int),
        ('QRSDuration', c_int),
        ('TDuration', c_int),
        ('QTInterval', c_int),
        ('Impedance', c_int),
        ('Electrode', c_int),
        ('PulseWidth', c_int),
        ('NoiseAmplitude', c_double),
        ('NoiseFrequency', c_int),
        ('PacingEnabled', c_int),
        ('PacingAmplitude', c_double),
        ('PacingDuration', c_double),
        ('PacingRate', c_int),
        ('RespirationEnabled', c_int),
        ('RespirationAmplitude', c_int),
        ('RespirationRate', c_int),
        ('RespirationRatio', c_int),
        ('RespirationBaseline', c_int),
        ('RespirationApneaDuration', c_int),
        ('RespirationApneaCycle', c_int),
        ('Reserved', c_char * 12)
    ]


class PPG_WAVEFORM (Structure):
    _fields_ = [
        ('WaveformType', c_int),
        ('Frequency', c_double),
        ('VolDC', c_double),
        ('VolSP', c_double),
        ('VolDN', c_double),
        ('VolDP', c_double),
        ('ACOffset', c_double),
        ('TimeSP', c_int),
        ('TimeDN', c_int),
        ('TimeDP', c_int),
        ('TimePeriod', c_int),
        ('SyncPulse', c_int),
        ('Inverted', c_int),
        ('NoiseAmplitude', c_double),
        ('NoiseFrequency', c_int),
        ('RespirationEnabled', c_int),
        ('RespirationRate', c_int),
        ('RespirationVariation', c_int),
        ('RespirationInExhaleRatio', c_int),
        ('Reserved', c_char * 16)
    ]


class FREQUENCY_SCAN (Structure):
    _fields_ = [
        ('Amplitude', c_double),
        ('FrequencyStart', c_double),
        ('FrequencyFinish', c_double),
        ('Duration', c_int)
    ]


class FREQUENCY_SCAN2 (Structure):
    _fields_ = [
        ('Amplitude', c_double),
        ('DC', c_double),
        ('SyncPulse', c_int),
        ('FrequencyStart', c_double),
        ('FrequencyFinish', c_double),
        ('Duration', c_int)
    ]


class PLAY_RAW_DATA (Structure):
    _fields_ = [
        ('SampleRate', c_double),
        ('Size', c_int),
        ('SyncPulse', c_int),
        ('AC', c_void_p),
        ('DC', c_void_p),
        ('OutputSignalCallback', OutputSignalCallback)
    ]

if platform.machine() == 'aarch64':
    device = cdll.LoadLibrary ("sdk/libaecgrpix64.so")
elif platform.machine() == 'armv7l': 
    device = cdll.LoadLibrary ("sdk/libaecgrpix86.so")
elif platform.machine() == 'x86_64': 
    device = cdll.LoadLibrary ("sdk/libaecgx64.so")
else:
    device = cdll.LoadLibrary ("sdk/libaecgx86.so")


device.WTQInit.restype = c_bool
device.WTQGetSerialNumber.restype = c_char_p
device.WTQGetPPGSerialNumber.restype = c_char_p


def TestGetMainModuleModelInformation():
    print("get main module model information...", end='')

    hwInfo = HW_INFORMATION()
    device.WTQGetHWInformation(pointer(hwInfo))

    print('{:s}, FW Ver.: {:d}.{:d}, HW Ver.: {:d}.{:d}'.format(device.WTQGetSerialNumber().decode(
        'ascii'), hwInfo.FWMainVersion, hwInfo.FWSubVersion, hwInfo.PCBVersion, hwInfo.HWVersion))


def TestGetPPGModuleModelInformation():
    print("get ppg module model information...", end='')

    hwInfo = HW_INFORMATION()
    device.WTQGetPPGHWInformation(pointer(hwInfo))

    print('{:s}, HW Ver.: {:d}.{:d}'.format(device.WTQGetPPGSerialNumber().decode(
        'ascii'), hwInfo.PCBVersion, hwInfo.HWVersion))


def TestOutputECGWaveform1HzECG():
    print('output ECG (1Hz, 1mV, ECG, RA) ...', end='')
    sys.stdout.flush()

    waveform = ECG_WAVEFORM()
    waveform.WaveformType = ECGWaveformType.ECGWaveformTypeECG.value
    waveform.Frequency = 1
    waveform.Amplitude = 1.0
    waveform.TWave = 0.2
    waveform.PWave = 0.2
    waveform.STSegment = 0
    waveform.DCOffsetVariable = 0
    waveform.DCOffset = 0
    waveform.TimePeriod = 1000
    waveform.PRInterval = 160
    waveform.QRSDuration = 100
    waveform.TDuration = 180
    waveform.QTInterval = 350
    waveform.Impedance = ECGImpedance.ECGImpedanceOff.value
    waveform.Electrode = Electrode.ElectrodeRightArm.value
    waveform.PulseWidth = 100
    waveform.NoiseAmplitude = 0
    waveform.NoiseFrequency = ECGNoiseFrequency.ECGNoiseFrequencyOff.value
    waveform.PacingEnabled = 0
    waveform.PacingAmplitude = 2
    waveform.PacingDuration = 2
    waveform.PacingRate = 60
    waveform.RespirationEnabled = 0
    waveform.RespirationAmplitude = 1000
    waveform.RespirationRate = 20
    waveform.RespirationBaseline = 1000
    waveform.RespirationRatio = 1
    waveform.RespirationApneaDuration = 10
    waveform.RespirationApneaCycle = 1

    device.WTQOutputECG(pointer(waveform), None)

    time.sleep(10)
    print('done')
    device.WTQStopOutputWaveform()


def TestOutputECGWaveform1HzECGNoise():
    print('output ECG (1Hz, 4mV, ECG, RA, Noise: 50Hz, 0.5mV) ...', end='')
    sys.stdout.flush()

    waveform = ECG_WAVEFORM()
    waveform.WaveformType = ECGWaveformType.ECGWaveformTypeECG.value
    waveform.Frequency = 1
    waveform.Amplitude = 4.0
    waveform.TWave = 0.2
    waveform.PWave = 0.2
    waveform.STSegment = 0
    waveform.DCOffsetVariable = 0
    waveform.DCOffset = 0
    waveform.TimePeriod = 1000
    waveform.PRInterval = 160
    waveform.QRSDuration = 100
    waveform.TDuration = 180
    waveform.QTInterval = 350
    waveform.Impedance = ECGImpedance.ECGImpedanceOff.value
    waveform.Electrode = Electrode.ElectrodeRightArm.value
    waveform.PulseWidth = 100
    waveform.NoiseAmplitude = 0.5
    waveform.NoiseFrequency = ECGNoiseFrequency.ECGNoiseFrequency50Hz.value
    waveform.PacingEnabled = 0
    waveform.PacingAmplitude = 2
    waveform.PacingDuration = 2
    waveform.PacingRate = 60
    waveform.RespirationEnabled = 0
    waveform.RespirationAmplitude = 1000
    waveform.RespirationRate = 20
    waveform.RespirationBaseline = 1000
    waveform.RespirationRatio = 1
    waveform.RespirationApneaDuration = 10
    waveform.RespirationApneaCycle = 1

    device.WTQOutputECG(pointer(waveform), None)

    time.sleep(10)
    print('done')
    device.WTQStopOutputWaveform()


def TestOutputECGWaveform1HzSine():
    print('output ECG (1Hz, 1mV, Sine, RA) ...', end='')
    sys.stdout.flush()

    waveform = ECG_WAVEFORM()
    waveform.WaveformType = ECGWaveformType.ECGWaveformTypeSine.value
    waveform.Frequency = 1
    waveform.Amplitude = 1.0
    waveform.TWave = 0.2
    waveform.PWave = 0.2
    waveform.STSegment = 0
    waveform.DCOffsetVariable = 0
    waveform.DCOffset = 0
    waveform.TimePeriod = 1000
    waveform.PRInterval = 160
    waveform.QRSDuration = 100
    waveform.TDuration = 180
    waveform.QTInterval = 350
    waveform.Impedance = ECGImpedance.ECGImpedanceOff.value
    waveform.Electrode = Electrode.ElectrodeRightArm.value
    waveform.PulseWidth = 100
    waveform.NoiseAmplitude = 0
    waveform.NoiseFrequency = ECGNoiseFrequency.ECGNoiseFrequencyOff.value
    waveform.PacingEnabled = 0
    waveform.PacingAmplitude = 2
    waveform.PacingDuration = 2
    waveform.PacingRate = 60
    waveform.RespirationEnabled = 0
    waveform.RespirationAmplitude = 1000
    waveform.RespirationRate = 20
    waveform.RespirationBaseline = 1000
    waveform.RespirationRatio = 1
    waveform.RespirationApneaDuration = 10
    waveform.RespirationApneaCycle = 1

    device.WTQOutputECG(pointer(waveform), None)

    time.sleep(10)
    print('done')
    device.WTQStopOutputWaveform()


def TestOutputECGWaveform05HzRectangle():
    print('output ECG (0.5Hz, 1mv, Rectangle, RA) ...', end='')
    sys.stdout.flush()

    waveform = ECG_WAVEFORM()
    waveform.WaveformType = ECGWaveformType.ECGWaveformTypeSquare.value
    waveform.Frequency = 0.5
    waveform.Amplitude = 1.0
    waveform.TWave = 0.2
    waveform.PWave = 0.2
    waveform.STSegment = 0
    waveform.DCOffsetVariable = 0
    waveform.DCOffset = 0
    waveform.TimePeriod = 2000
    waveform.PRInterval = 160
    waveform.QRSDuration = 100
    waveform.TDuration = 180
    waveform.QTInterval = 350
    waveform.Impedance = ECGImpedance.ECGImpedanceOff.value
    waveform.Electrode = Electrode.ElectrodeRightArm.value
    waveform.PulseWidth = 100
    waveform.NoiseAmplitude = 0
    waveform.NoiseFrequency = ECGNoiseFrequency.ECGNoiseFrequencyOff.value
    waveform.PacingEnabled = 0
    waveform.PacingAmplitude = 2
    waveform.PacingDuration = 2
    waveform.PacingRate = 60
    waveform.RespirationEnabled = 0
    waveform.RespirationAmplitude = 1000
    waveform.RespirationRate = 20
    waveform.RespirationBaseline = 1000
    waveform.RespirationRatio = 1
    waveform.RespirationApneaDuration = 10
    waveform.RespirationApneaCycle = 1

    device.WTQOutputECG(pointer(waveform), None)

    time.sleep(10)
    print('done')
    device.WTQStopOutputWaveform()


def TestOutputECGFrequencyScan():
    print('output ECG frequency scan (0.5Hz-150Hz, 30sec) ...', end='')
    sys.stdout.flush()

    scan = FREQUENCY_SCAN()
    scan.Amplitude = 1
    scan.FrequencyStart = 0.5
    scan.FrequencyFinish = 150
    scan.Duration = 30

    device.WTQOutputFrequencyScan(pointer(scan), None)

    time.sleep(31)
    print('done')
    device.WTQStopOutputWaveform()


def TestSetDCOffset():
    print('set DC offset to +300mV ...', end='')
    sys.stdout.flush()
    device.WTQDeviceSetDCOffset(300)
    time.sleep(10)
    print('done')

    print('set DC offset to -300mV ...', end='')
    sys.stdout.flush()
    device.WTQDeviceSetDCOffset(-300)
    time.sleep(10)
    print('done')


def TestSetDCOffsetVariable():
    # +200 mV
    print('set DC offset variable to +200mV ...', end='')
    sys.stdout.flush()

    waveform = ECG_WAVEFORM()
    waveform.WaveformType = ECGWaveformType.ECGWaveformTypeSine.value
    waveform.Frequency = 1
    waveform.Amplitude = 0
    waveform.TWave = 0.2
    waveform.PWave = 0.2
    waveform.STSegment = 0
    waveform.DCOffsetVariable = 1
    waveform.DCOffset = 200
    waveform.TimePeriod = 1000
    waveform.PRInterval = 160
    waveform.QRSDuration = 100
    waveform.TDuration = 180
    waveform.QTInterval = 350
    waveform.Impedance = ECGImpedance.ECGImpedanceOff.value
    waveform.Electrode = Electrode.ElectrodeRightArm.value
    waveform.PulseWidth = 100
    waveform.NoiseAmplitude = 0
    waveform.NoiseFrequency = ECGNoiseFrequency.ECGNoiseFrequencyOff.value
    waveform.PacingEnabled = 0
    waveform.PacingAmplitude = 2
    waveform.PacingDuration = 2
    waveform.PacingRate = 60
    waveform.RespirationEnabled = 0
    waveform.RespirationAmplitude = 1000
    waveform.RespirationRate = 20
    waveform.RespirationBaseline = 1000
    waveform.RespirationRatio = 1
    waveform.RespirationApneaDuration = 10
    waveform.RespirationApneaCycle = 1

    device.WTQOutputECG(pointer(waveform), None)

    time.sleep(10)
    print('done')

    # +500 mV
    print('set DC offset variable to +500mV ...', end='')
    sys.stdout.flush()
    waveform.DCOffset = 500
    device.WTQOutputECG(pointer(waveform), None)
    time.sleep(10)
    print('done')

    # -200 mV
    print('set DC offset variable to -200mV ...', end='')
    sys.stdout.flush()
    waveform.DCOffset = -200
    device.WTQOutputECG(pointer(waveform), None)
    time.sleep(10)
    print('done')

    # -500 mV
    print('set DC offset variable to -500mV ...', end='')
    sys.stdout.flush()
    waveform.DCOffset = -500
    device.WTQOutputECG(pointer(waveform), None)
    time.sleep(10)
    print('done')

    device.WTQStopOutputWaveform()


def TestECGPlayRaw():
    print('ecg play raw (1Hz, 5mV)...', end='')
    sys.stdout.flush()

    playRaw = PLAY_RAW_DATA()
    lineNumber = 0
    f = open('ecg-1hz-5mv.txt')
    for x in f:
        if lineNumber == 0:
            playRaw.SampleRate = int(x)
        elif lineNumber == 1:
            playRaw.Size = int(x)
            ac = (c_double * playRaw.Size)()
            dc = (c_double * playRaw.Size)()
        elif lineNumber >= 4:
            ac[lineNumber-4] = float(x)
            dc[lineNumber-4] = 0

        lineNumber = lineNumber + 1

    f.close()

    playRaw.AC = addressof(ac)
    playRaw.DC = addressof(dc)
    playRaw.OutputSignalCallback = OutputSignalCallback(0)

    device.WTQWaveformPlayerLoop(c_bool(True))
    device.WTQWaveformPlayerOutputECG(pointer(playRaw))

    time.sleep(10)
    print('done')
    device.WTQStopOutputWaveform()


def TestOutputPWTT60BPM():
    print('output PWTT (60BPM; ECG: 1mv, RA; PPG: 12.5mV, SyncOff; PTTp: 500ms) ...', end='')
    sys.stdout.flush()

    ecgWaveform = ECG_WAVEFORM()
    ecgWaveform.WaveformType = ECGWaveformType.ECGWaveformTypeECG.value
    ecgWaveform.Frequency = 1
    ecgWaveform.Amplitude = 1.0
    ecgWaveform.TWave = 0.2
    ecgWaveform.PWave = 0.2
    ecgWaveform.STSegment = 0
    ecgWaveform.DCOffsetVariable = 0
    ecgWaveform.DCOffset = 0
    ecgWaveform.TimePeriod = 1000
    ecgWaveform.PRInterval = 160
    ecgWaveform.QRSDuration = 100
    ecgWaveform.TDuration = 180
    ecgWaveform.QTInterval = 350
    ecgWaveform.Impedance = ECGImpedance.ECGImpedanceOff.value
    ecgWaveform.Electrode = Electrode.ElectrodeRightArm.value
    ecgWaveform.PulseWidth = 100
    ecgWaveform.NoiseAmplitude = 0
    ecgWaveform.NoiseFrequency = ECGNoiseFrequency.ECGNoiseFrequencyOff.value
    ecgWaveform.PacingEnabled = 0
    ecgWaveform.PacingAmplitude = 2
    ecgWaveform.PacingDuration = 2
    ecgWaveform.PacingRate = 60
    ecgWaveform.RespirationEnabled = 0
    ecgWaveform.RespirationAmplitude = 1000
    ecgWaveform.RespirationRate = 20
    ecgWaveform.RespirationBaseline = 1000
    ecgWaveform.RespirationRatio = 1
    ecgWaveform.RespirationApneaDuration = 10
    ecgWaveform.RespirationApneaCycle = 1

    ppgWaveform = PPG_WAVEFORM()
    ppgWaveform.Frequency = 1
    ppgWaveform.WaveformType = PPGWaveformType.PPGWaveformTypePPG.value
    ppgWaveform.VolDC = 625
    ppgWaveform.VolSP = 12.5
    ppgWaveform.VolDN = 7.0
    ppgWaveform.VolDP = 8.0
    ppgWaveform.ACOffset = 0
    ppgWaveform.TimePeriod = 1000
    ppgWaveform.TimeSP = 150
    ppgWaveform.TimeDN = 360
    ppgWaveform.TimeDP = 460
    ppgWaveform.SyncPulse = SyncPulse.SyncPulseSyncOff.value
    ppgWaveform.Inverted = PPGInverted.PPGInvertedOn.value
    ppgWaveform.NoiseAmplitude = 0
    ppgWaveform.NoiseFrequency = PPGNoiseFrequency.PPGNoiseFrequencyOff.value
    ppgWaveform.RespirationEnabled = 0
    ppgWaveform.RespirationRate = 30
    ppgWaveform.RespirationVariation = 1
    ppgWaveform.RespirationInExhaleRatio = 1

    device.WTQOutputECGAndPPG(500, pointer(
        ecgWaveform), pointer(ppgWaveform), None, None)

    time.sleep(10)
    print('done')
    device.WTQStopOutputWaveform()


def TestOutputPWTT60BPMSquare():
    print('output PWTT (60BPM; ECG-Square: 1mv, RA; PPG-Square: 12.5mV, SyncOff; PTTp: 600ms) ...', end='')
    sys.stdout.flush()

    ecgWaveform = ECG_WAVEFORM()
    ecgWaveform.WaveformType = ECGWaveformType.ECGWaveformTypeSquare.value
    ecgWaveform.Frequency = 1
    ecgWaveform.Amplitude = 1.0
    ecgWaveform.TWave = 0.2
    ecgWaveform.PWave = 0.2
    ecgWaveform.STSegment = 0
    ecgWaveform.DCOffsetVariable = 0
    ecgWaveform.DCOffset = 0
    ecgWaveform.TimePeriod = 1000
    ecgWaveform.PRInterval = 160
    ecgWaveform.QRSDuration = 100
    ecgWaveform.TDuration = 180
    ecgWaveform.QTInterval = 350
    ecgWaveform.Impedance = ECGImpedance.ECGImpedanceOff.value
    ecgWaveform.Electrode = Electrode.ElectrodeRightArm.value
    ecgWaveform.PulseWidth = 100
    ecgWaveform.NoiseAmplitude = 0
    ecgWaveform.NoiseFrequency = ECGNoiseFrequency.ECGNoiseFrequencyOff.value
    ecgWaveform.PacingEnabled = 0
    ecgWaveform.PacingAmplitude = 2
    ecgWaveform.PacingDuration = 2
    ecgWaveform.PacingRate = 60
    ecgWaveform.RespirationEnabled = 0
    ecgWaveform.RespirationAmplitude = 1000
    ecgWaveform.RespirationRate = 20
    ecgWaveform.RespirationBaseline = 1000
    ecgWaveform.RespirationRatio = 1
    ecgWaveform.RespirationApneaDuration = 10
    ecgWaveform.RespirationApneaCycle = 1

    ppgWaveform = PPG_WAVEFORM()
    ppgWaveform.Frequency = 1
    ppgWaveform.WaveformType = PPGWaveformType.PPGWaveformTypeSquare.value
    ppgWaveform.VolDC = 625
    ppgWaveform.VolSP = 12.5
    ppgWaveform.VolDN = 7.0
    ppgWaveform.VolDP = 8.0
    ppgWaveform.TimePeriod = 1000
    ppgWaveform.TimeSP = 150
    ppgWaveform.TimeDN = 360
    ppgWaveform.TimeDP = 460
    ppgWaveform.SyncPulse = SyncPulse.SyncPulseSyncOff.value
    ppgWaveform.Inverted = PPGInverted.PPGInvertedOn.value
    ppgWaveform.NoiseAmplitude = 0
    ppgWaveform.NoiseFrequency = PPGNoiseFrequency.PPGNoiseFrequencyOff.value
    ppgWaveform.RespirationEnabled = 0
    ppgWaveform.RespirationRate = 30
    ppgWaveform.RespirationVariation = 1
    ppgWaveform.RespirationInExhaleRatio = 1

    device.WTQOutputECGAndPPG(600, pointer(
        ecgWaveform), pointer(ppgWaveform), None, None)

    time.sleep(10)
    print('done')
    device.WTQStopOutputWaveform()


def TestOutputPPG60BPM():
    print('output PPG (60BPM, 12.5mV, SyncOff) ...', end='')
    sys.stdout.flush()

    ppgWaveform = PPG_WAVEFORM()
    ppgWaveform.Frequency = 1
    ppgWaveform.WaveformType = PPGWaveformType.PPGWaveformTypePPG.value
    ppgWaveform.VolDC = 625
    ppgWaveform.VolSP = 12.5
    ppgWaveform.VolDN = 7.0
    ppgWaveform.VolDP = 8.0
    ppgWaveform.ACOffset = 0
    ppgWaveform.TimePeriod = 1000
    ppgWaveform.TimeSP = 150
    ppgWaveform.TimeDN = 360
    ppgWaveform.TimeDP = 460
    ppgWaveform.SyncPulse = SyncPulse.SyncPulseSyncOff.value
    ppgWaveform.Inverted = PPGInverted.PPGInvertedOn.value
    ppgWaveform.NoiseAmplitude = 0
    ppgWaveform.NoiseFrequency = PPGNoiseFrequency.PPGNoiseFrequencyOff.value
    ppgWaveform.RespirationEnabled = 0
    ppgWaveform.RespirationRate = 30
    ppgWaveform.RespirationVariation = 1
    ppgWaveform.RespirationInExhaleRatio = 1

    device.WTQOutputPPG(PPGChannel.PPGChannel1.value,
                        pointer(ppgWaveform), None)

    time.sleep(10)
    print('done')
    device.WTQStopOutputWaveform()


def TestOutputPPG60BPMAcOffsetAdded():
    print('output PPG (60BPM, 12.5mV, SyncOff, AC Offset=2mV) ...', end='')
    sys.stdout.flush()

    ppgWaveform = PPG_WAVEFORM()
    ppgWaveform.Frequency = 1
    ppgWaveform.WaveformType = PPGWaveformType.PPGWaveformTypePPG.value
    ppgWaveform.VolDC = 625
    ppgWaveform.VolSP = 12.5
    ppgWaveform.VolDN = 7.0
    ppgWaveform.VolDP = 8.0
    ppgWaveform.ACOffset = 2
    ppgWaveform.TimePeriod = 1000
    ppgWaveform.TimeSP = 150
    ppgWaveform.TimeDN = 360
    ppgWaveform.TimeDP = 460
    ppgWaveform.SyncPulse = SyncPulse.SyncPulseSyncOff.value
    ppgWaveform.Inverted = PPGInverted.PPGInvertedOn.value
    ppgWaveform.NoiseAmplitude = 0
    ppgWaveform.NoiseFrequency = PPGNoiseFrequency.PPGNoiseFrequencyOff.value
    ppgWaveform.RespirationEnabled = 0
    ppgWaveform.RespirationRate = 30
    ppgWaveform.RespirationVariation = 1
    ppgWaveform.RespirationInExhaleRatio = 1

    device.WTQOutputPPG(PPGChannel.PPGChannel1.value,
                        pointer(ppgWaveform), None)

    time.sleep(10)
    print('done')
    device.WTQStopOutputWaveform()


def TestOutputPPG60BPMNoise():
    print('output PPG (60BPM, 12.5mV, SyncOff, Noise: 50Hz, 2mV) ...', end='')
    sys.stdout.flush()

    ppgWaveform = PPG_WAVEFORM()
    ppgWaveform.Frequency = 1
    ppgWaveform.WaveformType = PPGWaveformType.PPGWaveformTypePPG.value
    ppgWaveform.VolDC = 625
    ppgWaveform.VolSP = 12.5
    ppgWaveform.VolDN = 7.0
    ppgWaveform.VolDP = 8.0
    ppgWaveform.ACOffset = 0
    ppgWaveform.TimePeriod = 1000
    ppgWaveform.TimeSP = 150
    ppgWaveform.TimeDN = 360
    ppgWaveform.TimeDP = 460
    ppgWaveform.SyncPulse = SyncPulse.SyncPulseSyncOff.value
    ppgWaveform.Inverted = PPGInverted.PPGInvertedOn.value
    ppgWaveform.NoiseAmplitude = 2
    ppgWaveform.NoiseFrequency = PPGNoiseFrequency.PPGNoiseFrequency50Hz.value
    ppgWaveform.RespirationEnabled = 0
    ppgWaveform.RespirationRate = 30
    ppgWaveform.RespirationVariation = 1
    ppgWaveform.RespirationInExhaleRatio = 1

    device.WTQOutputPPG(PPGChannel.PPGChannel1.value,
                        pointer(ppgWaveform), None)

    time.sleep(10)
    print('done')
    device.WTQStopOutputWaveform()


def TestPPGPDSampling():
    print('\rppg channel-1 pd sampling...', end='')
    samplingCb = SamplingCallback(Channel1PDSamplingHandler)
    samplingErrorCb = SamplingErrorCallback(SamplingErrorHandler)

    device.WTQEnableSampling(
        PPGSampling.PPGSamplingChannel1PD.value, samplingCb)

    device.WTQStartSampling(samplingErrorCb)
    time.sleep(10)

    device.WTQDisableSampling()
    print('')
    print('ppg channel-1 pd sampling...done')


def TestPPGPlayRaw():
    print('ppg play raw (2Hz, rectangle pulse, 100ms)...', end='')
    sys.stdout.flush()

    playRaw = PLAY_RAW_DATA()
    playRaw.SampleRate = 1000
    playRaw.Size = 1000
    playRaw.SyncPulse = SyncPulse.SyncPulseSyncOff.value

    SampleArray = c_double * playRaw.Size
    ac = SampleArray()
    for i in range(300):
        ac[i] = 0

    dc = SampleArray()
    for i in range(100):
        dc[i] = 3000
        dc[i+500] = 3000

    playRaw.AC = addressof(ac)
    playRaw.DC = addressof(dc)
    playRaw.OutputSignalCallback = OutputSignalCallback(0)

    device.WTQWaveformPlayerLoop(c_bool(True))
    device.WTQWaveformPlayerOutputPPG(
        PPGChannel.PPGChannel1.value, pointer(playRaw))

    time.sleep(10)
    print('done')
    device.WTQStopOutputWaveform()


def TestOutputPPGFrequencyScan():
    print('output PPG frequency scan (1Hz-30Hz, 30sec) ...', end='')
    sys.stdout.flush()

    scan = FREQUENCY_SCAN2()
    scan.Amplitude = 12.5
    scan.DC = 625
    scan.SyncPulse = SyncPulse.SyncPulseSyncOff.value
    scan.FrequencyStart = 1
    scan.FrequencyFinish = 30
    scan.Duration = 30
    device.WTQOutputFrequencyScanPPG(
        PPGChannel.PPGChannel1.value, pointer(scan), None)

    time.sleep(31)
    print('done')
    device.WTQStopOutputWaveform()


def DeviceConnectedHandler(connected):
    if connected:
        print('device is connected')
        thread = threading.Thread(target=StartTest)
        thread.start()
    else:
        print('device is disconnected')


def Channel1PDSamplingHandler(data, number):
    global pd1
    average_count = 1000

    while number != 0:
        append = min(number, average_count - len(pd1))
        number -= append
        pd1 += [data] * append

        if len(pd1) == average_count:
            average = 0
            for x in pd1:
                average += x

            average /= average_count
            print('\rppg channel-1 pd sampling...' + str(average), end='')
            pd1 = []


def SamplingErrorHandler(error):
    print('sampling error... ' + error)


def StartTest():
    time.sleep(3)
    TestGetMainModuleModelInformation()
    TestGetPPGModuleModelInformation()
    TestOutputECGWaveform1HzECG()
    TestOutputECGWaveform1HzECGNoise()
    TestOutputECGWaveform1HzSine()
    TestOutputECGWaveform05HzRectangle()
    TestOutputECGFrequencyScan()
    TestSetDCOffset()
    TestSetDCOffsetVariable()
    TestECGPlayRaw()
    TestOutputPWTT60BPM()
    TestOutputPWTT60BPMSquare()
    TestOutputPPG60BPM()
    TestOutputPPG60BPMAcOffsetAdded()
    TestOutputPPG60BPMNoise()
    TestPPGPDSampling()
    TestPPGPlayRaw()
    TestOutputPPGFrequencyScan()
    completedEvent.set()


connectedCb = ConnectedCallback(DeviceConnectedHandler)
if device.WTQInit(connectedCb) == False:
    print('Error: connect failed')
    device.WTQFree()
    sys.exit()

completedEvent.wait()
print('all tests are done...')
device.WTQFree()
time.sleep(3)

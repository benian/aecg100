#pragma once

#define WHALETEQ_API extern "C"

// Defined in <limits.h>
//#define INT_MIN     (-2147483647 - 1) /* minimum (signed) int value */

/// \fn ConnectedCallback
/// \brief Called when the device is connected or disconnected
/// @param[in] connected    true if connected; otherwise, it's false
typedef void (*ConnectedCallback) (bool connected);

/// \fn OutputSignalCallback
/// \brief Called back with outputted data; if the outputting is stopped, the data sent by the last callback is the minimum value of INT
/// @param[in] ac         Unit: uV
/// @param[in] dc         Unit: uV
typedef void (*OutputSignalCallback) (double time, int ac, int dc);

/// \fn SamplingCallback
/// \brief Called back with sampling data; the PD sampling data is [0, 1023]
/// @param[in] data       PD sampling data
/// @param[in] number     the number of the sampling data with the value
typedef void (*SamplingCallback) (int data, int number);

/// \fn SamplingErrorCallback
/// \brief Called back with PD sampling error code
/// @param[in] error      Error code for PD sampling error
typedef void (*SamplingErrorCallback) (int error);

#define STATUS_OK                      0
#define STATUS_DEVICE_NOT_CONNECTED    1
#define STATUS_DEVICE_ERROR            2
#define STATUS_INVALID_PARAMETER       3
#define STATUS_INVALID_MODE_TYPE       4  // Mode-ECG, Mode-PWV, Mode-SPO2, Mode-PPG (1 LED), Mode-PPG (2 LED)

// Sampling Error Code
#define SAMPLING_STATUS_CHANNEL1_PD_PACKET_LOST      0x10    //!< the packet of channel-1 pd sampling is lost
#define SAMPLING_STATUS_CHANNEL1_SWITCH_PACKET_LOST  0x11    //!< the packet of channel-1 switch (trigger level) sampling is lost
#define SAMPLING_STATUS_CHANNEL2_PD_PACKET_LOST      0x12    //!< the packet of channel-2 pd sampling is lost
#define SAMPLING_STATUS_CHANNEL2_SWITCH_PACKET_LOST  0x13    //!< the packet of channel-2 switch (trigger level) sampling is lost

#define PPG_DC_MAX                     3000
#define PPG_DC_MIN                     100
#define PPG_AC_MAX                     30.0
#define PPG_AC_MIN                     0.75

// WAP1001      channel-1: G, channel-2: NA,  channel-3: NA
// WAP2001-2004 channel-1: R, channel-2: IR,  channel-3: NA
// WAP2005-2006 channel-1: R, channel-2: IR,  channel-3: G 
typedef enum {
    PPGChannel1 = 1,               //!< channel-1
    PPGChannel2 = 2,               //!< channel-2
	PPGChannel3 = 3                //!< channel-3
} PPGChannel;

typedef enum {
    StandAloneModeMain,
    StandAloneModeA,               //!< Mode-A
    StandAloneModeB,               //!< Mode-B
    StandAloneModeC                //!< Mode-C
} StandAloneMode;

typedef enum {
    ModeTypeECG = 1,               //!< ECG mode
    ModeTypePWV = 2,               //!< PWV mode (ECG+PPG)
    ModeTypeSPO2 = 3,              //!< SPO2 mode (two PPG channel)
    ModeTypePPG1 = 4,              //!< PPG Adv mode (only PPG channel-1)
    ModeTypePPG2 = 5,              //!< PPG Adv mode (two PPG channels)
    ModeTypePWV2 = 6,              //!< PWV mode (ECG + two PPG)
    ModeTypePWV3 = 7,              //!< PWV mode (ECG + three PPG)
    ModeTypeSPO23 = 8,             //!< SPO2 mode (three PPG channel)
    ModeTypePPG3 = 9,              //!< PPG Adv mode (three PPG channels)
    ModeTypeMax = 10
} ModeType;

typedef enum {
    ECGWaveformTypeSine,           //!< Sine
    ECGWaveformTypeTriangle,
    ECGWaveformTypeSquare,
    ECGWaveformTypeRectanglePulse, //!< Rectangle Pulse
    ECGWaveformTypeTrianglePulse,  //!< Triangle Pulse
    ECGWaveformTypeExponential,    //!< Exponential
    ECGWaveformTypeECG,
} ECGWaveformType;

/// Device output lead
typedef enum {
    ElectrodeRightArm,             //!< RA
    ElectrodeLeftArm=0xff          //!< LA
} Electrode;

typedef enum {
    ECGImpedanceOff,               //!< Disable impedance
    ECGImpedanceOn=0xff            //!< Enable 620K impedance
} ECGImpedance;

typedef enum {
    ECGPacingOff,
    ECGPacingOn=0xff
} ECGPacingEnable;

typedef enum {
    ECGRespirationOff,
    ECGRespirationOn=0xff
} ECGRespirationEnable;

typedef enum {
    ECGRespirationBaseline500  = 500,       //!< not supported now
    ECGRespirationBaseline1000 = 1000,
    ECGRespirationBaseline1500 = 1500,
    ECGRespirationBaseline2000 = 2000
} ECGRespirationBaseline;

typedef enum {
    ECGNoiseFrequencyOff,
    ECGNoiseFrequency50Hz,
    ECGNoiseFrequency60Hz,
	ECGNoiseFrequency100Hz,
	ECGNoiseFrequency120Hz
} ECGNoiseFrequency;

typedef enum {
    PPGWaveformTypeSine,
    PPGWaveformTypeTriangle,
    PPGWaveformTypeSquare,
    PPGWaveformTypePPG
} PPGWaveformType;

typedef enum {
    PPGNoiseFrequencyOff,
    PPGNoiseFrequency50Hz,
    PPGNoiseFrequency60Hz,
    PPGNoiseFrequency1KHz,
    PPGNoiseFrequency5KHz,
	PPGNoiseFrequency100Hz,
	PPGNoiseFrequency120Hz,
	PPGNoiseFrequencyWhiteNoise,
} PPGNoiseFrequency;

typedef enum {
    LEDModeOff,
    LEDModeOn
} LEDMode;

typedef enum {
    LEDTypeGreen,  //!< Green
    LEDTypeRed,    //!< Red
    LEDTypeIR,     //!< IR
    LEDTypeNone    //!< not existing
} LEDType;

typedef enum {
	LEDPulseNone = 0x00,
	LEDPulseGreen = 0x01,
	LEDPulseRed = 0x02,
	LEDPulseInfrared = 0x04
} LEDPulse;

typedef enum {
    SyncPulseLEDOff, //!< not supported now
    SyncPulseSync,
    SyncPulseSyncOff
} SyncPulse;

typedef enum {
    PPGInvertedOff,  //!< The outputting PPG waveform is not inverted 
    PPGInvertedOn    //!< The outputting PPG waveform is inverted
} PPGInverted;

typedef enum {
    PPGSamplingChannel1PD,  
    PPGSamplingChannel2PD,
    PPGSamplingChannel1Switch,
    PPGSamplingChannel2Switch,
    PPGSamplingMax
} PPGSampling;

typedef enum {
	PPGRespirationOff,
	PPGRespirationBaselineModulation,
	PPGRespirationAmplitudeModulation,
	PPGRespirationFrequencyModulation
} PPGRespiration;

typedef enum {
	LEDTriggerModeOne,
	LEDTriggerModeMulti
} LEDTriggerMode;


/// \anchor structHW_INFORMATION
/// \brief Define a structure of device hw and fw information
/// \details <B>FW version:</B> x.y (ex: version 1.2)\n
///          <B>HW version:</B> x (ex: version 9)
typedef struct {
    int         FWMainVersion;   //!< FW main version
    int         FWSubVersion;    //!< FW sub version
    int         HWVersion;       //!< HW version
	int			PCBVersion;      //!< PCB version
} HW_INFORMATION;

/// \anchor structMODEL_INFORMATION
/// \brief Define a structure of the device model; for C code, you can get the serial number by the format: 
///        ("W%c%c%02x%02x-%02d%04d", ProductName[0], ProductName[1], GenerationNumber, ModelNumber, Year, SerialNumber)
typedef struct {
    char            ProductName[2];
    char            GenerationNumber;
    char            ModelNumber;
    int             SerialNumber;       //!< device serial number
    int             Year;               //!< 0x11 = 2017
    int             LEDType1;           //!< enum ::LEDType of channel-1 
    int             LEDType2;           //!< enum ::LEDType of channel-2
    int             LEDType3;           //!< enum ::LEDType of channel-3
} MODEL_INFORMATION;

/// \anchor structECG_WAVEFORM
/// \brief  Define a structure of ECG waveform setting
typedef struct {
    int         WaveformType;                 //!< ::ECGWaveformType
    double      Frequency;                    //!< Unit: Hz
    double      Amplitude;                    //!< Unit: mV
    double      TWave;                        //!< Unit: mV
    double      PWave;                        //!< Unit: mV
    double      STSegment;                    //!< Unit: mV
    int         DCOffsetVariable;             //!< boolean value; the possible DCOffset value depends on this
    int         DCOffset;                     //!< If DCOffsetVariable is true, the range is -500~500; otherwise, the value is 300|0|-300.
    int         TimePeriod;                   //!< Unit: ms
    int         PRInterval;                   //!< Unit: ms
    int         QRSDuration;                  //!< Unit: ms
    int         TDuration;                    //!< Unit: ms
    int         QTInterval;                   //!< Unit: ms
    int         Impedance;                    //!< ::ECGImpedance
    int         Electrode;                    //!< ::Electrode
    int         PulseWidth;                   //!< Effective only when the WaveformType is ::ECGWaveformTypeRectanglePulse| ::ECGWaveformTypeTrianglePulse| ::ECGWaveformTypeExponential
    double      NoiseAmplitude;               //!< Unit: mV; The max noise amplitude is 2.00 mV
    int         NoiseFrequency;               //!< ::ECGNoiseFrequency
    int         PacingEnabled;                //!< boolean value; 0 if disable
    double      PacingAmplitude;              //!< Unit: mV; -1000mV ~ 1000mV
    double      PacingDuration;               //!< Unit: ms; 0ms ~ 2ms; resolution: 0.1ms
    int         PacingRate;                   //!< Unit: BPM
    int         RespirationEnabled;           //!< boolean value; 0 if disable
    int         RespirationAmplitude;         //!< Unit: milli-ohm; the supported range: 1000 ~ 5000 milli-ohm; resolution: 0.1 ohm
    int         RespirationRate;              //!< 4~200 BrPM
    int         RespirationRatio;             //!< The possible values are from 1 to 5. 1 means 1:1, 2 means 1:2. The default is 1 (1:1).
    int         RespirationBaseline;          //!< ::ECGRespirationBaseline. The default is 1000 ohm.
    int         RespirationApneaDuration;     //!< Unit: sec. The value is 0~60 sec.
    int         RespirationApneaCycle;        //!< Unit: sec. The value is 1~10 minute.
    char        Reserved[12];
} ECG_WAVEFORM;

/// \anchor structPPG_WAVEFORM
/// \brief Define a structure of PPG waveform setting
typedef struct {
    int                 WaveformType;                //!< ::PPGWaveformType
    double              Frequency;                   //!< Unit: Hz
    double              VolDC;                       //!< Unit: mV
    double              VolSP;                       //!< Unit: mV
    double              VolDN;                       //!< Unit: mV
    double              VolDP;                       //!< Unit: mV
    double              ACOffset;                    //!< Unit: mV; the sum of the VolSP(AC) and ACOffset must less than or equal to 30mV
    int                 TimeSP;                      //!< Unit: ms
    int                 TimeDN;                      //!< Unit: ms
    int                 TimeDP;                      //!< Unit: ms
    int                 TimePeriod;                  //!< Unit: ms
    int                 SyncPulse;                   //!< ::SyncPulse
    int                 Inverted;                    //!< ::PPGInverted
    double              NoiseAmplitude;              //!< Unit: mV. The max noise amplitude is 2.00 mV
    int                 NoiseFrequency;              //!< ::PPGNoiseFrequency
    int			        RespirationEnabled;          //!< ::PPGRespiration
    int                 RespirationRate;             //!< Unit: BrPM
    double              RespirationVariation;        //!< Unit: -16~16% percent
	int                 RespirationInExhaleRatio;    //!< inhale:exhale ratio; the supported value is 1~5 (1:1 ~ 1:5)
    char                Reserved[12];
} PPG_WAVEFORM;

typedef struct {
    double      Amplitude;        //!< Unit: mV
    double      FrequencyStart;   //!< Unit: Hz
    double      FrequencyFinish;  //!< Unit: Hz
    int         Duration;         //!< Unit: second
} FREQUENCY_SCAN;

typedef struct {
    double      Amplitude;        //!< Unit: mV
    double      DC;               //!< Unit: mV; ECG: -500mV ~ +500mV, PPG: 0mV ~ 3000mV
    int         SyncPulse;        //!< ::SyncPulse
    double      FrequencyStart;   //!< Unit: Hz
    double      FrequencyFinish;  //!< Unit: Hz
    int         Duration;         //!< Unit: second
} FREQUENCY_SCAN2;

typedef struct {
    double SampleRate;   //!< sampling frequency
    int Size;            //!< the number of points for AC and DC
    int SyncPulse;       //!< ::SyncPulse
    double *AC;          //!< the array of AC data
    double *DC;          //!< the array of DC data
    OutputSignalCallback cb;
} PLAY_RAW_DATA;

typedef struct {
	unsigned char		LEDPulse;				//!< ::LEDPulse
	unsigned char		Reserved;
	unsigned short      PulsePeriod;			//!< Unit: us; effective when trigger mode is PPGTriggerModeMulti
	unsigned short      PulseWidth;				//!< Unit: us; effective when trigger mode is PPGTriggerModeMulti
} PPG_LED_PULSE;

typedef struct {
	LEDTriggerMode		TriggerMode;			//!< ::LEDTriggerMode
	union {
		unsigned short	PulseGroupInterval;		//!< Unit: us; effective when trigger mode is PPGTriggerModeOne
		unsigned short	BurstPeriod;			//!< Unit: us; effective when trigger mode is PPGTriggerModeMulti
	};
	PPG_LED_PULSE		LEDPulse[8];
} PPG_LED_PULSE_GROUP_SETTING;


//
// Initialization & Cleanup
//

///
/// Initialization
///
/// During initialization, it will try to connect a device. If a device is found,
/// the cb function will be called. After then, if a device is disconnected,
/// the cb will be called again to notify the disconnection event. 
/// @param[in] cb  a callback function to notify the connection or disconnection event
///
WHALETEQ_API 
bool 
WTQInit (
    ConnectedCallback cb
);

///
/// Connect the device.
/// @param[in] portNumber            Device COM port number; -1 means the port number is automatically selected
/// @param[in] millisecondsTimeout   Connection timeout; the number of milliseconds to connect, or -1 to wait indefinitely
/// @return true if the device is connected; false if the time-out interval elapsed and 
///         the device is still not connected
///
WHALETEQ_API
bool
WTQConnect (
    unsigned int portNumber,
    unsigned int millisecondsTimeout
);

///
/// Disconnect the device and clean up library resource
///
WHALETEQ_API 
void 
WTQFree (
    void
);

//
// Device Configurations
//

///
/// Get device information (main module)
/// @param[out] modelInfo     A pointer to a ::MODEL_INFORMATION structure
///
WHALETEQ_API 
bool
WTQGetDeviceInformation (
    MODEL_INFORMATION *modelInfo
);

///
/// Get device serial number (main module)
///
/// @return a null-terminated string of serial number text; DO NOT free the returned string
///
WHALETEQ_API 
char*
WTQGetSerialNumber (
	void
);

///
/// Get device information (PPG module)
/// @param[out] modelInfo     A pointer to a ::MODEL_INFORMATION structure
///
WHALETEQ_API 
bool
WTQGetPPGDeviceInformation (
    MODEL_INFORMATION *modelInfo
);

///
/// Get device serial number (PPG module)
///
/// @return a null-terminated string of serial number text; DO NOT free the returned string
///
WHALETEQ_API 
char*
WTQGetPPGSerialNumber (
	void
);

///
/// Get device FW/HW information
/// @param[out] hwlInfo     A pointer to a ::HW_INFORMATION structure
///
WHALETEQ_API
bool
WTQGetHWInformation (
    HW_INFORMATION *hwInfo
);

WHALETEQ_API
bool
WTQGetPPGHWInformation (
	HW_INFORMATION *hwInfo
);

//
// PPG Module Sampling
//
///
/// Enable Sampling Mode
/// @param[in] mode  \ref PPGSampling
/// @param[in] cbSamplingData A callback function to pass the sampling data
/// 
WHALETEQ_API 
bool 
WTQEnableSampling (
    PPGSampling mode,
    SamplingCallback cbSamplingData
);

WHALETEQ_API 
bool
WTQStartSampling (
    SamplingErrorCallback cbError
);

///
/// Stop Sampling and reset all sampling mode
/// 
WHALETEQ_API 
void 
WTQDisableSampling (
    void
);

///
/// Enable RLD function; when the RLD measurement is finished, it's required to disable RLD 
///
/// @param[in] enable  true to enable RLD; otherwises, the RLD is disabled
///
WHALETEQ_API
bool
WTQEnableRLD (
    bool enable
);

///
/// Measure RLD N1/N2 voltage; it's required add delay (ex: 1 second) during the calls to WTQEnableRLD and the first WTQReadRLD
///
WHALETEQ_API
bool
WTQReadRLD (
    double *N1, 
    double *N2
);

//
// Signal Output Control
//

WHALETEQ_API
bool
WTQDeviceEnableImpedance (
    int impedance         //!< ::ECGImpedance
);

WHALETEQ_API
bool
WTQDeviceSetElectrode (
    int electrode         //!< ::Electrode
);

WHALETEQ_API
bool
WTQDeviceSetDCOffset (
    int dcOffset          //!< The DCOffset mode is fixed, not variable. The valid value is 300| 0| -300.
);

WHALETEQ_API
bool
WTQDeviceEnablePacing (
    int pacing            //!< ::ECGPacingEnable
);

WHALETEQ_API
bool
WTQDeviceEnableRespiration (
	int respiration       //!< ::ECGRespirationEnable
);

WHALETEQ_API
bool
WTQReadLEDPulseGroupSetting (
	PPG_LED_PULSE_GROUP_SETTING  *pulseGroupSetting
);

WHALETEQ_API
bool
WTQWriteLEDPulseGroupSetting (
	PPG_LED_PULSE_GROUP_SETTING  *pulseGroupSetting
);

///
/// Start outputting ECG
///
/// @param[in] waveform     ECG waveform setting.
/// @param[in] cb           A callback function to pass waveform point data.
///
WHALETEQ_API
bool 
WTQOutputECG (
    ECG_WAVEFORM *waveform, 
    OutputSignalCallback cb
);

///
/// Start outputting ECG and PPG
///
/// @param[in] timeDiffPTTPeak The time difference between the two peak points of ECG and PPG
/// @param[in] ecgWaveform     ECG waveform setting
/// @param[in] ppgWaveform     PPG waveform setting
/// @param[in] cbECG           A callback function to pass ECG waveform point data\n 
///                            <B>Note:</B> the point value unit is uV
/// @param[in] cbPPG           A callback function to pass PPG waveform point data\n
///                            <B>Note:</B> the point value unit is uV
///
WHALETEQ_API
bool 
WTQOutputECGAndPPG (
    int timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform, 
    PPG_WAVEFORM *ppgWaveform, 
    OutputSignalCallback cbECG, 
    OutputSignalCallback cbPPG
);

///
/// Start outputting ECG and two PPG
///
/// @param[in] timeDiffPTTPeak         The time difference between the two peak points of ECG and PPG
/// @param[in] ecgWaveform             ECG waveform setting
/// @param[in] ppgChannel1Waveform     PPG waveform setting
/// @param[in] ppgChannel2Waveform     PPG waveform setting
/// @param[in] cbECG                   A callback function to pass ECG waveform point data\n 
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel1           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel2           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
///
WHALETEQ_API
bool 
WTQOutputECGAndPPGEx (
    int timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform, 
    PPG_WAVEFORM *ppgChannel1Waveform,
    PPG_WAVEFORM *ppgChannel2Waveform,
    OutputSignalCallback cbECG, 
    OutputSignalCallback cbPPGChannel1,
    OutputSignalCallback cbPPGChannel2
);

///
/// Start outputting ECG and two PPG
///
/// @param[in] timeDiffPTTPeak         The time difference between the two peak points of ECG and PPG
/// @param[in] ecgWaveform             ECG waveform setting
/// @param[in] ppgChannel1Waveform     PPG waveform setting (R)
/// @param[in] ppgChannel2Waveform     PPG waveform setting (IR)
/// @param[in] ppgChannel3Waveform     PPG waveform setting (G)
/// @param[in] cbECG                   A callback function to pass ECG waveform point data\n 
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel1           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel2           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
/// @param[in] cbPPGChannel3           A callback function to pass PPG waveform point data\n
///                                    <B>Note:</B> the point value unit is uV
///
WHALETEQ_API
bool 
WTQOutputECGAndPPG3 (
	int timeDiffPTTPeak,
	ECG_WAVEFORM *ecgWaveform, 
	PPG_WAVEFORM *ppgChannel1Waveform,
	PPG_WAVEFORM *ppgChannel2Waveform,
	PPG_WAVEFORM *ppgChannel3Waveform,
	OutputSignalCallback cbECG, 
	OutputSignalCallback cbPPGChannel1,
	OutputSignalCallback cbPPGChannel2,
	OutputSignalCallback cbPPGChannel3
);

///
/// Start outputting PPG (only one channel)
///
/// @param[in] channelNo   enum ::PPGChannel. Specify which channel to output.
/// @param[in] waveform    PPG waveform setting.
/// @param[in] cb          A callback function to pass PPG waveform point data.\n
///                        <B>Note:</B> the point value unit is uV
///
WHALETEQ_API 
bool 
WTQOutputPPG (
    PPGChannel channelNo,
    PPG_WAVEFORM *waveform, 
    OutputSignalCallback cb
); 

///
/// Start outputting PPG (two channels)
///
/// @param[in] channel1Waveform    PPG waveform setting for channel-1.
/// @param[in] channel2Waveform    PPG waveform setting for channel-2.
/// @param[in] cbChannel1          A callback function to pass PPG waveform point data for channel-1.\n
/// @param[in] cbChannel2          A callback function to pass PPG waveform point data for channel-2.\n
///                                <B>Note:</B> the point value unit is uV
WHALETEQ_API
bool 
WTQOutputPPGEx (
    PPG_WAVEFORM *channel1Waveform, 
    PPG_WAVEFORM *channel2Waveform, 
    OutputSignalCallback cbChannel1, 
    OutputSignalCallback cbChannel2
);

///
/// Start outputting PPG (three channels)
///
/// @param[in] channel1Waveform    PPG waveform setting for channel-1.
/// @param[in] channel2Waveform    PPG waveform setting for channel-2.
/// @param[in] channel3Waveform    PPG waveform setting for channel-3.
/// @param[in] cbChannel1          A callback function to pass PPG waveform point data for channel-1.\n
/// @param[in] cbChannel2          A callback function to pass PPG waveform point data for channel-2.\n
/// @param[in] cbChannel3          A callback function to pass PPG waveform point data for channel-3.\n
///                                <B>Note:</B> the point value unit is uV
WHALETEQ_API
bool 
WTQOutputPPG3 (
	PPG_WAVEFORM *channel1Waveform, 
	PPG_WAVEFORM *channel2Waveform,
	PPG_WAVEFORM *channel3Waveform,
	OutputSignalCallback cbChannel1, 
	OutputSignalCallback cbChannel2,
	OutputSignalCallback cbChannel3
);

///
/// Frequency Scan; output sine waveform with varying frequency
/// 
/// @param[in]  scan        struct ::FREQUENCY_SCAN
/// @param[in]  cb          A callback function to pass waveform point data\n 
///                         <B>Note:</B> the point value unit is uV
WHALETEQ_API
bool 
WTQOutputFrequencyScan (
    FREQUENCY_SCAN *scan,
    OutputSignalCallback cb
);

///
/// Frequency Scan; output sine waveform with varying frequency
/// 
/// @param[in]  scan        struct ::FREQUENCY_SCAN2
/// @param[in]  channelNo   enum ::PPGChannel. Specify which channel to output
/// @param[in]  cb          A callback function to pass waveform point data\n 
///                         <B>Note:</B> the point value unit is uV
WHALETEQ_API
bool 
WTQOutputFrequencyScanPPG (
    PPGChannel channelNo,
    FREQUENCY_SCAN2 *scan,
    OutputSignalCallback cb
);

//
// Play Raw Data
//

///
/// Play Raw Data to ECG channel
/// @param[in]  data           enum ::PLAY_RAW_DATA. ECG raw data
///
WHALETEQ_API
bool
WTQWaveformPlayerOutputECG (
    PLAY_RAW_DATA *data
);

/// 
/// Play Raw Data to ECG and PPG one channel
/// @param[in]  ecgData        enum ::PLAY_RAW_DATA. ECG raw data
/// @param[in]  channelNo      enum ::PPGChannel. Specify which channel to output
/// @param[in]  ppgData        enum ::PLAY_RAW_DATA. PPG raw data
///
WHALETEQ_API
bool
WTQWaveformPlayerOutputECGAndPPG (
    PLAY_RAW_DATA *ecgData,
    PPGChannel channelNo, 
    PLAY_RAW_DATA *ppgData
);

/// 
/// Play Raw Data to ECG and PPG two channels
/// @param[in]  ecgData          enum ::PLAY_RAW_DATA. ECG raw data
/// @param[in]  ppgChannel1Data  enum ::PLAY_RAW_DATA. PPG channel-1 raw data
/// @param[in]  ppgChannel2Data  enum ::PLAY_RAW_DATA. PPG channel-2 raw data
///
WHALETEQ_API
bool
WTQWaveformPlayerOutputECGAndPPGEx (
    PLAY_RAW_DATA *ecgData,
    PLAY_RAW_DATA *ppgChannel1Data,
    PLAY_RAW_DATA *ppgChannel2Data
);

/// 
/// Play Raw Data to ECG and PPG three channels
/// @param[in]  ecgData          enum ::PLAY_RAW_DATA. ECG raw data
/// @param[in]  ppgChannel1Data  enum ::PLAY_RAW_DATA. PPG channel-1 raw data (R)
/// @param[in]  ppgChannel2Data  enum ::PLAY_RAW_DATA. PPG channel-2 raw data (IR)
/// @param[in]  ppgChannel3Data  enum ::PLAY_RAW_DATA. PPG channel-3 raw data (G)
///
WHALETEQ_API
bool
WTQWaveformPlayerOutputECGAndPPG3 (
	PLAY_RAW_DATA *ecgData,
	PLAY_RAW_DATA *ppgChannel1Data,
	PLAY_RAW_DATA *ppgChannel2Data,
	PLAY_RAW_DATA *ppgChannel3Data
);

///
/// Play Raw Data to PPG one channel
/// @param[in]  channelNo      enum ::PPGChannel. Specify which channel to output
/// @param[in]  ppgData        enum ::PLAY_RAW_DATA. PPG raw data
///
WHALETEQ_API
bool
WTQWaveformPlayerOutputPPG (
    PPGChannel channelNo,
    PLAY_RAW_DATA *ppgData
);

/// 
/// Play Raw Data to PPG two channels
/// @param[in]  ppgChannel1Data  enum ::PLAY_RAW_DATA. PPG channel-1 raw data
/// @param[in]  ppgChannel2Data  enum ::PLAY_RAW_DATA. PPG channel-2 raw data
///
WHALETEQ_API
bool
WTQWaveformPlayerOutputPPGEx (
    PLAY_RAW_DATA *ppgChannel1Data,
    PLAY_RAW_DATA *ppgChannel2Data
);

/// 
/// Play Raw Data to PPG three channels
/// @param[in]  ppgChannel1Data  enum ::PLAY_RAW_DATA. PPG channel-1 raw data (R)
/// @param[in]  ppgChannel2Data  enum ::PLAY_RAW_DATA. PPG channel-2 raw data (IR)
/// @param[in]  ppgChannel3Data  enum ::PLAY_RAW_DATA. PPG channel-3 raw data (G)
///
WHALETEQ_API
bool
WTQWaveformPlayerOutputPPG3 (
	PLAY_RAW_DATA *ppgChannel1Data,
	PLAY_RAW_DATA *ppgChannel2Data,
	PLAY_RAW_DATA *ppgChannel3Data
);

WHALETEQ_API
void
WTQWaveformPlayerLoop (
    bool loop
);

///
/// Stop the device outputting waveform
///
WHALETEQ_API 
void 
WTQStopOutputWaveform (
    void
);

///
/// Stop playing raw data
///
WHALETEQ_API 
void 
WTQStopPlayRawData (
    void
);

//
// Standalone Mode Setting Control
//

///
/// Read/Write waveform from/to device
/// @param[in] mode             enum ::StandAloneMode. Specify which mode to read from.      
/// @returns enum ::ModeType
/// 
WHALETEQ_API
int
WTQReadStandaloneModeType (
    int mode
);

///
/// Read ECG waveform from device
/// @param[in]  mode            enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] waveform        ECG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQReadECGModeFromStandaloneMode (
    int mode,
    ECG_WAVEFORM *waveform
);

///
/// Write ECG waveform to device
/// @param[in]  mode            enum ::StandAloneMode. Specify which mode to write to.
/// @param[out] waveform        ECG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQWriteECGModeToStandaloneMode (
    int mode,
    ECG_WAVEFORM *waveform
);

///
/// Read ECG and PPG waveform from device
/// @param[in]  mode            enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] timeDiffPTTPeak time difference between ECG waveform peak and PPG waveform peak
/// @param[out] ecgWaveform     ECG waveform setting.
/// @param[out] ppgWaveform     PPG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQReadPWVModeFromStandaloneMode (
    int mode,
    int *timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,  
    PPG_WAVEFORM *ppgWaveform
);

///
/// Write ECG and PPG waveform to device
/// @param[in]  mode            enum ::StandAloneMode. Specify which mode to write to.
/// @param[out] timeDiffPTTPeak time difference between ECG waveform peak and PPG waveform peak
/// @param[out] ecgWaveform     ECG waveform setting.
/// @param[out] ppgWaveform     PPG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQWritePWVModeToStandaloneMode (
    int mode,
    int timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,  
    PPG_WAVEFORM *ppgWaveform
);

///
/// Read ECG and PPG waveform from device
/// @param[in]  mode                    enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] timeDiffPTTPeak         time difference between ECG waveform peak and PPG waveform peak
/// @param[out] ecgWaveform             ECG waveform setting.
/// @param[out] ppgChannel1Waveform     PPG waveform setting.
/// @param[out] ppgChannel2Waveform     PPG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQReadPWVModeExFromStandaloneMode (
    int mode,
    int *timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,  
    PPG_WAVEFORM *ppgChannel1Waveform,
    PPG_WAVEFORM *ppgChannel2Waveform
);

///
/// Write ECG and two PPG waveform to device
/// @param[in]  mode                    enum ::StandAloneMode. Specify which mode to write to.
/// @param[out] timeDiffPTTPeak         time difference between ECG waveform peak and PPG waveform peak
/// @param[out] ecgWaveform             ECG waveform setting.
/// @param[out] ppgChannel1Waveform     PPG waveform setting.
/// @param[out] ppgChannel2Waveform     PPG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQWritePWVModeExToStandaloneMode (
    int mode,
    int timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,  
    PPG_WAVEFORM *ppgChannel1Waveform,
    PPG_WAVEFORM *ppgChannel2Waveform
);

///
/// Read ECG and PPG waveform from device (only supported in one LED-RED mode)
/// @param[in]  mode                    enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] timeDiffPTTPeak         time difference between ECG waveform peak and PPG waveform peak
/// @param[out] ecgWaveform             ECG waveform setting
/// @param[out] ppgChannel1Waveform     PPG waveform setting
/// @param[out] ppgChannel2Waveform     PPG waveform setting
/// @param[out] ppgChannel3Waveform     PPG waveform setting
/// @returns status code
///
WHALETEQ_API
int
WTQReadPWVModePPG3FromStandaloneMode (
    int mode,
    int *timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,  
    PPG_WAVEFORM *ppgChannel1Waveform,
    PPG_WAVEFORM *ppgChannel2Waveform,
    PPG_WAVEFORM *ppgChannel3Waveform
);

///
/// Write ECG and two PPG waveform to device (only supported in one LED-RED mode)
/// @param[in]  mode                    enum ::StandAloneMode. Specify which mode to write to.
/// @param[out] timeDiffPTTPeak         time difference between ECG waveform peak and PPG waveform peak
/// @param[out] ecgWaveform             ECG waveform setting
/// @param[out] ppgChannel1Waveform     PPG waveform setting
/// @param[out] ppgChannel2Waveform     PPG waveform setting
/// @param[out] ppgChannel3Waveform     PPG waveform setting
/// @returns status code
///
WHALETEQ_API
int
WTQWritePWVModePPG3ToStandaloneMode (
    int mode,
    int timeDiffPTTPeak,
    ECG_WAVEFORM *ecgWaveform,  
    PPG_WAVEFORM *ppgChannel1Waveform,
    PPG_WAVEFORM *ppgChannel2Waveform,
    PPG_WAVEFORM *ppgChannel3Waveform
);

///
/// Read SPO2 waveform from device
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] channel1Waveform     PPG waveform setting for channel-1.
/// @param[out] channel2Waveform     PPG waveform setting for channel-2.
/// @returns status code
///
WHALETEQ_API
int
WTQReadSPO2ModeFromStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform
);

///
/// Write SPO2 waveform to device
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to write to.
/// @param[in]  channel1Waveform     PPG waveform setting for channel-1.
/// @param[in]  channel2Waveform     PPG waveform setting for channel-2.
/// @returns status code
///
WHALETEQ_API
int
WTQWriteSPO2ModeToStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform
);

///
/// Read SPO2 waveform from device (only supported in one LED-RED mode)
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] channel1Waveform     PPG waveform setting for channel-1 (R)
/// @param[out] channel2Waveform     PPG waveform setting for channel-2 (IR)
/// @param[out] channel3Waveform     PPG waveform setting for channel-3 (G)
/// @returns status code
///
WHALETEQ_API
int
WTQReadSPO2ModePPG3FromStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform,
    PPG_WAVEFORM *channel3Waveform
);

///
/// Write SPO2 waveform to device (only supported in one LED-RED mode)
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to write to.
/// @param[out] channel1Waveform     PPG waveform setting for channel-1 (R)
/// @param[out] channel2Waveform     PPG waveform setting for channel-2 (IR)
/// @param[out] channel3Waveform     PPG waveform setting for channel-3 (G)
/// @returns status code
///
WHALETEQ_API
int
WTQWriteSPO2ModePPG3ToStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform,
    PPG_WAVEFORM *channel3Waveform
);

///
/// Read PPG waveform from device (only one LED)
/// @param[in]  mode                enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] ppgWaveform         PPG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQReadPPGModeFromStandaloneMode (
    int mode,
    PPG_WAVEFORM *ppgWaveform
);

///
/// Write PPG waveform to device (only one LED)
/// @param[in]  mode                enum ::StandAloneMode. Specify which mode to write to.
/// @param[in]  ppgWaveform         PPG waveform setting.
/// @returns status code
///
WHALETEQ_API
int
WTQWritePPGModeToStandaloneMode (
    int mode,
    PPG_WAVEFORM *ppgWaveform
);

///
/// Read PPG waveform from device (two LED)
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] channel1Waveform     PPG waveform setting for channel-1.
/// @param[out] channel2Waveform     PPG waveform setting for channel-2.
/// @returns status code
///
WHALETEQ_API
int
WTQReadPPGModeExFromStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform
);

///
/// Write PPG waveform to device (two LED)
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to read from.
/// @param[in]  channel1Waveform     PPG waveform setting for channel-1.
/// @param[in]  channel2Waveform     PPG waveform setting for channel-2.
/// @returns status code
///
WHALETEQ_API
int
WTQWritePPGModeExToStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform
);

///
/// Read PPG waveform from device (only supported in one LED-RED mode)
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] channel1Waveform     PPG waveform setting for channel-1 (R)
/// @param[out] channel2Waveform     PPG waveform setting for channel-2 (IR)
/// @param[out] channel3Waveform     PPG waveform setting for channel-3 (G)
/// @returns status code
///
WHALETEQ_API
int
WTQReadPPGModePPG3FromStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform,
    PPG_WAVEFORM *channel3Waveform
);

///
/// Write PPG waveform to device (only supported in one LED-RED mode)
/// @param[in]  mode                 enum ::StandAloneMode. Specify which mode to read from.
/// @param[out] channel1Waveform     PPG waveform setting for channel-1 (R)
/// @param[out] channel2Waveform     PPG waveform setting for channel-2 (IR)
/// @param[out] channel3Waveform     PPG waveform setting for channel-3 (G)
/// @returns status code
///
WHALETEQ_API
int
WTQWritePPGModePPG3ToStandaloneMode (
    int mode,
    PPG_WAVEFORM *channel1Waveform,
    PPG_WAVEFORM *channel2Waveform,
    PPG_WAVEFORM *channel3Waveform
);

///
/// Restore the LED level and Trigger level of PPG module to the factory settings
///
WHALETEQ_API
bool
WTQRestoreFactorySetting (
	void
);

///
/// Read PPG LED Level data
/// @param[in]  channelNo       enum ::PPGChannel. Specify which channel to read.
/// @param[out] level           PPG LED Level data. The range is [0, 255]
///
WHALETEQ_API
bool
WTQReadPPGLedCalibrationSetting (
	PPGChannel channelNo,
	unsigned char *level
);

///
/// Write PPG LED Level data
/// @param[in]  channelNo       enum ::PPGChannel. Specify which channel to write.
/// @param[in]  level           PPG LED Level data. The range is [0, 255]
///
WHALETEQ_API
bool
WTQWritePPGLedCalibrationSetting (
	PPGChannel channelNo,
	unsigned char level
);

///
/// Read PPG Trigger Level data
/// @param[in]  channelNo       enum ::PPGChannel. Specify which channel to read.
/// @param[out] level           PPG Trigger Level data. The range is [0, 255]
///
WHALETEQ_API
bool
WTQReadPPGTriggerLevelCalibrationSetting (
    PPGChannel channelNo,
    unsigned char *level
);

///
/// Write PPG Trigger Level data
/// @param[in]  channelNo       enum ::PPGChannel. Specify which channel to write.
/// @param[in]  level           PPG Trigger Level data. The range is [0, 255]
///
WHALETEQ_API
bool
WTQWritePPGTriggerLevelCalibrationSetting (
    PPGChannel channelNo,
    unsigned char level
);

//
// DLL Version
//
/// Get DLL file version
/// \return The version is 4-digits and are saved in each byte of unsigned int value.\n
///         For example, if the return value is 0x01020304, the dll version is 1.2.3.4.
WHALETEQ_API
unsigned int
WTQGetVersion (
    void
);


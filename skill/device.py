from logging import Logger
from typing import Optional, Union, TypedDict, NoReturn, List

from miio import DreameVacuum, RoborockVacuum, G1Vacuum, ViomiVacuum
from miio.integrations.vacuum.dreame import dreamevacuum_miot
from miio.integrations.vacuum.roborock.vacuum import SUPPORTED_MODELS as ROBOROCK_MODELS
from miio.integrations.vacuum.mijia.g1vacuum import SUPPORTED_MODELS as MIJIA_MODELS
from miio.integrations.vacuum.viomi.viomivacuum import SUPPORTED_MODELS as VIOMI_MODELS

try:
    from skill.connection import MiCloudConnection, TDeviceConfig
    from skill.utility import read_config
except ModuleNotFoundError:
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from connection import MiCloudConnection, TDeviceConfig
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from utility import read_config


TDevices = Union[
    DreameVacuum,
    RoborockVacuum,
    G1Vacuum,
    ViomiVacuum
]


class TLocalDeviceConfig(TypedDict):
    device_name: str


class TModelMapping(TypedDict):
    handler: TDevices
    models: List[str]


def mi_local_device(func):
    def wrapper(self):
        if not self.device:
            raise DeviceNotFound
        func(self)
    return wrapper


class DeviceNotFound(Exception):

    def __init__(self):
        message = 'Device not found.'
        super().__init__(message)


MODEL_MAPPINGS: List[TModelMapping] = [
    {
        'handler': DreameVacuum,
        'models': [
            dreamevacuum_miot.DREAME_1C,
            dreamevacuum_miot.DREAME_F9,
            dreamevacuum_miot.DREAME_D9,
            dreamevacuum_miot.DREAME_Z10_PRO,
            dreamevacuum_miot.DREAME_MOP_2_PRO_PLUS,
            dreamevacuum_miot.DREAME_MOP_2_ULTRA,
            dreamevacuum_miot.DREAME_MOP_2
        ]
    }, {
        'handler': RoborockVacuum,
        'models': ROBOROCK_MODELS
    }, {
        'handler': G1Vacuum,
        'models': MIJIA_MODELS
    }, {
        'handler': ViomiVacuum,
        'models': VIOMI_MODELS
    }
]


class MiDevice:

    logger: Logger
    config: TLocalDeviceConfig
    mcc: MiCloudConnection
    device: TDevices

    def __init__(self) -> NoReturn:
        self.logger = Logger(name='alexa-miio-device')
        self.config = read_config(section='MiDevice')

        self.mcc = MiCloudConnection()
        self.mcc.connect()

        self.device = self.get_device()

    def get_device(self) -> Optional[TDevices]:
        device_config = self._get_device_config()
        if not device_config:
            self.logger.error('Device config could not be found.')
            return None

        model = device_config['model']
        handler = self._get_device_handler(model)
        if not handler:
            self.logger.error('Model not supported')
            return None

        return handler(
            model=model,
            token=device_config['token'],
            ip=device_config['localip']
        )

    def _get_device_config(self) -> Optional[TDeviceConfig]:
        for device_config in self.mcc.device_configs:
            if not device_config['name'] == self.config['device_name']:
                continue
            return device_config

        return None

    @staticmethod
    def _get_device_handler(model: str) -> Optional[TDevices]:
        for mapping in MODEL_MAPPINGS:
            if model in mapping['models']:
                return mapping['handler']
        return None


class MiDeviceActions(MiDevice):

    def __init__(self) -> NoReturn:
        super().__init__()

    @mi_local_device
    def start_cleaning(self) -> NoReturn:
        self.device.start()

    @mi_local_device
    def stop_cleaning(self) -> NoReturn:
        self.device.stop()

    @mi_local_device
    def return_to_home(self) -> NoReturn:
        self.device.home()

    @mi_local_device
    def locate_device(self) -> NoReturn:
        self.device.identify()

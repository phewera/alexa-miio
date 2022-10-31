from logging import Logger
from typing import Optional, TypedDict, NoReturn, Union

from miio.integrations.vacuum.dreame import dreamevacuum_miot
from miio.integrations.vacuum.mijia.g1vacuum import SUPPORTED_MODELS as MIJIA_MODELS
from miio.integrations.vacuum.roborock.vacuum import SUPPORTED_MODELS as ROBOROCK_MODELS
from miio.integrations.vacuum.viomi.viomivacuum import SUPPORTED_MODELS as VIOMI_MODELS

try:
    from skill.connection import MiCloudConnection, TDeviceConfig
    from skill.utility import read_config
    from skill.actions import DreameDeviceActions, RoborockDeviceActions, MijiaDeviceActions, ViomiDeviceActions
except ModuleNotFoundError:
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from connection import MiCloudConnection, TDeviceConfig
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from utility import read_config
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from actions import DreameDeviceActions, RoborockDeviceActions, MijiaDeviceActions, ViomiDeviceActions


DREAME_MODELS = [
    dreamevacuum_miot.DREAME_1C,
    dreamevacuum_miot.DREAME_F9,
    dreamevacuum_miot.DREAME_D9,
    dreamevacuum_miot.DREAME_Z10_PRO,
    dreamevacuum_miot.DREAME_MOP_2_PRO_PLUS,
    dreamevacuum_miot.DREAME_MOP_2_ULTRA,
    dreamevacuum_miot.DREAME_MOP_2
]

TDevices = Union[
    DreameDeviceActions,
    RoborockDeviceActions,
    MijiaDeviceActions,
    ViomiDeviceActions
]


class TLocalDeviceConfig(TypedDict):
    device_name: str


def mi_device_action(func):
    def wrapper(self):
        if not self.device:
            raise DeviceNotFound
        try:
            func(self)
        except AttributeError:
            raise DeviceActionNotSupported
    return wrapper


class DeviceNotFound(Exception):

    def __init__(self):
        message = 'Device not found.'
        super().__init__(message)


class DeviceActionNotSupported(Exception):

    def __init__(self):
        message = 'Action not supported by device.'
        super().__init__(message)


class MiDevice:
    """ Main device class with control functions """

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
        """ Get the actual device by model name """
        device_config = self._get_device_config()
        if not device_config:
            self.logger.error('Device config could not be found.')
            return None

        model = device_config['model']
        token = device_config['token']
        localip = device_config['localip']

        if model in DREAME_MODELS:
            return DreameDeviceActions(
                model=model,
                token=token,
                ip=localip
            )

        elif model in ROBOROCK_MODELS:
            return RoborockDeviceActions(
                model=model,
                token=token,
                ip=localip
            )

        elif model in MIJIA_MODELS:
            return MijiaDeviceActions(
                model=model,
                token=token,
                ip=localip
            )

        elif model in VIOMI_MODELS:
            return ViomiDeviceActions(
                model=model,
                token=token,
                ip=localip
            )

        self.logger.error(f'Model "{model}" not supported."')
        return None

    def _get_device_config(self) -> Optional[TDeviceConfig]:
        """ Get device config by the configured device name """
        for device_config in self.mcc.device_configs:
            if not device_config['name'] == self.config['device_name']:
                continue
            return device_config
        return None

    @mi_device_action
    def start_cleaning(self) -> NoReturn:
        self.device.start_cleaning()

    @mi_device_action
    def stop_cleaning(self) -> NoReturn:
        self.device.stop_cleaning()

    @mi_device_action
    def return_to_home(self) -> NoReturn:
        self.device.return_to_home()

    @mi_device_action
    def locate_device(self) -> NoReturn:
        self.device.locate_device()

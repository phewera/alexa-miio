from logging import Logger
from typing import TypedDict, List, NoReturn

from micloud import MiCloud
from micloud.micloudexception import MiCloudException

try:
    from skill.utility import read_config
except ModuleNotFoundError:
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from utility import read_config


class TMiCloudConfig(TypedDict):
    username: str
    password: str
    country: str


class TDeviceConfigExtra(TypedDict):
    isSetPincode: int
    pincodeType: int
    fw_version: str
    needVerfiyCode: int
    isPasswordEncrypt: int


class TDeviceConfig(TypedDict):
    did: str
    token: str
    longitude: str
    latitude: str
    name: str
    pid: str
    localip: str
    mac: str
    ssid: str
    bssid: str
    parent_id: str
    parent_model: str
    show_mode: int
    model: str
    adminFlag: int
    shareFlag: int
    permitLevel: int
    isOnline: bool
    desc: str
    extra: TDeviceConfigExtra
    uid: int
    pd_id: int
    password: str
    p2p_id: str
    rssi: int
    family_id: int
    reset_flag: int


def mi_cloud_connection(func):
    def wrapper(self):
        if not self.connection:
            raise MiCloudConnectionNotAvailable
        return func(self)
    return wrapper


class MiCloudConnectionNotAvailable(Exception):

    def __init__(self):
        message = 'MiCloud connection not available.'
        super().__init__(message)


class MiCloudConnection:

    logger: Logger
    config: TMiCloudConfig = None
    connection: MiCloud = None

    def __init__(self) -> NoReturn:
        self.logger = Logger(name='alexa-miio-connection')
        self.config = read_config(section='MiCloud')

    def connect(self) -> NoReturn:
        try:
            mc = MiCloud(
                username=self.config.get('username'),
                password=self.config.get('password')
            )
            mc.login()
            self.connection = mc

        except MiCloudException as e:
            self.logger.error(f'Connect: {e}')

    @property
    @mi_cloud_connection
    def device_configs(self) -> List[TDeviceConfig]:
        country = self.config.get('country', None)
        return self.connection.get_devices(country)

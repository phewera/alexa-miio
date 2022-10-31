from typing import NoReturn

from miio import DreameVacuum, RoborockVacuum, G1Vacuum, ViomiVacuum


class DreameDeviceActions(DreameVacuum):
    """ Mapping of individually DreameVaccum actions to MiDevice actions """

    def __init__(self, model, token, ip):
        super().__init__(
            model=model,
            token=token,
            ip=ip
        )

    def start_cleaning(self) -> NoReturn:
        self.start()

    def stop_cleaning(self) -> NoReturn:
        self.stop()

    def return_to_home(self) -> NoReturn:
        self.home()

    def locate_device(self) -> NoReturn:
        self.identify()


class RoborockDeviceActions(RoborockVacuum):
    """ Mapping of individually RoborockVacuum actions to MiDevice actions """

    def __init__(self, model, token, ip):
        super().__init__(
            model=model,
            token=token,
            ip=ip
        )

    def start_cleaning(self) -> NoReturn:
        self.start()

    def stop_cleaning(self) -> NoReturn:
        self.stop()

    def return_to_home(self) -> NoReturn:
        self.home()

    def locate_device(self) -> NoReturn:
        self.find()


class MijiaDeviceActions(G1Vacuum):
    """ Mapping of individually G1Vacuum actions to MiDevice actions """

    def __init__(self, model, token, ip):
        super().__init__(
            model=model,
            token=token,
            ip=ip
        )

    def start_cleaning(self) -> NoReturn:
        self.start()

    def stop_cleaning(self) -> NoReturn:
        self.stop()

    def return_to_home(self) -> NoReturn:
        self.home()

    def locate_device(self) -> NoReturn:
        self.find()


class ViomiDeviceActions(ViomiVacuum):
    """ Mapping of individually ViomiVacuum actions to MiDevice actions """

    def __init__(self, model, token, ip):
        super().__init__(
            model=model,
            token=token,
            ip=ip
        )

    def start_cleaning(self) -> NoReturn:
        self.start()

    def stop_cleaning(self) -> NoReturn:
        self.stop()

    def return_to_home(self) -> NoReturn:
        self.home()

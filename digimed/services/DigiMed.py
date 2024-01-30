import pathlib
import os
from digitalpy.core.main.DigitalPy import DigitalPy
from digitalpy.core.component_management.impl.component_registration_handler import ComponentRegistrationHandler

class DigiMed(DigitalPy):
    """ this is the main class for the digimed application
    """
    def __init__(self):
        super().__init__()
        self.configuration.add_configuration("digimed/configuration/digimed_configuration.ini")

    def start_services(self):
        super().start_services()
        self.start_service("digimed.api")

    def register_components(self):
        super().register_components()

        # register digimed core components
        digipy_core_components = ComponentRegistrationHandler.discover_components(
            component_folder_path=pathlib.PurePath(
                str(
                    pathlib.PurePath(
                        os.path.abspath(__file__)
                    ).parent.parent
                    /
                    "core"
                ),
            )
        )

        for digipy_core_component in digipy_core_components:
            ComponentRegistrationHandler.register_component(
                digipy_core_component,  # type: ignore
                "digimed.core",
                self.configuration,  # type: ignore
            )

if __name__ == '__main__':
    dm = DigiMed()
    dm.start()
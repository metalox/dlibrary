from abc import ABCMeta
import os
from dlibrary.dialog_predefined import AlertType, Alert
from dlibrary.utility import AbstractXmlFile, SingletonMeta, VSException
import vs


class Platform(object):
    MAC_OS = 1
    WINDOWS = 2


class Vectorworks(object, metaclass=SingletonMeta):

    @property
    def version(self) -> str:
        major, _, _, _, _ = vs.GetVersionEx()
        return str(major + 1995 if major > 12 else major)

    @property
    def platform(self) -> int:
        _, _, _, platform, _ = vs.GetVersionEx()
        return platform

    @property
    def dongle(self) -> str:
        return vs.GetActiveSerialNumber()[-6:]

    def get_folder_path_of_plugin_file(self, filename: str) -> str:
        _, file_path = vs.FindFileInPluginFolder(filename)
        return self.__get_os_independent_file_path(file_path)

    def get_folder_path_of_active_document(self) -> str:
        return self.get_file_path_of_active_document()[:-len(vs.GetFName())]

    def get_file_path_of_active_document(self) -> str:
        return self.__get_os_independent_file_path(vs.GetFPathName())

    def __get_os_independent_file_path(self, file_path: str) -> str:
        """
        Patrick Stanford <patstanford@coviana.com> on the VectorScript Discussion List:
        Since Mac OS 10, as they're rewritten it using UNIX kernel, the mac uses Posix natively.
        Since VW predates that, the old calls use HFS paths and need to be converted for newer APIs.
        You can ask VW to do the conversion, as simply replacing the characters are not enough (Posix uses volume
        mounting instead of drive names). This can be done through vs.ConvertHSF2PosixPath().
        """
        if self.platform == Platform.MAC_OS:
            _, file_path = vs.ConvertHSF2PosixPath(file_path)
        return file_path


class ActivePlugInType(object):
    MENU = '.vsm'
    TOOL = '.vst'
    OBJECT = '.vso'


class ActivePlugIn(object, metaclass=SingletonMeta):

    def __init__(self):
        self.__name = None
        self.__version = ''

    @property
    def name(self) -> str:
        # Singletons will keep it's data throughout the entire Vectorworks session!
        # This result isn't the same during that session, it depends on the active plugin!
        succeeded, self.__name, _ = vs.GetPluginInfo()
        if not succeeded:
            raise VSException('GetPluginInfo')
        return self.__name

    @property
    def version(self) -> str:
        return self.__version

    @version.setter
    def version(self, value: str):
        self.__version = value


class ActivePlugInInfo(object):
    """
    Decorator to initialize the active plugin. This should be used on the main run method of the plugin!
    """

    def __init__(self, version: str):
        self.__version = version

    def __call__(self, function: callable) -> callable:
        def initialize_active_plugin_function(*args, **kwargs):
            ActivePlugIn().version = self.__version
            function(*args, **kwargs)
        return initialize_active_plugin_function


class AbstractActivePlugInPrefsXmlFile(AbstractXmlFile, metaclass=ABCMeta):

    def __init__(self, active_plugin_type: str):
        """
        :type active_plugin_type: ActivePlugInType(Enum)
        """
        file_path = Vectorworks().get_folder_path_of_plugin_file(ActivePlugIn().name + active_plugin_type)
        super().__init__(os.path.join(file_path, ActivePlugIn().name + 'Prefs.xml'))


class AbstractActivePlugInDrawingXmlFile(AbstractXmlFile, metaclass=ABCMeta):

    def __init__(self):
        super().__init__(os.path.join(Vectorworks().get_folder_path_of_active_document(), ActivePlugIn().name + '.xml'))


class Security(object):
    """
    Decorator to secure a function based on the dongle and VW version running.
    """

    @staticmethod
    def __create_no_license_alert():
        return Alert(AlertType.WARNING,
                     'You have no rights to use this plugin.',
                     'Contact the plugin distributor to acquire a license.')

    @staticmethod
    def __create_other_license_alert(version: str):
        return Alert(AlertType.WARNING,
                     'Your license is for Vectorworks %s' % version,
                     'Contact the plugin distributor to update your license.')

    def __init__(self, version: str, dongles: set):
        self.__version = version
        self.__dongles = dongles
        self.__no_license_alert = self.__create_no_license_alert()
        self.__other_license_alert = self.__create_other_license_alert(version)

    def __call__(self, function: callable) -> callable:
        def secured_function(*args, **kwargs):
            if Vectorworks().dongle not in self.__dongles:
                self.__no_license_alert.show()
            elif Vectorworks().version != self.__version:
                self.__other_license_alert.show()
            else:
                function(*args, **kwargs)
        return secured_function

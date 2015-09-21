import vs


class AlertType(object):
    CRITICAL = 0
    WARNING = 1
    INFO = 2
    SUCCESS = 3


class Alert(object):

    def __init__(self, alert_type: int, text: str, advice: str=''):
        self.__type = alert_type
        self.__text = text
        self.__advice = advice

    def show(self):
        if self.__type == AlertType.CRITICAL:
            vs.AlertCritical(self.__text, self.__advice)
        elif self.__type == AlertType.WARNING:
            vs.AlertInform(self.__text, self.__advice, False)
        elif self.__type == AlertType.INFO:
            vs.AlertInform(self.__text, self.__advice, True)
        elif self.__type == AlertType.SUCCESS:
            vs.AlrtDialog(self.__text)


class PlugInFileVsExceptionAlert(Alert):

    def __init__(self, plugin_name: str):
        super().__init__(AlertType.CRITICAL,
                         'Something went wrong with the %s plug-in. It may be corrupt.' % plugin_name,
                         'Please contact the distributor.')


class PlugInFileFileNotFoundErrorAlert(Alert):

    def __init__(self, filename: str):
        super().__init__(AlertType.CRITICAL,
                         'The plug-in file `%s` could not be found.' % filename,
                         'Make sure the plug-in file is in the plug-in folder.')


class PlugInFilePermissionErrorAlert(Alert):

    def __init__(self, filename: str):
        super().__init__(AlertType.CRITICAL,
                         'The plug-in file `%s` could not be read.' % filename,
                         'Make sure the plug-in file has read/write permissions.')


class PlugInFileOsErrorAlert(Alert):

    def __init__(self, filename: str):
        super().__init__(AlertType.CRITICAL,
                         'Something went wrong while loading the plug-in file `%s`.' % filename,
                         'Make sure the plug-in file is in the plug-in folder, '
                         'have read/write permissions and is not corrupt.')

from dlibrary.dialog.control import AbstractControl, AbstractDataContext
import vs


class Separator(AbstractControl):

    def __init__(self, dialog_id: int, control_id: int, help_text: str, data_parent: AbstractDataContext,
                 data_context: str):
        super().__init__(dialog_id, control_id, help_text, data_parent, data_context, data_disabled='')
        vs.CreateSeparator(dialog_id, control_id, 0)

    def _setup(self):
        pass

    def _update(self):
        pass

    def _on_control_event(self, data: int):
        pass


# ----------------------------------------------------------------------------------------------------------------------
#   <separator/>
# ----------------------------------------------------------------------------------------------------------------------

def create(dialog_id: int, control_id: int, data: dict, data_parent: AbstractDataContext) -> Separator:
    return Separator(dialog_id, control_id, data.get('@help', ''), data_parent, data.get('@data-context', ''))
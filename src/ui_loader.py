from PySide6.QtCore import QFile, QObject
from PySide6.QtUiTools import QUiLoader


class UiLoader(QUiLoader):
    def __init__(self, base_instance):
        super().__init__(base_instance)
        self.base_instance = base_instance

    def createWidget(self, class_name, parent=None, name=""):
        if parent is None and self.base_instance is not None:
            widget = self.base_instance
        else:
            widget = super().createWidget(class_name, parent, name)

        if name:
            widget.setObjectName(name)
        return widget


def load_ui(base_instance, ui_path):
    ui_file = QFile(str(ui_path))
    if not ui_file.open(QFile.OpenModeFlag.ReadOnly):
        raise RuntimeError(f"Unable to open UI file: {ui_path}")

    try:
        loader = UiLoader(base_instance)
        loaded_widget = loader.load(ui_file)
    finally:
        ui_file.close()

    if loaded_widget is None:
        raise RuntimeError(loader.errorString())

    for child in base_instance.findChildren(QObject):
        name = child.objectName()
        if name:
            setattr(base_instance, name, child)

    return loaded_widget

import xml.etree.ElementTree as ET

from PySide6.QtCore import QCoreApplication, QFile, QObject
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QComboBox


TRANSLATABLE_PROPERTIES = {
    "accessibleDescription",
    "accessibleName",
    "statusTip",
    "text",
    "title",
    "toolTip",
    "whatsThis",
    "windowTitle",
}

PROPERTY_SETTERS = {
    "accessibleDescription": "setAccessibleDescription",
    "accessibleName": "setAccessibleName",
    "statusTip": "setStatusTip",
    "text": "setText",
    "title": "setTitle",
    "toolTip": "setToolTip",
    "whatsThis": "setWhatsThis",
    "windowTitle": "setWindowTitle",
}


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
    context, sources = read_ui_translation_sources(ui_path)
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

    base_instance._ui_translation_context = context
    base_instance._ui_translation_sources = sources
    retranslate_loaded_ui(base_instance)

    for child in base_instance.findChildren(QObject):
        name = child.objectName()
        if name:
            setattr(base_instance, name, child)

    return loaded_widget


def read_ui_translation_sources(ui_path):
    tree = ET.parse(str(ui_path))
    root = tree.getroot()
    context = root.findtext("class") or ""
    sources = {}

    for element in root.iter():
        if element.tag not in {"widget", "action", "actiongroup"}:
            continue

        object_name = element.attrib.get("name")
        if not object_name:
            continue

        object_sources = {}
        for property_element in element.findall("property"):
            property_name = property_element.attrib.get("name")
            if property_name not in TRANSLATABLE_PROPERTIES:
                continue

            string_element = property_element.find("string")
            if string_element is None or string_element.attrib.get("notr") == "true":
                continue

            object_sources[property_name] = string_element.text or ""

        item_sources = []
        for item_element in element.findall("item"):
            for property_element in item_element.findall("property"):
                if property_element.attrib.get("name") != "text":
                    continue

                string_element = property_element.find("string")
                if string_element is None or string_element.attrib.get("notr") == "true":
                    continue

                item_sources.append(string_element.text or "")

        if item_sources:
            object_sources["items"] = item_sources

        if object_sources:
            sources[object_name] = object_sources

    return context, sources


def retranslate_loaded_ui(base_instance):
    context = getattr(base_instance, "_ui_translation_context", "")
    sources = getattr(base_instance, "_ui_translation_sources", {})
    if not context or not sources:
        return

    for object_name, object_sources in sources.items():
        target = _find_translation_target(base_instance, object_name)
        if target is None:
            continue

        for property_name, source in object_sources.items():
            if property_name == "items":
                _retranslate_combo_items(context, target, source)
                continue

            setter_name = PROPERTY_SETTERS.get(property_name)
            setter = getattr(target, setter_name, None)
            if setter is None:
                continue

            setter(translate_ui_text(context, source))


def _find_translation_target(base_instance, object_name):
    if base_instance.objectName() == object_name:
        return base_instance

    return base_instance.findChild(QObject, object_name)


def _retranslate_combo_items(context, target, sources):
    if not isinstance(target, QComboBox):
        return

    for index, source in enumerate(sources):
        if index >= target.count():
            break

        target.setItemText(index, translate_ui_text(context, source))


def translate_ui_text(context, source):
    translated = QCoreApplication.translate(context, source)
    if source and not translated:
        return source

    return translated

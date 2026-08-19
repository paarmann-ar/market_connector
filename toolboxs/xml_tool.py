import xml.etree.ElementTree as ET


class XmlTool:
    @staticmethod
    def get_item(context: str, key: str):
        root = ET.fromstring(context)

        for elem in root.iter():
            if elem.tag.endswith(key):
                return elem.text
        return None

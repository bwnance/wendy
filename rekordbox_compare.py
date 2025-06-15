from lxml import etree
import regex as re

xml_path_modified = "/Users/bea.nance/Documents/tidal_xml.xml"
xml_path_imported = "/Users/bea.nance/Documents/tidal_xml.xml"

def parse_xml(xml_path):
    """
    Parse the XML file and return the root element.
    """
    with open(xml_path, 'r', encoding="latin1") as file:
        xml_content = file.read()
    parser = etree.XMLParser(recover=True)
    root = etree.fromstring(xml_content.encode('latin1'), parser)
    return root

root_modified = parse_xml(xml_path_modified)
root_imported = parse_xml(xml_path_imported)
collection_modified = root_modified.find(".//COLLECTION")
collection_imported = root_imported.find(".//COLLECTION")
collection_tracks = collection_modified.findall(".//TRACK")
collection_tracks_imported = collection_imported.findall(".//TRACK")

collection_track_names = set([track.get("Name") for track in collection_tracks])
collection_track_names_imported = set([track.get("Name") for track in collection_tracks_imported])

# Compare the two lists of track name
diff_1 = collection_track_names - collection_track_names_imported
print(f"Tracks in modified collection but not in imported collection: {diff_1}")
diff_2 = collection_track_names_imported - collection_track_names
print(f"Tracks in imported collection but not in modified collection: {diff_2}")
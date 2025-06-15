from lxml import etree
import regex as re

xml_path = "/Users/bea.nance/Documents/tidal_xml.xml"

def parse_xml(xml_path):
    """
    Parse the XML file and return the root element.
    """
    with open(xml_path, 'r', encoding="latin1") as file:
        xml_content = file.read()
    parser = etree.XMLParser(recover=True)
    root = etree.fromstring(xml_content.encode('latin1'), parser)
    return root

root = parse_xml(xml_path)
collection = root.find(".//COLLECTION")
playlists = root.find(".//PLAYLISTS")[0] # first node is root

seen_local_tracks = {} # (name,artist): id
seen_tidal_tracks = {} # (name,artist): id
track_mapping = {} # tidal id: id
remove_track_ids = []
for node in collection:
    name = node.get("Name")
    artist = node.get("Artist")
    id = node.get("TrackID")
    location = node.get("Location")
    if 'localhosttidal' in location:
        # Tidal track
        if (name, artist) not in seen_tidal_tracks:
            seen_tidal_tracks[(name, artist)] = id
    elif 'soundcloud' in location:
        remove_track_ids.append(id)
    elif '/rekordbox/' in location:
        # backed up from rekordbox, don't put in collection
        remove_track_ids.append(id)
    else:
        # Local track
        if (name, artist) not in seen_local_tracks:
            seen_local_tracks[(name, artist)] = id

for id in remove_track_ids:
    track = collection.find(f".//TRACK[@TrackID='{id}']")
    if track is not None:
        collection.remove(track)

unmatched_tidal = []
for tup, id in seen_tidal_tracks.items():
    if tup in seen_local_tracks:
        local_id = seen_local_tracks[tup]
        track_mapping[id] = local_id
        # print(f"Mapping Tidal track {id} to local track {local_id}")
    else:
        unmatched_tidal.append((tup, id))
        # print(f"Tidal track {id}, {tup} not found in local tracks")
unmatched_local = []
for tup, id in seen_local_tracks.items():
    if tup not in seen_tidal_tracks:
        unmatched_local.append((tup, id))
        # print(f"Local track {id}, {tup} not found in Tidal tracks")

still_unmatched = set([id for _, id in unmatched_tidal])
for tup_t, id_t in unmatched_tidal:
    for tup_l, id_l in unmatched_local:
        if id_t == id_l:
            continue
        name_1 = tup_t[0].lower()
        artist_1 = tup_t[1].lower()
        name_2 = tup_l[0].lower()
        artist_2 = tup_l[1].lower()
        if name_1 == name_2 and (artist_1 in artist_2 or artist_2 in artist_1):
            # print(f"Unmatched tracks {id_t} and {id_l} are similar: {name_1} - {artist_1} and {name_2} - {artist_2}")
            track_mapping[id_t] = id_l
            still_unmatched.discard(id_t)

id_to_tup_tidal = {id: tup for tup, id in unmatched_tidal}
unmatched_tidal = [(id_to_tup_tidal[id], id) for id in still_unmatched]
unmatched_local = [(tup, id) for tup, id in unmatched_local if id not in track_mapping.values()]
still_unmatched = set([id for _, id in unmatched_tidal])
for tup_t, id_t in unmatched_tidal:
    for tup_l, id_l in unmatched_local:
        if id_t == id_l:
            continue
        name_1 = tup_t[0].lower().replace("'", '')
        artist_1 = tup_t[1].lower()
        name_2 = tup_l[0].lower().replace("'", '')
        artist_2 = tup_l[1].lower()
        if (name_1 in name_2 or name_2 in name_1) and (artist_1 in artist_2 or artist_2 in artist_1):
            # print(f"Unmatched tracks {id_t} and {id_l} are similar: {name_1} - {artist_1} and {name_2} - {artist_2}")
            track_mapping[id_t] = id_l
            still_unmatched.discard(id_t)

id_to_tup_tidal = {id: tup for tup, id in unmatched_tidal}
unmatched_tidal = [(id_to_tup_tidal[id], id) for id in still_unmatched]
unmatched_local = [(tup, id) for tup, id in unmatched_local if id not in track_mapping.values()]
for tup_t, id_t in unmatched_tidal:
    for tup_l, id_l in unmatched_local:
        if id_t == id_l:
            continue
        name_1 = tup_t[0].lower()
        name_1 = re.sub(r'\\x..\s*','', str(bytes(name_1, 'utf-8'))).replace("b'", '').replace("'", '')
        artist_1 = tup_t[1].lower()
        name_2 = tup_l[0].lower()
        name_2 = re.sub(r'\\x..\s*','', str(bytes(name_2, 'utf-8'))).replace("b'", '').replace("'", '')
        artist_2 = tup_l[1].lower()
        if (name_1 in name_2 or name_2 in name_1) and (artist_1 in artist_2 or artist_2 in artist_1):
            # print(f"Unmatched tracks {id_t} and {id_l} are similar: {name_1} - {artist_1} and {name_2} - {artist_2}")
            track_mapping[id_t] = id_l
            still_unmatched.discard(id_t)

id_to_tup_tidal = {id: tup for tup, id in unmatched_tidal}
unmatched_tidal = [(id_to_tup_tidal[id], id) for id in still_unmatched]
unmatched_local = [(tup, id) for tup, id in unmatched_local if id not in track_mapping.values()]
for tup_t, id_t in unmatched_tidal:
    for tup_l, id_l in unmatched_local:
        if id_t == id_l:
            continue
        name_1 = tup_t[0].lower().replace('.', '')
        # name_1 = re.sub(r' (.+)', '', tup_t[0].lower()).replace('.', '')
        artist_1 = tup_t[1].lower()
        # name_2 = re.sub(r' (.+)', '', tup_t[0].lower()).replace('.', '')
        name_2 = tup_l[0].lower().replace('.', '')
        artist_2 = tup_l[1].lower()
        if (name_1 in name_2 or name_2 in name_1) and (artist_1 in artist_2 or artist_2 in artist_1):
            # print(f"Unmatched tracks {id_t} and {id_l} are similar: {name_1} - {artist_1} and {name_2} - {artist_2}")
            track_mapping[id_t] = id_l
            still_unmatched.discard(id_t)


for id in still_unmatched:
    tup = id_to_tup_tidal[id]
    name = tup[0]
    artist = tup[1]
    print(f"Unmatched Tidal track: {id}, {name} - {artist}")

all_playlist_track_ids = []
for playlist in playlists:
    all_playlist_tracks = playlist.findall(".//TRACKS")
    playlist_track_ids = [t.get("Key") for t in all_playlist_tracks]
    all_playlist_track_ids.extend(playlist_track_ids)


local_id_to_tidal_id = {v: k for k, v in track_mapping.items()}
for track in collection.findall(".//TRACK"):
    track_id = track.get("TrackID")
    # if track_id == "152239428":
    #     breakpoint()
    if track_id in local_id_to_tidal_id:
        if track_id == "30716593":
            breakpoint()
        # print(f"Replacing Tidal track {track_id} with local track {local_id_to_tidal_id[track_id]}")
        tidal_track = collection.find(f".//TRACK[@TrackID='{local_id_to_tidal_id[track_id]}']")
        if tidal_track is not None:
            collection.remove(tidal_track)
        local_track = collection.find(f".//TRACK[@TrackID='{track_id}']")
        local_track.set("TrackID", local_id_to_tidal_id[track_id])
        if track_id in all_playlist_track_ids:
            raise Exception(f"Track {track_id} is in a playlist, cannot remove it.")

#check integrity of playlists - every track in a playlist should be in the collection
for playlist in playlists:
    all_playlist_tracks = playlist.findall(".//TRACK")
    bad_tracks = []
    for track in all_playlist_tracks:
        track_id = track.get("Key")
        track = collection.find(f".//TRACK[@TrackID='{track_id}']")
        if track is None and track_id in remove_track_ids:
            # print(f"Track {track_id} not found in collection!")
            bad_tracks.append(track_id)
    if bad_tracks:
        # print(f"Playlist {playlist.get('Name')} has tracks not found in collection: {bad_tracks}")
        for track_id in bad_tracks:
            track = playlist.find(f".//TRACK[@Key='{track_id}']")
            if track is not None:
                playlist.remove(track)
                # print(f"Removed track {track_id} from playlist {playlist.get('Name')}")

# Save the modified XML to a new file
output_path = "/Users/bea.nance/Documents/tidal_xml_modified.xml"
with open(output_path, 'wb') as file:
    file.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8'))
print(f"Modified XML saved to {output_path}")

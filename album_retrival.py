import musicbrainzngs
from colorthief import ColorThief #type: ignore
import io
from collections import Counter
#import logging

#used for musicbrainz to give error info
#logging.basicConfig(level=logging.DEBUG)

# Set application details and contact
musicbrainzngs.set_useragent("Album_Poster_Generator", "1.0", "kisituaaron@gmail.com")

#gets the ID for the album release group
def get_releasegroupid(search_album, search_artist):
    try:
        #search for the album using the name and artist provided
        result = musicbrainzngs.search_release_groups(artist = search_artist, releasegroup = search_album)

        #if the album was found using the search return the id
        if result['release-group-list']: 
            album = result['release-group-list'][0]
            return album['id']

        else:
            print("Could Not find release group")

    except musicbrainzngs.WebServiceError as e:
        print(f"an error occured(release group id): {e}")

#uses release group ID to get the ID of the first release(album) within the release group
def get_releaseID_from_releasegroup(release_groupID):
    try:
        #get the release group by the ID we found, include all the release versions
        result = musicbrainzngs.get_release_group_by_id(release_groupID, includes=["releases"])

        #check if the release-group and releases(album) keys are in result
        if 'release-group' in result and 'release-list' in result['release-group']:
            album = result['release-group']['release-list']

            #if there are any releases(albums) within the release group, return the first one
            if album:
                return album[0]['id']
            
        else:
            print("could not find release(album) within the release group")

    except musicbrainzngs.WebServiceError as e:
        print(f"an error occured(release ID): {e}")

#attempt to download the album cover
def get_cover(album_id):
    try:
        cover = musicbrainzngs.get_image_front(album_id)
        return cover

    except musicbrainzngs.WebServiceError as e:
        print(f"An error occurred(cover): {e}")

#gets the tracklist
def get_tracklist(album_id):
    try:
        #gets the release(album) by the id, including the list of recordings
        result = musicbrainzngs.get_release_by_id(album_id, includes=["recordings"])
        mediums = result.get('release', {}).get('medium-list', [])
        
        # use set comprehension to simplify this part
        tracklist = {track['recording']['title'] for medium in mediums for track in medium.get('track-list', [])}

        #turn the set back into a list and return it
        return list(tracklist)


    except musicbrainzngs.WebServiceError as e:
        print(f"An error occurred(tracks): {e}")

#get the most used colors in album cover
def get_palette(album_cover):
    #turns the album cover into an image that colortheif can use
    colors = ColorThief(io.BytesIO(album_cover))

    #gets the 5 most prominent colors from the image and returns them
    palette = colors.get_palette(color_count = 5)
    return palette

#get duration of album
def get_duration(album_id):
    try:
        #gets the release(album) by the id, including the list of recordings
        result = musicbrainzngs.get_release_by_id(album_id, includes=["recordings"])

        # Extract the list of mediums(cd, dvd, casette, etc)
        mediums = result.get('release', {}).get('medium-list', [])

        # Sum the lengths of all tracks in all mediums
        total_len_ms = sum(
            int(track['length']) 
            for medium in mediums 
            for track in medium.get('track-list', []) 
            if 'length' in track
        )
        
        # Convert the  milliseconds to minutes and seconds
        minutes, seconds = divmod(total_len_ms // 1000, 60)

        # Format the time string
        time_str = f"{minutes}:{seconds:02}"

        return time_str

    except musicbrainzngs.WebServiceError as e:
        print(f"An error occurred(length): {e}")

#gets label info about album
def get_label_info(album_id):
    try:
        # Get the release (album) by the id, including the label information
        result = musicbrainzngs.get_release_by_id(album_id, includes=["labels"])

        # Check if there is label info in the result
        label_info_list = result.get('release', {}).get('label-info-list', [])
        
        # If no label info is found, return independently released
        if not label_info_list:
            return "Released Independently"
        
        # Retrieve label names or return independant if no labels
        labels = []
        for label_info in label_info_list:
            label = label_info.get('label', {})
            label_name = label.get('name', "[no label]")
            if label_name == "[no label]":
                return "Released Independently"
            labels.append(label_name)
        
        # Join all labels into a single string
        label_str = "Released by " + ", ".join(labels)
        return label_str

    except musicbrainzngs.WebServiceError as e:
        print(f"An error occurred(label): {e}")

#get album release date
def get_release_date(album_id):
    try:
        #gets the release(album) by the id, including the label
        result = musicbrainzngs.get_release_by_id(album_id)

        if 'date' in result['release']:
            return result['release']['date']

    except musicbrainzngs.WebServiceError as e:
        print(f"An error occurred(date): {e}")

# Gets the name of the album
def get_album_name(release_group_id):
    try:
        # Get all releases in the release group
        releases = musicbrainzngs.browse_releases(release_group=release_group_id)['release-list']
        
        # Extract titles from all releases
        titles = [release['title'] for release in releases]

        # Count occurrences of each title
        title_counts = Counter(titles)

        # Get the most common title
        most_common_title = title_counts.most_common(1)[0][0]

        return most_common_title

    except musicbrainzngs.WebServiceError as e:
        print(f"An error occurred(album name): {e}")

#gets the name of the artist
def get_artist_name(album_releasegroupid):
    try:
        result = musicbrainzngs.get_release_group_by_id(album_releasegroupid, includes=["artists"])

        #use artist credit phrase to account for albums with multiple artists
        if 'artist-credit-phrase' in result['release-group']:
            return result['release-group']['artist-credit-phrase']
            
    except musicbrainzngs.WebServiceError as e:
        print(f"An error occurred(artist name): {e}")
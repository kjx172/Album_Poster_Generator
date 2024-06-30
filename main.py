from album_retrival import (get_releasegroupid, get_releaseID_from_releasegroup, get_cover, #type: ignore
                            get_tracklist, get_palette, get_duration, get_label_info,
                            get_release_date, get_album_name, get_artist_name)
from poster_creator import create_poster  # type: ignore

#gets the details for the album
def fetch_album_details(search_album, search_artist):
    #searches for release groups
    album_releasegroupid = get_releasegroupid(search_album, search_artist)

    #if no release group found return
    if not album_releasegroupid:
        return None
    
    #find the release(album) ID from the release group
    album_id = get_releaseID_from_releasegroup(album_releasegroupid)

    #if no albums found return
    if not album_id:
        return None
    
    #retrieves and returns the album data
    return {
        "cover": get_cover(album_id),
        "tracklist": get_tracklist(album_id),
        "palette": get_palette(get_cover(album_id)),
        "length": get_duration(album_id),
        "label_info": get_label_info(album_id),
        "release_date": get_release_date(album_id),
        "album_name": get_album_name(album_releasegroupid),
        "artist_name": get_artist_name(album_releasegroupid),
    }


# Defining main function 
def main(): 
    search_album = input("Enter the name of the album:")
    search_artist = input("Enter the name of the artist:")

    
    album_details = fetch_album_details(search_album, search_artist)

    if not album_details:
        print("The album you were looking for could not be found")
        return
    


    #passes album cover into poster creator
    create_poster(album_details['cover'], album_details['tracklist'], album_details['palette'],
                  album_details['length'], album_details['label_info'], album_details['release_date'],
                  album_details['album_name'], album_details['artist_name'])
  
  
# Using the special variable __name__ 
if __name__=="__main__": 
    main()

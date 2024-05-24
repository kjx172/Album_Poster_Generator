from album_retrival import get_releasegroupid, get_releaseID_from_releasegroup, get_cover, get_tracklist, get_palette # type: ignore
from poster_creator import create_poster #type: ignore

# Defining main function 
def main(): 
    search_album = input("Enter the name of the album:")
    search_artist = input("Enter the name of the artist:")

    #searches for the album cover art by release ID
    album_releasegroupid = get_releasegroupid(search_album, search_artist)
    if album_releasegroupid:
        album_id = get_releaseID_from_releasegroup(album_releasegroupid)

    #gets the the album cover, tracklist, palette
    album_cover = get_cover(album_id)
    tracklist = get_tracklist(album_id)
    palette = get_palette(album_cover)

    #passes album cover into poster creator
    create_poster(album_cover, search_album, tracklist, palette)
  
  
# Using the special variable __name__ 
if __name__=="__main__": 

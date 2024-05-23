import musicbrainzngs

# Set application details and contact
musicbrainzngs.set_useragent("Album_Poster_Generator", "1.0", "kisituaaron@gmail.com")

#gets the ID for the album release group
def get_releasegroupid(search_album, search_artist):
    try:
        #search for the album using the name and artist provided
        result = musicbrainzngs.search_release_groups(artist = search_artist, releasegroup = search_album)

        if result['release-group-list']: #if the album was found using the search return the id
            album = result['release-group-list'][0]
            return album['id']

        else:
            print("Could Not find release group")

    except musicbrainzngs.WebServiceError as e:
        print(f"an error occured: {e}")

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
        print(f"an error occured: {e}")

#attempt to download the album cover
def get_cover(album_releasegroupid, search_album):
    try:
        cover = musicbrainzngs.get_image_front(releaseid=album_releasegroupid)

        with open(f"{search_album}_cover.jpg", "wb") as file:
            file.write(cover)
        print(f"Successfully downloaded image and saved as {search_album}_cover.jpg")

    except musicbrainzngs.WebServiceError as e:
        print(f"An error occurred: {e}")

# Defining main function 
def main(): 
    search_album = input("Enter the name of the album:")
    search_artist = input("Enter the name of the artist:")

    #searches for the album cover art by release ID
    album_releasegroupid = get_releasegroupid(search_album, search_artist)
    if album_releasegroupid:
        album_id = get_releaseID_from_releasegroup(album_releasegroupid)

    #downloads the album
    get_cover(album_id, search_album)

  
  
# Using the special variable __name__ 
if __name__=="__main__": 

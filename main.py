import musicbrainzngs

# Set application details and contact
musicbrainzngs.set_useragent("Album_Poster_Generator", "1.0", "kisituaaron@gmail.com")

def get_releasegroupid(search_album, search_artist):
    try:
        result = musicbrainzngs.search_release_groups(artist = search_artist, releasegroup = search_album)

        if result['release-group-list']:
            album = result['release-group-list'][0]
            return album['id']

        else:
            print("Could Not find album")

    except musicbrainzngs.WebServiceError as e:
        print(f"an error occured: {e}")

#searching by artist name
#def get_cover(album_releasegroupid):
    #empty for now

# Defining main function 
def main(): 
    search_album = input("Enter the name of the album:")
    search_artist = input("Enter the name of the artist:")
    album_releasegroupid = get_releasegroupid(search_album, search_artist)

    print(album_releasegroupid)
  
  
# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main() 

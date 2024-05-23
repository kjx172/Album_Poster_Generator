import musicbrainzngs

# Set application details and contact
musicbrainzngs.set_useragent("Album_Poster_Generator", "1.0", "kisituaaron@gmail.com")

#searching by artist name
def search_artist(artistName):
    try: #if an error is not thrown then try to find artist
        result = musicbrainzngs.search_artists(artist=artistName)
        
        #if a result is found off the search
        if result['artist-list']:
            #print artist name and ID
            artist = result['artist-list'][0]
            print(f"Artist Name: {artist['name']}")
            print(f"Artist ID: {artist['id']}")

            #if disambiguation or country is found print those as well
            if 'disambiguation' in artist:
                print(f"Disambiguation: {artist['disambiguation']}")
            if 'country' in artist:
                print(f"Country: {artist['country']}")

        #if nothing is found off the search
        else:
            print("No artist found.")

    except musicbrainzngs.WebServiceError as e:
        print(f"an error occured: {e}")

# Defining main function 
def main(): 
    search_val = input("Enter an artists name:")

    # Example usage
    search_artist(search_val)
  
  
# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main() 

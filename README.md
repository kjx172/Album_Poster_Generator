# Album Poster Generator
Album Poster Generator is a Python-based application designed to generate posters for albums using data from the MusicBrainz database. It retrieves album information, extracts prominent colors from the album cover, and gathers various metadata about the album.

## Features
- Retrieve album information and cover images using the MusicBrainz API.
- Extract prominent colors from album covers.
- Gather metadata about the album, including tracklist, duration, label info, release date, album name, and artist name.

## Installation
To get started with Album Poster Generator, follow these steps:

1. Clone the repository:

bash
  git clone https://github.com/yourusername/album_poster_generator.git
  cd album_poster_generator

2. Install the required dependencies:

bash
  pip install -r requirements.txt

3. Set up MusicBrainz user agent
  edit this line to use your information
  musicbrainzngs.set_useragent("Album_Poster_Generator", "1.0", "your-email@example.com")

## Example
Entering "More life" for the album and "Drake" for the artist will generate the file named generated_image.jpg in this repo

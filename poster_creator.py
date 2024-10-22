import pygame
import pygame.image
import io
import datetime
#import logging

#used for musicbrainz to give error info
#logging.basicConfig(level=logging.DEBUG)

#set the constant variables 
background_color = (255, 255, 240)
width, height = 2304, 3456
color_width, color_height = 100, 100
top_margin, bottom_margin, left_margin, right_margin = 150, 3306, 150, 2154
marginalized_width, marginalized_height, marginalized_center = 2004, 3156, 1002
text_portion_y = 2254
track_font_size, column_gap = 80, 15
info_font_size, album_name_font_size, artist_name_font_size = 40, 300, 90
artist_name_x, artist_name_y = marginalized_center + 500, 2900 #+500 being the offset from center and 2900 being random height near bottom
album_name_x, album_name_y = marginalized_center + 500, 3000 + artist_name_font_size #+500 being the offset from center
album_font_name, info_font_name, artist_font_name = "Futura", "courier new", "courier new"
font_color = (0, 0, 0)
font_name = pygame.font.get_default_font()

#Reformats the date
def format_date(raw_date):
    #Split the date format into parts
    date_components = raw_date.split('-')

    #if the date contains month day year
    if len(date_components) == 3:
        year, month, day = date_components

        # Get the month name, year and day are place holders(used my birthday as place holder)
        month_name = datetime.date(2004, int(month), 25).strftime('%B')

        # Return date with month name instead of number
        return f"{day} {month_name} {year}"
    
    #if the date contains month year
    elif len(date_components) == 2:
        year, month = date_components
        
        # Get the month name, year and day are place holders(used my birthday as place holder)
        month_name = datetime.date(2004, int(month), 25).strftime('%B')

        # Return date with month name and year only
        return f"{month_name} {year}"
    
    #if the date contains year only
    elif len(date_components) == 1:
        year = date_components[0]
        # Return year only
        return year
    
    #should not happen but just in case the date doesnt work
    else:
        # If the input format is unexpected, raise an error or return a default value
        raise ValueError("Invalid date format")

#prevents albums with multiple labels from taking up too much of the screen
def info_wrap_text(surface, font, text, color, max_width, starting_x, starting_y):

    #splits the text into words and creates an array for the lines
    words = text.split(' ')
    lines = []
    current_line = ''

    #for each word if the word doesnt cause the current line to reach the maximum width we add it to the current line, otherwise start a new line
    for i, word in enumerate(words):

        if i == 0:
            current_line += word
            continue

        if font.size(current_line + ' ' + word)[0] <= max_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    #places the lines onto the screen
    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(topleft=(starting_x, starting_y))
        surface.blit(text_surface, text_rect)
        starting_y += text_rect.height

    return text_surface, text_rect

#places album name in bottom right corner
def fit_album(screen, album_font, album_name, font_color, marginalized_width, marginalized_center, album_name_x, album_name_y):
    while True:
        #attempt to render the album text
        album_text_surface = album_font.render(album_name, True, font_color)
        album_text_rect = album_text_surface.get_rect(topleft=(album_name_x, album_name_y))

        #check if the album title can be put at the  album_name_x and album_name_y without running into the right margin, if so break
        if album_text_rect.right <= right_margin:
            break

        #step 1: keep moving the album title topleft x 50 pixels to the left while maintaining the font size
        album_name_x -= 50

        #if the next movement would hit or pass the marginalized center move to Step 2: Try to fit the album name by wrapping into two lines
        if album_name_x <= marginalized_center:
            #set the album name x to the marginalized center and split the text into words
            album_name_x = marginalized_center

            words = album_name.split(' ')
            first_line = ''
            second_line = ''

            #add each word to the first line until it reachs the right margin, then start a new line and add the following words into that line
            for i, word in enumerate(words):
                if i == 0:
                    first_line += word
                    continue

                if album_font.size(first_line + ' ' + word)[0] <= marginalized_width:
                    first_line += ' ' + word
                else:
                    second_line = ' '.join(words[i:])
                    break

            #attempt to render the two lines
            first_line_surface = album_font.render(first_line, True, font_color)
            first_line_rect = first_line_surface.get_rect(topleft=(album_name_x, album_name_y))

            second_line_surface = album_font.render(second_line, True, font_color)
            second_line_rect = second_line_surface.get_rect(topleft=(album_name_x, album_name_y + album_font.get_linesize()))

            #checks if the two lines hit the right margin
            if first_line_rect.right <= right_margin and second_line_rect.right <= right_margin:
                #puts the lines onto the screen, if first line is empty then only put second line
                if first_line:
                    screen.blit(first_line_surface, first_line_rect)
                screen.blit(second_line_surface, second_line_rect)
                return second_line_rect

            # If the lines still hit the right margin, move to Step 3: Reduce font size and start over
            album_font_size = album_font.get_height()
            if album_font_size <= 0:
                break  # Prevent infinite loop if font size becomes too small
            album_font = pygame.font.SysFont(album_font_name, album_font_size - 50)

            album_name_x = marginalized_center + 500

    # Blit the final album name surface onto the screen
    screen.blit(album_text_surface, album_text_rect)
    return album_text_rect

#place artist name right above the album name
def fit_artist(screen, artist_font, artist_name, font_color, marginalized_width, marginalized_center, artist_name_x, artist_name_y, album_name_rect):
    while True:
        #Attempt to render the artist text
        artist_text_surface = artist_font.render(artist_name, True, font_color)
        artist_text_rect = artist_text_surface.get_rect(topleft=(artist_name_x, artist_name_y))

        #Check if the artist title can be put at the artist_name_x and artist_name_y without running into the right margin or colliding with album name
        if artist_text_rect.right <= right_margin and artist_text_rect.bottom <= album_name_rect.top:
            break

        #Step 1: Keep moving the artist title topleft x 15 pixels to the left while maintaining the font size
        artist_name_x -= 15

        #If the next movement would pass the album text, move to Step 2: Try to fit the artist name by wrapping into two lines
        if artist_name_x <= album_name_rect.left:
            #Set the artist name x to the album name left and split the text into words
            artist_name_x = album_name_rect.left

            words = artist_name.split(' ')
            first_line = ''
            second_line = ''

            #Add each word to the first line until it reaches the right margin, then start a new line and add the following words into that line
            for i, word in enumerate(words):
                if i == 0:
                    first_line += word
                    continue

                if artist_font.size(first_line + ' ' + word)[0] <= marginalized_width:
                    first_line += ' ' + word
                else:
                    second_line = ' '.join(words[i:])
                    break

            #Attempt to render the two lines
            first_line_surface = artist_font.render(first_line, True, font_color)
            first_line_rect = first_line_surface.get_rect(topleft=(artist_name_x, artist_name_y))

            second_line_surface = artist_font.render(second_line, True, font_color)
            second_line_rect = second_line_surface.get_rect(topleft=(artist_name_x, artist_name_y + artist_font.get_linesize()))

            #Checks if the two lines hit the right margin or collide with album name
            if first_line_rect.right <= right_margin and first_line_rect.bottom <= album_name_rect.top and second_line_rect.right <= right_margin:

                #Puts the lines onto the screen, if first line is empty then only put second line
                if first_line:
                    screen.blit(first_line_surface, first_line_rect)
                screen.blit(second_line_surface, second_line_rect)
                return second_line_rect
            
             #If the lines still hit the right margin, move to Step 3: Reduce font size and start over
            artist_font_size = artist_font.get_height()
            if artist_font_size <= 0:
                break  #Prevent infinite loop if font size becomes too small
            artist_font = pygame.font.SysFont(artist_font_name, artist_font_size - 15)

            artist_name_x = marginalized_center + 500

    # Blit the final artist name surface onto the screen
    screen.blit(artist_text_surface, artist_text_rect)
    return artist_text_rect

#places tracklist onto screen
def fit_tracklist(screen, tracklist, track_font, album_name_rect, artist_name_rect, squares_rect, text_portion_y, left_margin, font_color):
    def check_collision(rect, elements):
        return any(rect.colliderect(element) for element in elements)

    # First, try to fit all tracks in one column with the original font size
    last_track_y = text_portion_y
    fits = True
    track_surfaces = []
    elements_to_check = [album_name_rect, artist_name_rect, squares_rect]
    max_right1 = 0  # Rightmost point of the first column
    max_right2 = 0  # Rightmost point of the second column

    for i, track in enumerate(tracklist):
        text_surface = track_font.render(f"{i + 1}. {track}", True, font_color)
        text_rect = text_surface.get_rect(topleft=(left_margin, last_track_y))
        track_surfaces.append((text_surface, text_rect))
        last_track_y += track_font.get_height()

        # Check if the text goes beyond the bottom margin or collides with elements
        if last_track_y > bottom_margin or check_collision(text_rect, elements_to_check):
            fits = False
            break

    if fits:
        for text_surface, text_rect in track_surfaces:
            screen.blit(text_surface, text_rect)
        return last_track_y

    # If tracks don't fit in one column, switch to two-column layout
    while True:
        fits = True
        track_surfaces = []
        last_track_y1 = text_portion_y
        last_track_y2 = text_portion_y
        column_x = left_margin
        first_column_done = False

        for i, track in enumerate(tracklist):
            text_surface = track_font.render(f"{i + 1}. {track}", True, font_color)

            if not first_column_done:
                text_rect = text_surface.get_rect(topleft=(column_x, last_track_y1))
                last_track_y1 += track_font.get_height()

                if last_track_y1 > bottom_margin:
                    first_column_done = True
                    column_x = max_right1 + column_gap
                    last_track_y1 = text_portion_y
                    text_rect = text_surface.get_rect(topleft=(column_x, last_track_y2))
                    last_track_y2 += track_font.get_height()
                else:
                    track_surfaces.append((text_surface, text_rect))
                    max_right1 = max(max_right1, text_rect.right)
            else:
                text_rect = text_surface.get_rect(topleft=(column_x, last_track_y2))
                last_track_y2 += track_font.get_height()
                track_surfaces.append((text_surface, text_rect))
                max_right2 = max(max_right2, text_rect.right)

        # Check for collisions with album name, artist name, or squares
        if any(check_collision(text_rect, elements_to_check) for _, text_rect in track_surfaces):
            fits = False
        else:
            fits = True

        if fits:
            for text_surface, text_rect in track_surfaces:
                screen.blit(text_surface, text_rect)
            return max(last_track_y1, last_track_y2)

        # Reduce font size and try again if text collides
        track_font_size = track_font.get_height()
        if track_font_size <= 0:
            break  # Prevent infinite loop if font size becomes too small
        track_font = pygame.font.Font(None, track_font_size - 2)

    print("Unable to fit the tracklist")
    return -1


def create_poster(cover, tracklist, palette, album_length, label_info, release_date, album_name, artist_name):

    # Initialize Pygame
    pygame.init()

    # Create a background and sets background color
    screen = pygame.Surface((width, height))
    screen.fill(background_color)

    #turns the musicbrainz image to an image that pygame can use
    image_data = io.BytesIO(cover)
    image_surface = pygame.image.load(image_data)

    # Scale the image to fit the surface, want it to take up entire marginalized width
    image_surface = pygame.transform.scale(image_surface, (marginalized_width, marginalized_width))

    #places the image on the screen
    screen.blit(image_surface, (left_margin,top_margin))

    #sets the top right of the square to be a 200 below image and 150 off the right edge
    top_right_x_squares = right_margin
    top_y_squares = marginalized_width + 200

    # Calculate the total width of the combined squares
    total_width = len(palette) * (color_width + 10) - 10
    # Set the top left x coordinate of the combined rectangle
    top_left_x_combined = top_right_x_squares - total_width

    # Draw the combined rectangle
    squares_rect = pygame.draw.rect(screen, background_color, (top_left_x_combined, top_y_squares, total_width, color_height))

    # Draw individual squares within the combined rectangle
    for i, color in enumerate(palette):
        top_left_x_squares = top_right_x_squares - (i + 1) * (color_width + 10) + 10
        pygame.draw.rect(screen, color, (top_left_x_squares, top_y_squares, color_width, color_height))

    #Places album name on screen
    album_font = pygame.font.SysFont(album_font_name, album_name_font_size)
    album_name_rect = fit_album(screen, album_font, album_name, font_color, marginalized_width, marginalized_center, album_name_x, album_name_y)
    
    #Places artist name on screen
    artist_font = pygame.font.SysFont(artist_font_name, artist_name_font_size)
    artist_name_rect = fit_artist(screen, artist_font,artist_name, font_color, marginalized_width, marginalized_center, artist_name_x, artist_name_y, album_name_rect)

    #places tracklist onto screen
    track_font = pygame.font.Font(font_name, track_font_size)
    last_track_y = fit_tracklist(screen, tracklist, track_font, album_name_rect, artist_name_rect, squares_rect, text_portion_y, left_margin, font_color)

    #if the tracks were unable to fit
    if last_track_y == -1:
        exit()

    #loads info font, places it 20 below the last track
    info_font = pygame.font.SysFont(info_font_name, info_font_size)
    info_starting_y = last_track_y + 40

    #add the release date to the album length
    length_year = album_length + " / " + format_date(release_date)

    #places length and year text onto screen
    length_year_text_surface = info_font.render(length_year, True, font_color)
    length_year_text_rect = length_year_text_surface.get_rect(topleft=(left_margin, info_starting_y))
    screen.blit(length_year_text_surface, length_year_text_rect)

    #for putting the labels below the length and date, set to font size
    label_starting_y = info_starting_y + info_font_size

    #places label text onto screen
    label_text_surface = info_font.render(label_info, True, font_color)
    info_wrap_text(screen, info_font, label_info, font_color, marginalized_center, left_margin, label_starting_y)

    # Save the poster as a jpg
    file_name = 'generated_image.jpg'
    pygame.image.save(screen, file_name)
    print(f"Image saved as {file_name}")

    # Quit Pygame
    pygame.quit()
    
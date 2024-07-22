import flet as ft
import random
import requests
from PIL import Image as PILImage
from io import BytesIO
import time
from bs4 import BeautifulSoup


def find_movie(genres):
    movie_list =[]
    for genre in genres:
        genre = genre.lower()
    url = f'https://www.imdb.com/search/title/?genres={"%2C".join(genres)}&title_type=feature'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    movie_list =[]
    try:
        # Make a GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
  
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find elements with a specific class
        specific_class = 'ipc-title__text'  
        class_pic = "ipc-image"
        class_desc = "ipc-html-content-inner-div"
        elements = soup.find_all(class_=specific_class)
        pictures = soup.find_all(class_=class_pic)
        discreption = soup.find_all(class_=class_desc)
        # Extract and print data from those elements
        for i in range(1,len(elements)-1):
            new_list=[]
            new_list.append(elements[i].text.strip())  # .text gets the text inside the element, .strip() removes surrounding whitespace
            new_list.append(pictures[i-1]["src"])
            new_list.append(discreption[i-1].text.strip())
            movie_list.append(new_list)
            
    except requests.exceptions.RequestException as e:
        print('Error during request:', e)
    except Exception as e:
        print('Error:', e)
    return random.choice(movie_list)



def button_clicked(e, page):
    # Assuming checkboxes and textAndGenresButton are defined elsewhere
    chosen_genres = [checkbox.label for checkbox in checkboxes if checkbox.value]

    # Check if any genres are selected
    if chosen_genres:
        # Fetch a random movie based on chosen genres
        chosen_movie = find_movie(chosen_genres)
        
        if chosen_movie:
            movie_text = ft.Text(f"\nName: {chosen_movie[0][4:]}\nPlot: {chosen_movie[-1]}", size =30)
            # Get the dimensions of the movie poster
            poster_width, poster_height = get_image_size(chosen_movie[1])

            # Display the movie poster in a bottom sheet
            movieButton = ft.Image(
                            src=chosen_movie[1],
                            width=poster_width,
                            height=poster_height, 
                            fit=ft.ImageFit.NONE,
                            repeat=ft.ImageRepeat.NO_REPEAT,
                        )
            
            # shows the buttons and removes after 15 secs
            page.add(movie_text)
            page.add(movieButton)
            page.update()
            time.sleep(15)
            page.controls.remove(movie_text)
            page.controls.remove(movieButton)
            page.update()
            
    page.update()
   

def get_image_size(image_url):
    response = requests.get(image_url)
    image_data = response.content
    image = PILImage.open(BytesIO(image_data))
    return image.size


def main(page: ft.Page):
    global textAndGenresButton, checkboxes
    page.title = "Movie generator (Demo)"
    page.scroll = "adaptive"
   
    # Define checkboxes for genres
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    textAndGenresButton = ft.Text("Choose a genre and see random movie suggestions below the checkboxes:", size=20)
    
    
    checkboxes = [
        ft.Checkbox(label="Action", value=False, splash_radius=40),
        ft.Checkbox(label="Adventure", value=False, splash_radius=40),
        ft.Checkbox(label="Animation", value=False, splash_radius=40),
        ft.Checkbox(label="Comedy", value=False, splash_radius=40),
        ft.Checkbox(label="Crime", value=False, splash_radius=40),
        ft.Checkbox(label="Horror", value=False, splash_radius=40),
        ft.Checkbox(label="Mystery", value=False, splash_radius=40),
        ft.Checkbox(label="Romance", value=False, splash_radius=40),
        ft.Checkbox(label="Sci-Fi", value=False, splash_radius=40),
        ft.Checkbox(label="Thriller", value=False, splash_radius=40),
        ft.Checkbox(label="War", value=False, splash_radius=40)
    ]
    
    
    # Create submit button
    submitButton = ft.ElevatedButton(text="Show random movie!", on_click=lambda e: button_clicked(e, page))

    # Add components to the page
    page.add(textAndGenresButton)
    for checkbox in checkboxes:
        page.add(checkbox)
    
    page.add(submitButton)
    button_clicked(None, page=page)

# Launch app 
ft.app(target=main, assets_dir="assets")
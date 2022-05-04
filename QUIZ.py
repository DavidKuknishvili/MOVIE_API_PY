import json
import requests
import sqlite3

# .
movie_name = input("Enter movie name: ")
movie = requests.get(f'https://api.tvmaze.com/singlesearch/shows?q={movie_name}')
print(movie.status_code)
print(movie.headers)
print(movie.text)

# .
with open('movies.json', 'w') as movies_file:
    json.dump(movie.json(), movies_file, indent=4)

# .
""""
    API-დან მომაქვს ფილმის შესახებ ინფორმაცია როგორიცაა პრემიერის თარიღი, ჟანრები, მოკლე აღწერა, რეიტინგი და ამ ინფორმაციას ვბეჭდავ.
    აქვე დავამატებ რომ ფილმის მოძევნბა ხდება მომხმარებლის მიერ ინფუთით შეყვანილი სახელის მიხედვით რომლის კოდიც ზემოთ წერია.
"""

movie_genres = movie.json()['genres']
movie_premiered = movie.json()['premiered']
movie_rating = movie.json()['rating']['average']
movie_description = movie.json()['summary']

print(" Movie name:", movie_name, '\n',
      'premiered:', movie_premiered, '\n',
      'movie genres:', movie_genres, '\n',
      "IMDB rating:", movie_rating, '\n',
      "movie description:", movie_description)

# .
question = int(input('Do you want to add this movie in DB \n YES:1        NO:0 \n'))
if question == 1:
    conn = sqlite3.connect('movieDB.sqlite3')
    cursor = conn.cursor()

    cursor.execute('''create table if not exists movie( id INTEGER PRIMARY KEY AUTOINCREMENT, movie_name TETX, movie_premiered TEXT, movie_genres, description TEXT
    TEXT, rating FLOAT) ''')

    genres = ''
    for i in movie_genres:
        genres = genres + i + ','  # ამას იმიტომ ვაკეთებ რომ ჟანრი არის თვითონ აპიში ლისტი და მინდა სტრინგად ჩავაინსერთო ბაზაში

    cursor.execute(
        f"insert into movie (movie_name, movie_premiered, movie_genres,description, rating) values (?, ?, ?, ?, ?)", (movie_name, movie_premiered, genres, movie_description, movie_rating))
    conn.commit()
    print('ფილმი შენახულია')
else:
    print("თქვენ არ გსურთ ფილმის შენავა")
'''
    პირველ რიგში მომხმარებელს ეკითხება კოდი თავის მიერ ინფუთიტ მოძებნილი ფილმის შენახვა სურს თუ არა თუ სურს
    აირჩევს 1-ს თუ არა მაშინ 0-ს. როდესაც მომხმარებელს ენდომება ფილმის შენახვა კოდი API-დან წამოირებს ფილმის შესახებ ინფორმაციას
    როგორიცაა პრემიერის თარიღი, ჟანრები, მოკლე აღწერა, რეიტინგი და ამ ინფოს შეინახავს ბაზაში.

'''


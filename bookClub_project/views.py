from django.shortcuts import render
from .models import Book
import requests
# from functions import getCover
# import functions as f

# Create your views here.
nyt_apiKey = 'i2gBHvKpbi0ZxGtoRAzX85JBi8iOot7t'
googleBooks_apiKey ='AIzaSyDs_cKUw7nk8l-QIVUVwyPlx1a3aRo_s2Q'

def book_list(request):
    selected_genre = 'hardcover-fiction'
    #Get NYT Best Seller genres
    response_genres = requests.get('https://api.nytimes.com/svc/books/v3/lists/names.json?&api-key=' + nyt_apiKey)
    genres_data = response_genres.json()
    genres = genres_data['results']
    if request.method == "POST":
        selected_genre = request.POST['value']
        print(selected_genre)
    #Get NYT Best Seller List
    response_books = requests.get('https://api.nytimes.com/svc/books/v3/lists.json?list-name=' + selected_genre +'&api-key=' + nyt_apiKey)
    books = response_books.json()
    books_results = books['results']
    #Get Covers
    for book in books_results: 
        if book['book_details'][0]['primary_isbn10']:
            isbn = book['book_details'][0]['primary_isbn10']
            response_covers = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn + "&key=" + googleBooks_apiKey)
            cover_data = response_covers.json()
        #while loop, while cover_data['totalItems'] == 0 keep book['isbns'][i + 1][0]['isbn10']
            if cover_data['totalItems'] == 0:
                isbn = book['isbns'][0]['isbn10']
                response_covers = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn + "&key=" + googleBooks_apiKey)
                cover_data = response_covers.json()
                if cover_data['totalItems'] == 0:
                    isbn = book['isbns'][1]['isbn10']
                    response_covers = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn + "&key=" + googleBooks_apiKey)
                    cover_data = response_covers.json()
        else: 
            cover_data = "Missing Cover"

        book['cover'] = cover_data
        
    return render(request, 'book_list.html', {
        'books': books,
        'genres': genres,
        'selected_genre': selected_genre,
    })



# TEST API LINK FOR NYT API BOOK
# https://api.nytimes.com/svc/books/v3/lists.json?list-name=hardcover-fiction&api-key=i2gBHvKpbi0ZxGtoRAzX85JBi8iOot7t

# TEST API LINK FOR NYT API BOOK USING NYT ISBN
# https://www.googleapis.com/books/v1/volumes?q=isbn:0399179364&key=AIzaSyDs_cKUw7nk8l-QIVUVwyPlx1a3aRo_s2Q

#List of names like fiction Biography etc
#https://api.nytimes.com/svc/books/v3/lists/names.json?&api-key=i2gBHvKpbi0ZxGtoRAzX85JBi8iOot7t
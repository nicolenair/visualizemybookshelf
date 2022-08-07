# Visualize My Bookshelf

A web app which automatically extracts and processes data about the books that a user has read and then visualizes that data in interesting ways.
The algorithm currently sources data from both the Google Books API and Wikipedia, using both rule-based and deep learning-based extraction methods.

## Installing / Using the App Locally

Clone the repository and run

```shell
cd visualizemybookshelf
python3.9 -m venv vmb-env
source vmb-env/bin/activate
pip install -r requirements.txt
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

After the script above ends, a secret key will be outputted. This is your Django secret key. Do not push it into version control.
Create a file called `.env` and in it type the following:

```
SECRET_KEY = <your secret key from the previous step>
DEBUG = true
```

DEBUG is set to true in the development environment. Don't do this in production.

Then in the terminal type:

```
python3 manage.py migrate
python3 manage.py runserver
```

Then navigate to http://127.0.0.1:8000/ in your browser and you should be good to go

## Brief Intro to Site Navigation

### You'll first encounter a login page. Click on the "registration" link.
<table><tr><td>
<img width="1439" alt="Screen Shot 2022-08-07 at 12 55 07" src="https://user-images.githubusercontent.com/27603465/183274728-8b5927ba-2377-4a6b-b151-df221af97569.png">
</td></tr></table>

### Register a user account and then login
<table><tr><td>
<img width="1440" alt="Screen Shot 2022-08-07 at 12 55 45" src="https://user-images.githubusercontent.com/27603465/183274759-87cc9bd1-fae4-4341-8ac3-bccf55e73a6e.png">
</td></tr></table>

### Upon login, you'll be presented with your empty bookshelf. Type the title of a book you would like to add to your bookshelf into the search bar. Then, click "search"
<table><tr><td>
<img width="1440" alt="Screen Shot 2022-08-07 at 13 29 53" src="https://user-images.githubusercontent.com/27603465/183275360-6071fe3a-2362-4eb7-a60c-b8d8e6815650.png">
</td></tr></table>

### The underlying information extraction algorithm will automatically search Wikipedia and the Google Books API based on the title you inputted and automatically extract relevant information about the book. The extraction procedure utilizes both rule-based extraction and a neural information extractor.

### If another user has already searched for this book before, some of the the book's information is already saved in Visualize My Bookshelf's database, so the saved information will be pulled from the database to avoid unnecessarily re-extracting the information.

The title and author of the book will then be displayed to you. If the title & author are correct, click "add" to add the book to your bookshelf. 
<table><tr><td><img width="1440" alt="Screen Shot 2022-08-07 at 13 02 48" src="https://user-images.githubusercontent.com/27603465/183275384-cef3db3b-d0ca-4761-a11c-04e9c7b9b04e.png">
</td></tr></table>


### Based on the information extracted, visualizations of your bookshelf will be auto-updated and you can view them by clicking the appropriate tab. For example, if you click into the "Genre" tab you can see the distribution of genres of the books you have read.
<table><tr><td>
<img width="1440" alt="Screen Shot 2022-08-07 at 13 03 25" src="https://user-images.githubusercontent.com/27603465/183274866-70febe39-7d98-43fa-86ae-f22db8a1222a.png">
</td></tr></table>


### TODO:
- Proper error handling and unit testing
- UI/aesthetical improvements
- improvements in both the speed and accuracy of the automatic information extraction algorithm
- increase in the variety of supported bookshelf visualizations & summarizations
- CI/CD
- auto importing of bookshelf data from Goodreads

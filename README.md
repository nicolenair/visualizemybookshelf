# Visualize My Bookshelf

Web app for automatically extracting and visualizing data about the books a user has read.

## Installing / Getting Started Locally

Clone the repository and run

```shell
python3 -m venv vmb-env
source vmb-env/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

And you should be good to go

## Brief Intro to Site Navigation

### You'll first encounter a login page. Click on the "registration" link.
<table><tr><td>
<img width="1439" alt="Screen Shot 2022-08-07 at 12 55 07" src="https://user-images.githubusercontent.com/27603465/183274728-8b5927ba-2377-4a6b-b151-df221af97569.png">
</td></tr></table>

### Register a user account
<table><tr><td>
<img width="1440" alt="Screen Shot 2022-08-07 at 12 55 45" src="https://user-images.githubusercontent.com/27603465/183274759-87cc9bd1-fae4-4341-8ac3-bccf55e73a6e.png">
</td></tr></table>

### Upon login, you'll be presented with an empty bookshelf. Type the title of a book you would like to add to your bookshelf into the search bar. Then, click "search"
<table><tr><td>
<img width="1439" alt="Screen Shot 2022-08-07 at 12 56 39" src="https://user-images.githubusercontent.com/27603465/183274781-564d47d0-d35a-413f-bb22-fe882f3dddcb.png">
</td></tr></table>

### The underlying information extraction algorithm will automatically search Wikipedia and the Google Books API based on the title you inputted and automatically extract relevant information about the book. The extraction procedure utilizes both rule-based extraction and a neural information extractor.

The title and author of the book will then be displayed to you. If the title & author are correct, click "add" to add the book to your bookshelf. 
<table><tr><td>
<img width="1440" alt="Screen Shot 2022-08-07 at 13 02 48" src="https://user-images.githubusercontent.com/27603465/183274793-9a505981-b937-47cc-8279-7d11ab99451a.png">
</td></tr></table>


### Based on the information extracted from the web, visualizations of your bookshelf will be auto-updated and you can view them by clicking the appropriate tab. For example, if you click into the "Genre" tab you can see the distribution of genres the books you have read.
<table><tr><td>
<img width="1440" alt="Screen Shot 2022-08-07 at 13 03 25" src="https://user-images.githubusercontent.com/27603465/183274866-70febe39-7d98-43fa-86ae-f22db8a1222a.png">
</td></tr></table>


This is a work in progress, so bear in mind that proper error handling and unit testing hasn't been done but is high on the priority list!



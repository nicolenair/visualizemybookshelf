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

## Brief Intro to Navigation

You'll first encounter a login page. Click on the "registration" link.
<img width="1439" alt="Screen Shot 2022-08-07 at 12 55 07" src="https://user-images.githubusercontent.com/27603465/183274728-8b5927ba-2377-4a6b-b151-df221af97569.png">

Register a user account
<img width="1440" alt="Screen Shot 2022-08-07 at 12 55 45" src="https://user-images.githubusercontent.com/27603465/183274759-87cc9bd1-fae4-4341-8ac3-bccf55e73a6e.png">

You'll be presented with an empty bookshelf. Type in the search bar to search for a book to add to your bookshelf. Click "search"
<img width="1440" alt="Screen Shot 2022-08-07 at 13 02 48" src="https://user-images.githubusercontent.com/27603465/183274793-9a505981-b937-47cc-8279-7d11ab99451a.png">

The underlying information extraction algorithm will automatically search the web and extract relevant info about your book and add it to your local SQL database.
<img width="1439" alt="Screen Shot 2022-08-07 at 12 56 39" src="https://user-images.githubusercontent.com/27603465/183274781-564d47d0-d35a-413f-bb22-fe882f3dddcb.png">

Based on the extracted information, visualizations of your bookshelf will be auto-updated and you can view them by clicking the appropriate tab. 
For example, if you click into the "Genre" tab you can see the distribution of genres the books you have read.
<img width="1440" alt="Screen Shot 2022-08-07 at 13 03 25" src="https://user-images.githubusercontent.com/27603465/183274866-70febe39-7d98-43fa-86ae-f22db8a1222a.png">


This is a work in progress, so bear in mind that proper error handling and unit testing hasn't been done but is high on the priority list!



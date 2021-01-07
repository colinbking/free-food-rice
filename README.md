# THIS IS NOT A FINISHED PROJECT YET

# wtf-rice
WTF(wheres the food) is a desktop app that detects free food events and automatically adds them to your calendar for your mooching pleasure.

# What does it do? And how?
WTF uses selenium to scrape postings from your desired facebook group that posts way too often and is annoying to go through manually. It extracts the important info like location, date, what free food is present, uses a simple classifier to determine if free food is present or not, and then writes it to a Postgres heroku server so other people using WTF can enjoy the free food event you found on your group, too. It then adds the free food opportunity in your group, as well as all the others in the database, to your google calendar automatically.  

## Installation
run "pip install requirements.txt"
add a .env with environment variables as follows:
FBNUM: facebook username
PWD: facebook password
SITE: your residential college group facebook page url


## Usage
just run "python main.py" (or python3 depending on your path to your installation of python3)



## License
[MIT](https://choosealicense.com/licenses/mit/)
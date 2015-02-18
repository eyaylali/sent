import model
from model import Ticket, Customer, session
import datetime
from zdesk import Zendesk
import os
import json
import sys

zendesk = Zendesk('https://sent.zendesk.com', os.environ["EMAIL"], os.environ["PASSWORD"])

print zendesk.tickets_list()
print zendesk.users_list()


def load_users(session):
    with open('seed_data/u.user', 'rb') as user_file:
        reader = csv.reader(user_file, delimiter='|')
        for row in reader:
            user = User(id=row[0], age=row[1], zipcode=row[4])
            session.add(user)
    session.commit()

def load_tickets(session):
    with open('seed_data/u.item', 'rb') as movie_file:
        reader = csv.reader(movie_file, delimiter='|')
        for row in reader:
            title = row[1]
            title = title.decode("latin-1")
            new_title = title[:-6]
            new_title = new_title.rstrip()
            if row[2] != '':
                date = datetime.datetime.strptime(row[2], "%d-%b-%Y")
            else:
                date = None
            movie = Movie(id=row[0], title=new_title, release_date=date, imdb_url=row[4])
            session.add(movie)
    session.commit()

def load_ratings(session):
    with open('seed_data/u.data', 'rb') as ratings_file:
        reader = csv.reader(ratings_file, delimiter='\t')
        for row in reader:
            rating = Rating(user_id=row[0], movie_id=row[1], rating=row[2])
            session.add(rating)
    session.commit()


def main(session):
    load_users(session)
    load_movies(session)
    load_ratings(session)
    

if __name__ == "__main__":
    main(session)
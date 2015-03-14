from zdesk import Zendesk
from tokenizer import tokenize_text
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
import model
from model import Ticket, User, session
from datetime import datetime, date
import os
import sys
from sklearn.externals import joblib
from train import train
import pickle
import numpy as np
 
zendesk = Zendesk("https://sent.zendesk.com", os.environ["EMAIL"], os.environ["PASSWORD"])

USERS = zendesk.users_list()
ORGANIZATIONS = zendesk.organizations_list()
print ORGANIZATIONS

# load the saved pipeline that includes vectorizer & classifier
classifier = joblib.load('train/classifier.pickle')
last_update = pickle.load(open('last_update_time.p', 'rb'))
today = datetime.now()

sentiment_changed_tickets = Ticket.list_changed_tickets(today)
def learn_new_data():
	X_data = []
	y_labels = []
	for ticket in sentiment_changed_tickets:
		ticket_title = ticket.subject
		ticket_content = ticket.content
		ticket_label = ticket.sentiment_label
		all_content = ticket_title + ticket_content
		X_data.append(all_content)
		y_labels.append(ticket_label)
	X_data = np.array(X_data)
	y_labels = np.array(y_labels)
	classes = np.array(["positive", "upset", "neutral"])
	classifier.partial_fit(X_data, y_labels, classes)
	pickle.dump(today, open('last_update_time.p', 'wb'))


def unpack_zendesk_users_tickets(session, user_dict, org_dict):
	existing_users = User.list_user_ids()
	for user in user_dict["users"]:
		#check to see if ticket author is already in database
		zendesk_user_id = int(user["id"])
		if zendesk_user_id not in existing_users:
			role = user["role"]
			name = user["name"]
			email = user["email"]
			organization_id = user["organization_id"]
			if organization_id:
				for organization in org_dict["organizations"]:
					if organization["id"] == organization_id:
						organization_name = organization["name"]
			else:
				organization_name = None

			user = model.User(zendesk_user_id = zendesk_user_id, role = role, name = name, email = email, organization_name = organization_name)
			session.add(user)
			session.commit()
			session.refresh(user)

		user_tickets = zendesk.user_tickets_requested(zendesk_user_id)
		print user_tickets
		#Find the last ticket id of messages already in DB in order to determine which messages to add (ticket ids increment by 1)
		# threshold_id = Ticket.query.order_by(Ticket.ticket_id).first()
		added_tickets = []
		for ticket in user_tickets["tickets"]:
			if ticket["status"] == "open" or ticket["status"] == "pending":
				ticket_id = int(ticket["id"])

				#if the ticket_id of the ticket to be added is less than or equal to the threshold, don't add it
				# if threshold_id:
				# 	if ticket_id not in added_tickets:
				# 		if ticket_id <= threshold_id:
				# 			continue
				if ticket_id in added_tickets:
					continue


				subject = ticket["subject"]
				content = ticket["description"]
				all_content = subject + " " + content
				user_id = int(ticket["requester_id"])
				submitter_id = int(ticket["submitter_id"])
				assignee_id = int(ticket["assignee_id"])
				source = ticket["via"]["channel"]
				if source == "twitter":
					priority = 1
				else:
					priority = 2
				timestamp = datetime.strptime(ticket["created_at"], "%Y-%m-%dT%H:%M:%SZ")
				status = ticket["status"]
				label = predict_sentiment_label(all_content)
				
				ticket = model.Ticket(ticket_id = ticket_id, 
									  user_id = user_id, 
									  submitter_id = submitter_id, 
									  assignee_id = assignee_id, 
									  timestamp = timestamp,
									  subject = subject, 
									  content = content, 
									  status = status, 
									  source = source,
									  priority = priority, 
									  sentiment_label = label,
									  update_date = update_date)
				session.add(ticket)
				session.commit()
				session.refresh(ticket)
				added_tickets.append(ticket_id)

def predict_sentiment_label(all_content):
	label = train.predict(classifier, [all_content])
	return label[0]

def main(session):
	unpack_zendesk_users_tickets(session, USERS, ORGANIZATIONS)
    
if __name__ == "__main__":
	main(session)
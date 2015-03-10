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
 
zendesk = Zendesk("https://sent.zendesk.com", os.environ["EMAIL"], os.environ["PASSWORD"])
TICKETS = zendesk.tickets_list()
USERS = zendesk.users_list()
ORGANIZATIONS = zendesk.organizations_list()

# load the saved pipeline that includes vectorizer & classifier
classifier = joblib.load('train/classifier.pickle')

def unpack_zendesk_users_tickets(session, user_dict, org_dict):
	for user in user_dict["users"]:
		zendesk_user_id = int(user["id"])
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
		for ticket in user_tickets["tickets"]:
			if ticket["status"] == "open" or ticket["status"] == "pending":
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
				ticket_id = int(ticket["id"])
				url = ticket["url"]
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
									  url = url, 
									  source = source,
									  priority = priority, 
									  sentiment_label = label)
				session.add(ticket)

		session.commit()

def predict_sentiment_label(all_content):
	label = train.predict(classifier, [all_content])
	return label[0]

def main(session):
	unpack_zendesk_users_tickets(session, USERS, ORGANIZATIONS)
    
if __name__ == "__main__":
	main(session)

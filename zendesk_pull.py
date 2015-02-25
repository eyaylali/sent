from zdesk import Zendesk
from tokenizer import tokenize_text, bag_of_words
import model
from model import Ticket, User, session
from datetime import datetime
import os
import sys

zendesk = Zendesk("https://sent.zendesk.com", os.environ["EMAIL"], os.environ["PASSWORD"])
TICKETS = zendesk.tickets_list()
USERS = zendesk.users_list()

def unpack_zendesk_users_tickets(session, dict_input, dict_input2):
	for user in dict_input["users"]:
		zendesk_user_id = int(user["id"])
		role = user["role"]
		name = user["name"]
		details = user["details"]
		email = user["email"]
		phone = user["phone"]
		url = user["url"]
		time_zone = user["time_zone"]
		notes = user["notes"]

		user = model.User(zendesk_user_id = zendesk_user_id, role = role, name = name, email = email, url = url, notes = notes, time_zone = time_zone, phone = phone, details = details)
		session.add(user)
		session.commit()
		session.refresh(user)

		user_tickets = zendesk.user_tickets_requested(zendesk_user_id)
		for ticket in dict_input2["tickets"]:
			if ticket["status"] == "open" or "pending":
				tokenized_subject = tokenize_text(ticket["subject"]))
				tokenized_content = tokenize_text(ticket["description"]))
				subject = ticket["subject"]
				content = ticket["description"]
				submitter_id = int(ticket["submitter_id"])
				assignee_id = int(ticket["assignee_id"])
				source = ticket["via"]["channel"]
				timestamp = datetime.strptime(ticket["created_at"], "%Y-%m-%dT%H:%M:%SZ")
				ticket_id = int(ticket["id"])
				url = ticket["url"]
				status = ticket["status"]

				ticket = model.Ticket(ticket_id = ticket_id, submitter_id = submitter_id, assignee_id = assignee_id, timestamp = timestamp, subject = subject, content = content, status = status, url = url, source = source, tokenized_subject = tokenized_subject, tokenized_content = tokenized_content)
				session.add(ticket)
		session.commit()

def main(session):
    unpack_zendesk_users_tickets(session, USERS, TICKETS)
    
if __name__ == "__main__":
	main(session)


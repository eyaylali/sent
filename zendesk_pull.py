from zdesk import Zendesk
from tokenizer import tokenize_text
import model
from model import Ticket, Customer, session
import datetime
import os
import sys

zendesk = Zendesk("https://sent.zendesk.com", os.environ["EMAIL"], os.environ["PASSWORD"])
TICKETS = zendesk.tickets_list()
USERS = zendesk.users_list()

def unpack_zendesk_users_tickets(session, dict_input):
	for user in dict_input["users"]:
		zendesk_customer_id = int(user["id"])
		role = user["role"]
		name = user["name"]
		details = user["details"]
		email = user["email"]
		phone = user["phone"]
		url = user["url"]
		time_zone = user["time_zone"]
		notes = user["notes"]

		user = model.User(zendesk_customer_id = zendesk_customer_id, role = role, name = name, email = email, url = url, notes = notes, time_zone = time_zone, phone = phone, details = details)
		session.add(user)
		session.commit()
		session.refresh(User)

		user_tickets = zendesk.user_tickets_requested(zendesk_customer_id)
		for ticket in dict_input["tickets"]:
			if ticket["status"] == "open" or "pending":
				subject = tokenize_text(ticket["subject"])
				content = tokenize_text(ticket["description"])
				submitter_id = int(ticket["submitter_id"])
				zendesk_customer_id = int(ticket["requester_id"]) #might not need to record again
				assignee_id = int(ticket["assignee_id"])
				source = ticket["via"]["channel"]
				timestamp = datetime.datetime.strptime(ticket["created_at"], "%Y-%m-%d")
				ticket_id = int(ticket["id"])
				url = ticket["url"]
				status = ticket["status"]

				ticket = model.Ticket(ticket_id = ticket_id, customer_id = BLAH, submitter_id = submitter_id, zendesk_customer_id = zendesk_customer_id, assignee_id = assignee_id, timestamp = timestamp, subject = subject, content = content, status = status, url = url, source = source)
				session.add(ticket)
				session.commit()




def main(session):
    unpack_zendesk_tix_tokenize(session, TICKETS)
    unpack_zendesk_users(session, USERS)
    
if __name__ == "__main__":
	main(session)


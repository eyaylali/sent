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

def unpack_zendesk_tix_tokenize(session, dict_input):
	for ticket in dict_input["tickets"]:
		if ticket["status"] == "open" or "pending":
			subject = tokenize_text(ticket["subject"])  #.encode('ascii','ignore')
			content = tokenize_text(ticket["description"])
			submitter_id = ticket["submitter_id"]
			customer_id = ticket["requester_id"]
			assignee_id = ticket["assignee_id"]
			source = ticket["via"]["channel"]
			timestamp = ticket["created_at"]
			ticket_id = ticket["id"]
			url = ticket["url"]
			status = ticket["status"]

			ticket = model.Ticket(ticket_id = int(ticket_id), submitter_id = submitter_id, customer_id = int(customer_id), assignee_id = int(assignee_id), timestamp = timestamp, subject = subject, content = content, status = status, url = url, source = source)
			session.add(ticket)
	session.commit()	

def unpack_zendesk_users(session, dict_input):
	for user in dict_input["users"]:
		customer_id = user["id"]
		role = user["role"]
		name = user["name"]
		details = user["details"]
		email = user["email"]
		phone = user["phone"]
		url = user["url"]
		time_zone = user["time_zone"]
		notes = user["notes"]

		user = model.User(customer_id = int(customer_id), role = role, name = name, email = email, url = url, notes = notes, time_zone = time_zone, phone = phone, details = details)
		session.add(user)
	session.commit()

	# session.refresh(user)




def main(session):
    unpack_zendesk_tix_tokenize(session, TICKETS)
    unpack_zendesk_users(session, USERS)
    
if __name__ == "__main__":
	main(session)

# print zendesk.user_tickets_requested(797980458)


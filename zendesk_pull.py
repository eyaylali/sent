from zdesk import Zendesk
from tokenizer import tokenize_text
import model
from model import Ticket, User, session
from datetime import datetime
import os
import sys

zendesk = Zendesk("https://sent.zendesk.com", os.environ["EMAIL"], os.environ["PASSWORD"])
TICKETS = zendesk.tickets_list()
USERS = zendesk.users_list()
ORGANIZATIONS = zendesk.organizations_list()

# user_tickets = zendesk.user_tickets_requested(789440538)
# print user_tickets

def unpack_zendesk_users_tickets(session, dict_input):
	for user in dict_input["users"]:
		zendesk_user_id = int(user["id"])
		role = user["role"]
		name = user["name"]
		email = user["email"]
		organization_id = user["organization_id"]

		user = model.User(zendesk_user_id = zendesk_user_id, role = role, name = name, email = email, organization_id = organization_id)
		session.add(user)
		session.commit()
		session.refresh(user)

		user_tickets = zendesk.user_tickets_requested(zendesk_user_id)
		for ticket in user_tickets["tickets"]:
			if ticket["status"] == "open" or ticket["status"] == "pending":
				subject = ticket["subject"]
				content = ticket["description"]
				submitter_id = int(ticket["submitter_id"])
				assignee_id = int(ticket["assignee_id"])
				source = ticket["via"]["channel"]
				timestamp = datetime.strptime(ticket["created_at"], "%Y-%m-%dT%H:%M:%SZ")
				ticket_id = int(ticket["id"])
				url = ticket["url"]
				status = ticket["status"]

				ticket = model.Ticket(ticket_id = ticket_id, submitter_id = submitter_id, assignee_id = assignee_id, timestamp = timestamp, subject = subject, content = content, status = status, url = url, source = source)
				session.add(ticket)
		session.commit()

def unpack_zendesk_organizations(session, dict_input):
	for organization in dict_input["organizations"]:
		zendesk_org_id = organization["id"]
		name = organization["name"]
		tags = organization["tags"]

		organization = model.Organization(zendesk_org_id = zendesk_org_id, name = name, tags = tags)
		session.add(organization)
	session.commit()


def main(session):
    unpack_zendesk_users_tickets(session, USERS)
    unpack_zendesk_organizations(session, ORGANIZATIONS)
    
if __name__ == "__main__":
	main(session)


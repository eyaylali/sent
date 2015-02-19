from zdesk import Zendesk
import os
import json
import sys
from tokenizer import tokenize_text

zendesk = Zendesk("https://sent.zendesk.com", os.environ["EMAIL"], os.environ["PASSWORD"])
TICKETS = zendesk.tickets_list()
USERS = zendesk.users_list()
all_tokenized_reviews_dict = {}

def unpack_zendesk(dict1):
	for ticket in dict1["tickets"]:
		if ticket["status"] == "open" or "pending":
			subject = tokenize_text(ticket["subject"])  #.encode('ascii','ignore')
			content = tokenize_text(ticket["description"])
			customer_id = ticket["submitter_id"]
			assignee_id = ticket["assignee_id"]
			source = ticket["via"]["channel"]
			timestamp = ticket["created_at"]
			ticket_id = ticket["id"]

			tokenized_dict = {"Author ID":customer_id, "Assignee ID": assignee_id, "Timestamp": timestamp, "Source": source, "Subject": subject, "Content":content}
			all_tokenized_reviews_dict[ticket_id] = tokenized_dict

	return all_tokenized_reviews_dict


print unpack_zendesk(TICKETS)




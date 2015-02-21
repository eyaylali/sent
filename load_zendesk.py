from zdesk import Zendesk
import json
from sys import argv
import os

zendesk = Zendesk('https://sent.zendesk.com', os.environ["EMAIL"], os.environ["PASSWORD"])

#create
new_ticket = {
    'ticket': {
    	# 'source':{'channel': 'api'}
        'requester':{'name': 'Ms. Example','email': 'example@customer.com'},
        'subject':'help! i am upset',
        'comment': {'body':'test'}
    }
}

result = zendesk.ticket_create(data=new_ticket)

def main(jsonfile):
	precontent = open(jsonfile).read()
	content = json.loads(precontent)
	# jsonfile.close()

	for review in content["Reviews"]:
		new_ticket["ticket"]["requester_name"] = review["Author"].encode('ascii','ignore')
		new_ticket["ticket"]["requester_email"] = "customer@email.com"
		new_ticket["ticket"]["subject"] = review["Title"].encode('ascii','ignore')
		new_ticket["ticket"]["comment"]["body"] = review["Content"].encode('ascii','ignore')
		#how to set the date from the json files

		# Create the ticket and get its URL
		result = zendesk.ticket_create(data=new_ticket)


if __name__ == "__main__":
    input_file_1 = argv[1]
    main(input_file_1)

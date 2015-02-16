from zdesk import Zendesk, get_id_from_url
import json
from sys import argv
import os

zendesk = Zendesk('https://sent.zendesk.com', os.environ["EMAIL"], os.environ["PASSWORD"])


#list
# zendesk.ticket_list()

#create
new_ticket = {
    'ticket': {
        'requester_id':9999,
        # 'recipient': 'howard@starbucks.com',
        'subject':'help! i am upset',
        'comment': {'body':'test'}
    }
}

result = zendesk.ticket_create(data=new_ticket)

# def main(file):
# 	precontent = open(jsonfile).read()
# 	content = json.loads(precontent)

# 	for review in content["Reviews"]:
# 		new_ticket["ticket"]["requester_name"] = review["Author"].encode('ascii','ignore')
# 		new_ticket["ticket"]["requester_email"] = "customer@email.com"
# 		new_ticket["ticket"]["subject"] = review["Title"].encode('ascii','ignore')
# 		new_ticket["ticket"]["comment"]["body"] = review["Content"].encode('ascii','ignore')

# 		# Create the ticket and get its URL
# 		result = zendesk.ticket_create(data=new_ticket)

# 	jsonfile.close()

# if __name__ == "__main__":
#     input_file_1 = argv[1]
#     main(input_file_1)

# # Show
# zendesk.ticket_show(id=ticket_id)
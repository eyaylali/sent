from zdesk import Zendesk
import json
from sys import argv
import os

zendesk = Zendesk('https://sent.zendesk.com', os.environ["EMAIL"], os.environ["PASSWORD"])

def main(jsonfile):
	precontent = open(jsonfile).read()
	content = json.loads(precontent)
	# jsonfile.close()

	for review in content["Reviews"]:

		new_ticket = {
	    	"ticket": {
	        "requester": {"name": review["Author"].encode('ascii','ignore'), "email": "name@gmail.com.com"},
	        "subject": review["Title"].encode('ascii','ignore'),
	        "comment": {"body":review["Content"].encode('ascii','ignore')}
    }
}
		# Create the ticket and get its URL
		result = zendesk.ticket_create(data=new_ticket)


if __name__ == "__main__":
    input_file_1 = argv[1]
    main(input_file_1)

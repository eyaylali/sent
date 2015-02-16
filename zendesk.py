from zdesk import Zendesk, get_id_from_url

zendesk = Zendesk('https://sent.zendesk.com', 'yaylalierin@gmail.com', 'sentzendesk')


#list
zendesk.ticket_list()

#create
new_ticket = {
    'ticket': {
        'requester_name': 'Howard Schultz',
        'requester_email': 'howard@starbucks.com',
        'subject':'My Starbucks coffee is cold!',
        'description': 'please reheat my coffee',
        'set_tags': 'coffee drinks',
        'ticket_field_entries': [
            {
                'ticket_field_id': 1,
                'value': 'venti'
            },
            {
                'ticket_field_id': 2,
                'value': '$10'
            }
        ]
    }
}
# Create the ticket and get its URL
result = zendesk.ticket_create(data=new_ticket)

# # Show
# zendesk.ticket_show(id=ticket_id)

# # Delete
# zendesk.ticket_delete(id=ticket_id)
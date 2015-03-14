from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

ENGINE = create_engine("sqlite:///senti.db", echo=False)
session = scoped_session(sessionmaker(bind=ENGINE,
									  autocommit = False,
									  autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class Ticket(Base):
	__tablename__ = "tickets"

	id = Column(Integer, primary_key = True)
	ticket_id = Column(Integer)
	user_id = Column(Integer, ForeignKey('users.zendesk_user_id'))
	submitter_id = Column(Integer)
	assignee_id = Column(Integer)
	timestamp = Column(DateTime)
	subject = Column(String(200))
	content = Column(String(3000))
	status = Column(String(64))
	source = Column(String(64))
	priority = Column(Integer)
	sentiment_label = Column(String(64))
	# update_date = Column(DateTime)

	user = relationship("User", backref=backref("tickets", order_by=id))

	@classmethod
	def list_changed_tickets(cls, update_date):
		all_changed_tickets = cls.query.filter(Ticket.update_date > update_date).all()
		return all_changed_tickets

	def __repr__(self):
		# return "<User: id=%d, email=%s, password=%s, age=%d, zipcode=%s>" % (self.id, self.email, self.password, self.age, self.zipcode)
		pass

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	zendesk_user_id = Column(Integer)
	role = Column(String(64))
	name = Column(String(100))
	email = Column(String(100))
	organization_name = Column(String, nullable = True)

	@classmethod
	def sum_tickets_by_org_name(cls, org_param, time_param, label):
		if label == "total":
			return len(cls.query.filter_by(organization_name=org_param).join(Ticket).filter(Ticket.timestamp > time_param).all())
		else:
			return len(cls.query.filter_by(organization_name=org_param).join(Ticket).filter(Ticket.timestamp > time_param, Ticket.sentiment_label == label).all())

	@classmethod
	def list_user_ids(cls):
		all_users = cls.query.all()
		return [user.zendesk_user_id for user in all_users]

	@classmethod
	def list_user_organizations(cls):
		all_users = cls.query.all()
		return set([user.organization_name for user in all_users])


	def __repr__(self):
		# return "<User: id=%d, email=%s, password=%s, age=%d, zipcode=%s>" % (self.id, self.email, self.password, self.age, self.zipcode)
		return "This is a user"

### End class declarations

def main():
	Base.metadata.create_all(bind=ENGINE)
	pass
	

if __name__ == "__main__":
	main()
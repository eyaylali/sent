from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

ENGINE = create_engine("sqlite:///sent.db", echo=False)
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
	month = Column(Integer)
	week = Column(Integer)
	day_of_week = Column(Integer)
	subject = Column(String(200))
	content = Column(String(3000))
	status = Column(String(64))
	url = Column(String(300))
	source = Column(String(64))
	priority = Column(Integer)
	sentiment_label = Column(String(64))

	user = relationship("User", backref=backref("tickets", order_by=id))

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

	# organization = relationship("Organization", backref=backref("users", order_by=id))

	def __repr__(self):
		# return "<User: id=%d, email=%s, password=%s, age=%d, zipcode=%s>" % (self.id, self.email, self.password, self.age, self.zipcode)
		pass

# class Organization(Base):
# 	__tablename__ = "organizations"

# 	id = Column(Integer, primary_key = True)
# 	zendesk_org_id = Column(Integer)
# 	name = Column(String(100))

# 	def __repr__(self):
# 		# return "<User: id=%d, email=%s, password=%s, age=%d, zipcode=%s>" % (self.id, self.email, self.password, self.age, self.zipcode)
# 		pass

### End class declarations

def main():
	Base.metadata.create_all(bind=ENGINE)
	pass
	

if __name__ == "__main__":
	main()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine("sqlite:///sent.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
									  autocommit = False,
									  autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class Ticket(Base):
	__tablename__ = "tickets"

	id = Column(Integer, primary_key = True)
	ticket_id = Column(Integer, nullable = False)
	customer_id = Column(Integer, ForeignKey('users.id'), nullable = False)
	submitter_id = Column(Integer, nullable = False)
	zendesk_customer_id = Column(Integer, nullable = False)
	assignee_id = Column(Integer, nullable = False)
	timestamp = Column(DateTime, nullable = False)
	subject = Column(String(200), nullable = False)
	content = Column(String(3000), nullable = False)
	status = Column(String(64), nullable = True)
	url = Column(String(300), nullable = False)
	source = Column(String(64), nullable = True)

	customer = relationship("User", backref=backref("tickets", order_by=id))

	def __repr__(self):
		# return "<User: id=%d, email=%s, password=%s, age=%d, zipcode=%s>" % (self.id, self.email, self.password, self.age, self.zipcode)
		pass

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	zendesk_customer_id = Column(Integer, nullable = False)
	role = Column(String(64), nullable = False)
	name = Column(String(100), nullable = False)
	email = Column(String(100), nullable = False)
	url = Column(String(300), nullable = False)
	notes = Column(String(1000), nullable = True)
	time_zone = Column(String(64), nullable = False)
	phone = Column(String(64), nullable = False)
	details = Column(String(1000), nullable = True)

	def __repr__(self):
		# return "<User: id=%d, email=%s, password=%s, age=%d, zipcode=%s>" % (self.id, self.email, self.password, self.age, self.zipcode)
		pass

### End class declarations

def main():
	"""In case we need this for something"""
	pass

if __name__ == "__main__":
	main()
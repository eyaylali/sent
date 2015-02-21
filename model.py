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
	user_id = Column(Integer, ForeignKey('users.id'))
	submitter_id = Column(Integer)
	assignee_id = Column(Integer)
	timestamp = Column(DateTime)
	subject = Column(String(200))
	content = Column(String(3000))
	tokenized_subject = Column(PickleType)
	tokenized_content = Column(PickleType)
	status = Column(String(64))
	url = Column(String(300))
	source = Column(String(64))

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
	url = Column(String(300))
	notes = Column(String(1000), nullable = True)
	time_zone = Column(String(64))
	phone = Column(String(64), nullable = True)
	details = Column(String(1000), nullable = True)

	def __repr__(self):
		# return "<User: id=%d, email=%s, password=%s, age=%d, zipcode=%s>" % (self.id, self.email, self.password, self.age, self.zipcode)
		pass

### End class declarations

def main():
	Base.metadata.create_all(bind=ENGINE)
	pass
	

if __name__ == "__main__":
	main()
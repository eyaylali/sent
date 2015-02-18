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

    ticket_id = Column(Integer, primary_key = True, nullable = False)
    submitter_id = Column(Integer, nullable = False)
    requester_id = Column(Integer, nullable = False, ForeignKey('customers.id'))
    assignee_id = Column(Integer, nullable = False)
    created_at = Column(DateTime, nullable = False)
	subject = Column(String(200), nullable = False)
	description = Column(String(3000), nullable = False)
    priority = Column(String(64), nullable = True)
    status = Column(String(64), nullable = True)
    url = Column(String(300), nullable = False)

    customer = relationship("Customer", backref=backref("tickets", order_by=id))

    def __repr__(self):
        # return "<User: id=%d, email=%s, password=%s, age=%d, zipcode=%s>" % (self.id, self.email, self.password, self.age, self.zipcode)
        pass

class Customer(Base):
	__tablename__ = "customers"

	id = Column(Integer, primary_key = True, nullable = False)
    role = Column(String(64), nullable = False)
    name = Column(String(100), nullable = False)
	email = Column(String(100), nullable = False)
	url = Column(String(300), nullable = False)
    notes = Column(String(1000), nullable = True)

    def __repr__(self):
        # return "<User: id=%d, email=%s, password=%s, age=%d, zipcode=%s>" % (self.id, self.email, self.password, self.age, self.zipcode)
        pass

### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
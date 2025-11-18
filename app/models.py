# from enum import unique
# from pickle import TRUE
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql.expression import text
# from sqlalchemy.sql.schema import ForeignKey
# from sqlalchemy.sql.sqltypes import TIMESTAMP, TIME, DATE
# from database import Base
# from sqlalchemy import Column, Integer, Boolean,String, Float, JSON, Text
# from sqlalchemy.sql import func



# # class User(Base):
# #     __tablename__ = "User" 

# #     id = Column(Integer, primary_key=True, nullable = False)
# #     email = Column(String(128), nullable = False, unique=True)
# #     password = Column(String(1024), nullable = False)
# #     first_name = Column(String(1024), nullable = False)
# #     last_name = Column(String(1024), nullable = True)
# #     username = Column(String(1024), nullable = False)
# #     mobile = Column(String(1024), nullable = True)
# #     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
# #     updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
# #     country = Column(String(255), nullable=False)
# #     city = Column(String(255), nullable=False) 
# #     role = relationship('Role', secondary='UserRole')
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

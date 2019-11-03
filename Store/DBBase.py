from sqlalchemy.ext.declarative import declarative_base

# define this as the base for all the DB tables here in a common module
BasePostgres = declarative_base()
BaseSQLite = declarative_base()

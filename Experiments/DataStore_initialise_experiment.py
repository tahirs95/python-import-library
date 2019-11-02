from Store.DataStoreModule import DataStore
from Resolvers.CommandLineResolver import CommandLineResolver

# data_store = DataStore("", "", "", 0, "sqlite_datastore.db", db_type='sqlite',
#                        missing_data_resolver=CommandLineResolver())
# data_store.initialise()


data_store_postgres = DataStore("postgres", "postgres", "localhost", 5432, "postgres")
data_store_postgres.initialise()

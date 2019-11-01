from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from importlib import import_module
from contextlib import contextmanager

from Store.DBBase import Base
from Store.DBStatus import TableTypes
from Resolvers.DefaultsResolver import DefaultsResolver

# TODO: add foreign key refs
# TODO: add proper uuid funcs that interact with entries table

# TODO: probably move this module to the top level as it's the main one


class DataStore:

    # TODO: supply or lookup user id
    # Valid options for db_type are 'postgres' and 'sqlite'
    def __init__(self, db_username, db_password, db_host, db_port, db_name, db_type='postgres', missing_data_resolver=DefaultsResolver()):
        if db_type == 'postgres':
            self.DBClasses = import_module('Store.PostgresDB')
            driver = 'postgresql+psycopg2'
        elif db_type == 'sqlite':
            self.DBClasses = import_module('Store.SqliteDB')
            driver = 'sqlite+pysqlite'
        else:
            raise Exception(f"Unknown db_type {db_type} supplied, if specified should be one of 'postgres' or 'sqlite'")

        # setup table type data
        self.setupTabletypeMap()

        connectionString = '{}://{}:{}@{}:{}/{}'.format(driver, db_username, db_password, db_host, db_port, db_name)
        self.engine = create_engine(connectionString, echo=False)
        Base.metadata.bind = self.engine

        self.missing_data_resolver = missing_data_resolver

        # caches of known data
        self.tableTypes = {}
        self.privacies = {}
        self.nationalities = {}
        self.datafileTypes = {}
        self.datafiles = {}
        self.platformTypes = {}
        self.platforms = {}
        self.sensorTypes = {}
        self.sensors = {}

        # TEMP list of values for defaulted IDs, to be replaced by missing info lookup mechanism
        self.defaultUserId = 1  # DevUser

        if db_type == 'sqlite':
            try:
                # Attempt to create schema if not present, to cope with fresh DB file
                Base.metadata.create_all(self.engine)
            except OperationalError:
                print("Error creating database schema, possible invalid path? ('" + db_name + "'). Quitting")
                exit()

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        try:
            yield self
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()


    #############################################################
    # Add functions

    def addTableType(self, tabletype_id, tablename):
        # check in cache for table type
        if tabletype_id in self.tableTypes:
            return self.tableTypes[tabletype_id]

        # doesn't exist in cache, try to lookup in DB
        tableTypeLookup = self.searchTableType(tabletype_id)
        if tableTypeLookup:
            # add to cache and return
            self.tableTypes[tabletype_id] = tableTypeLookup
            return tableTypeLookup

        # enough info to proceed and create entry
        tableTypeObj = self.DBClasses.TableType(
            tabletype_id=tabletype_id,
            name=tablename
        )
        self.session.add(tableTypeObj)
        self.session.flush()

        # add to cache and return created table type
        self.tableTypes[tabletype_id] = tableTypeObj
        # should return DB type or something else decoupled from DB?
        return tableTypeObj

    def addEntry(self, tabletypeId, tableName):
        # ensure table type exists to satisfy foreign key constraint
        self.addTableType(tabletypeId, tableName)

        # No cache for entries, just add new one when called
        entry_obj = self.DBClasses.Entry(
            tabletype_id=tabletypeId,
            created_user=self.defaultUserId
        )

        self.session.add(entry_obj)
        self.session.flush()

        return entry_obj.entry_id

    # TODO: add function to do common pattern of action in these functions
    def addPlatformType(self, platformTypeName):
        # check in cache for nationality
        if platformTypeName in self.platformTypes:
            return self.platformTypes[platformTypeName]

        # doesn't exist in cache, try to lookup in DB
        platformTypeLookup = self.searchPlatformType(platformTypeName)
        if platformTypeLookup:
            # add to cache and return looked up platform type
            self.platformTypes[platformTypeName] = platformTypeLookup
            return platformTypeLookup

        # enough info to proceed and create entry
        platformTypeObj = self.DBClasses.PlatformType(name=platformTypeName)
        self.session.add(platformTypeObj)
        self.session.flush()

        # add to cache and return created platform type
        self.platformTypes[platformTypeName] = platformTypeObj
        # should return DB type or something else decoupled from DB?
        return platformTypeObj

    def addNationality(self, nationalityName):
        # check in cache for nationality
        if nationalityName in self.nationalities:
            return self.nationalities[nationalityName]

        # doesn't exist in cache, try to lookup in DB
        nationalityLookup = self.searchNationality(nationalityName)
        if nationalityLookup:
            # add to cache and return looked up nationality
            self.nationalities[nationalityName] = nationalityLookup
            return nationalityLookup

        # enough info to proceed and create entry
        nationalityObj = self.DBClasses.Nationality(name=nationalityName)
        self.session.add(nationalityObj)
        self.session.flush()

        # add to cache and return created platform
        self.nationalities[nationalityName] = nationalityObj
        # should return DB type or something else decoupled from DB?
        return nationalityObj

    def addPrivacy(self, privacyName):
        # check in cache for privacy
        if privacyName in self.privacies:
            return self.privacies[privacyName]

        # doesn't exist in cache, try to lookup in DB
        privacyLookup = self.searchPrivacy(privacyName)
        if privacyLookup:
            # add to cache and return looked up platform
            self.privacies[privacyName] = privacyLookup
            return privacyLookup

        # enough info to proceed and create entry
        privacyObj = self.DBClasses.Privacy(name=privacyName)
        self.session.add(privacyObj)
        self.session.flush()

        # add to cache and return created platform
        self.privacies[privacyName] = privacyObj
        # should return DB type or something else decoupled from DB?
        return privacyObj

    def addDatafileType(self, datafile_type):
        # check in cache for datafile type
        if datafile_type in self.datafileTypes:
            return self.datafileTypes[datafile_type]

        # doesn't exist in cache, try to lookup in DB
        datafile_type_lookup = self.searchDatafileType(datafile_type)
        if datafile_type_lookup:
            # add to cache and return looked up datafile type
            self.datafileTypes[datafile_type] = datafile_type_lookup
            return datafile_type_lookup

        # proceed and create entry
        datafile_type_obj = self.DBClasses.DatafileType(
            name=datafile_type
        )

        self.session.add(datafile_type_obj)
        self.session.flush()

        # add to cache and return created datafile type
        self.datafileTypes[datafile_type] = datafile_type_obj
        # should return DB type or something else decoupled from DB?
        return datafile_type_obj

    def addDatafile(self, datafileName, datafileType):
        # check in cache for datafile
        if datafileName in self.datafiles:
            return self.datafiles[datafileName]

        # doesn't exist in cache, try to lookup in DB
        datafilelookup = self.searchDatafile(datafileName)
        if datafilelookup:
            # add to cache and return looked up datafile
            self.datafiles[datafileName] = datafilelookup
            return datafilelookup

        datafile_type_obj = self.addDatafileType(datafileType)

        # don't know privacy, use resolver to query for data
        missingPrivacyData = self.missing_data_resolver.resolvePrivacy(self, self.DBClasses.Datafile.tabletypeId, self.DBClasses.Datafile.__tablename__)

        # missingPrivacyData should contain (tabletype, privacyName)
        # enough info to proceed and create entry
        chosenTableType, chosenPrivacy = missingPrivacyData
        entry_id = self.addEntry(self.DBClasses.Datafile.tabletypeId, self.DBClasses.Datafile.__tablename__)

        datafile_obj = self.DBClasses.Datafile(
            datafile_id=entry_id,
            simulated=False,
            reference=datafileName,
            url=None,
            privacy_id=chosenPrivacy.privacy_id,
            datafiletype_id=datafile_type_obj.datafiletype_id
        )

        self.session.add(datafile_obj)
        self.session.flush()

        self.datafiles[datafileName] = datafile_obj
        # should return DB type or something else decoupled from DB?
        return datafile_obj

    def addPlatform(self, platformName):
        # check in cache for platform
        if platformName in self.platforms:
            return self.platforms[platformName]

        # doesn't exist in cache, try to lookup in DB
        platformlookup = self.searchPlatform(platformName)
        if platformlookup:
            # add to cache and return looked up platform
            self.platforms[platformName] = platformlookup
            return platformlookup

        # doesn't exist in DB, use resolver to query for data
        missingPlatformData = self.missing_data_resolver.resolvePlatform(self, platformName)

        # missingPlatformData should contain (platformName, chosenClass, chosenNationality)
        # enough info to proceed and create entry
        chosenPlatformName, chosenClass, chosenNationality = missingPlatformData
        entry_id = self.addEntry(self.DBClasses.Platform.tabletypeId, self.DBClasses.Platform.__tablename__)

        platform_obj = self.DBClasses.Platform(
            platform_id=entry_id,
            name=platformName,
            platformtype_id=chosenClass.platformtype_id,
            host_platform_id=None,
            nationality_id=chosenNationality.nationality_id
        )

        self.session.add(platform_obj)
        self.session.flush()

        # add to cache and return created platform
        self.platforms[platformName] = platform_obj
        # should return DB type or something else decoupled from DB?
        return platform_obj

    def addSensorType(self, sensorTypeName):
        # check in cache for sensor type
        if sensorTypeName in self.sensorTypes:
            return self.sensorTypes[sensorTypeName]

        # doesn't exist in cache, try to lookup in DB
        sensorTypeLookup = self.searchSensorType(sensorTypeName)
        if sensorTypeLookup:
            # add to cache and return looked up sensor type
            self.sensorTypes[sensorTypeName] = sensorTypeLookup
            return sensorTypeLookup

        # enough info to proceed and create entry
        sensorTypeObj = self.DBClasses.SensorType(name=sensorTypeName)
        self.session.add(sensorTypeObj)
        self.session.flush()

        # add to cache and return created sensor type
        self.sensorTypes[sensorTypeName] = sensorTypeObj
        # should return DB type or something else decoupled from DB?
        return sensorTypeObj

    def addSensor(self, sensorName, platform):
        # check in cache for sensor
        if sensorName in self.sensors:
            return self.sensors[sensorName]

        # doesn't exist in cache, try to lookup in DB
        sensorlookup = self.searchSensor(sensorName)
        if sensorlookup:
            # add to cache and return looked up sensor
            self.sensors[sensorName] = sensorlookup
            return sensorlookup

        # doesn't exist in DB, use resolver to query for data
        missingSensorData = self.missing_data_resolver.resolveSensor(self, sensorName)

        # missingSensorData should contain (sensorName, sensorType)
        # enough info to proceed and create entry
        chosenSensorName, chosenSensorType = missingSensorData
        entry_id = self.addEntry(self.DBClasses.Sensor.tabletypeId, self.DBClasses.Sensor.__tablename__)

        sensor_obj = self.DBClasses.Sensor(
            sensor_id=entry_id,
            name=sensorName,
            sensortype_id=self.DBClasses.mapUUIDType(chosenSensorType.sensortype_id),
            platform_id=self.DBClasses.mapUUIDType(platform.platform_id)
        )

        self.session.add(sensor_obj)
        self.session.flush()

        # add to cache and return created sensor
        self.sensors[sensorName] = sensor_obj
        # should return DB type or something else decoupled from DB?
        return sensor_obj

    def addState(self, timestamp, datafile, sensor, lat, long, heading, speed):
        # No cache for entries, just add new one when called

        # don't know privacy, use resolver to query for data
        missingPrivacyData = self.missing_data_resolver.resolvePrivacy(self, self.DBClasses.State.tabletypeId, self.DBClasses.State.__tablename__)

        # missingPrivacyData should contain (tabletype, privacyName)
        # enough info to proceed and create entry
        chosenTableType, chosenPrivacy = missingPrivacyData
        entry_id = self.addEntry(self.DBClasses.State.tabletypeId, self.DBClasses.State.__tablename__)

        state_obj = self.DBClasses.State(
            state_id=entry_id,
            time=timestamp,
            sensor_id=sensor.sensor_id,
            location='('+str(long.degrees)+','+str(lat.degrees)+')',
            heading=heading,
            # TODO: how to calculate course?
            #course=,
            speed=speed,
            datafile_id=datafile.datafile_id,
            privacy_id=chosenPrivacy.privacy_id
        )
        self.session.add(state_obj)
        self.session.flush()

        return state_obj


    #############################################################
    # Search/lookup functions

    def searchDatafileType(self, datafileTypeSearchName):
        # search for any datafile type with this name
        return self.session.query(self.DBClasses.DatafileType).filter(self.DBClasses.DatafileType.name == datafileTypeSearchName).first()

    def searchDatafile(self, datafileSearchName):
        # search for any datafile with this name
        return self.session.query(self.DBClasses.Datafile).filter(self.DBClasses.Datafile.reference == datafileSearchName).first()

    def searchPlatform(self, platformSearchName):
        # search for any platform with this name
        return self.session.query(self.DBClasses.Platform).filter(self.DBClasses.Platform.name == platformSearchName).first()

    def searchPlatformType(self, platformTypeSearchName):
        # search for any platform type with this name
        return self.session.query(self.DBClasses.PlatformType).filter(self.DBClasses.PlatformType.name == platformTypeSearchName).first()

    def searchNationality(self, nationalitySearchName):
        # search for any nationality with this name
        return self.session.query(self.DBClasses.Nationality).filter(self.DBClasses.Nationality.name == nationalitySearchName).first()

    def searchSensor(self, sensorSearchName):
        # search for any sensor type featuring this name
        return self.session.query(self.DBClasses.Sensor).filter(self.DBClasses.Sensor.name == sensorSearchName).first()

    def searchSensorType(self, sensorTypeSearchName):
        # search for any sensor type featuring this name
        return self.session.query(self.DBClasses.SensorType).filter(self.DBClasses.SensorType.name == sensorTypeSearchName).first()

    def searchPrivacy(self, privacySearchName):
        # search for any privacy with this name
        return self.session.query(self.DBClasses.Privacy).filter(self.DBClasses.Privacy.name == privacySearchName).first()

    def searchTableType(self, tabletype_id):
        # search for any table type with this id
        return self.session.query(self.DBClasses.TableType).filter(self.DBClasses.TableType.tabletype_id == tabletype_id).first()


    #############################################################
    # Get functions

    def getNationalities(self):
        # get list of all nationalities in the DB
        return self.session.query(self.DBClasses.Nationality).all()

    def getPlatformTypes(self):
        # get list of all platform types in the DB
        return self.session.query(self.DBClasses.PlatformType).all()

    def getPrivacies(self):
        # get list of all privacies in the DB
        return self.session.query(self.DBClasses.Privacy).all()

    def getSensors(self):
        # get list of all sensors in the DB
        return self.session.query(self.DBClasses.Sensor).all()

    def getSensorTypes(self):
        # get list of all sensors types in the DB
        return self.session.query(self.DBClasses.SensorType).all()

    def getSensorsByPlatformType(self, platformType):
        # given platform type, return all Sensors contained on platforms of that type
        return self.session.query(self.DBClasses.Platform, self.DBClasses.Sensor).join(self.DBClasses.Sensor, self.DBClasses.Sensor.platform_id == self.DBClasses.Platform.platform_id).filter(self.DBClasses.Platform.platformtype_id == platformType.platformtype_id).all()


    #############################################################
    # Validation/check functions

    # return True if provided nationality ok
    def checkNationality(self, nationality):
        if len(nationality) == 0:
            return False

        if next((nat for nat in self.getNationalities() if nat.name == nationality), None):
            # A nationality already exists with that name
            return False

        return True

    # return True if provided privacy ok
    def checkPrivacy(self, privacy):
        if len(privacy) == 0:
            return False

        if next((priv for priv in self.getPrivacies() if priv.name == privacy), None):
            # A privacy already exists with that name
            return False

        return True

    # return True if provided platform type ok
    def checkPlatformType(self, platformType):
        if len(platformType) == 0:
            return False

        if next((pt for pt in self.getPlatformTypes() if pt.name == platformType), None):
            # A platform type already exists with that name
            return False

        return True

    # return True if provided sensor ok
    def checkSensor(self, sensor):
        if len(sensor) == 0:
            return False

        if next((sen for sen in self.getSensors() if sen.name == sensor), None):
            # A sensor already exists with that name
            return False

        return True

    # return True if provided sensor type ok
    def checkSensorType(self, sensorType):
        if len(sensorType) == 0:
            return False

        if next((st for st in self.getSensorTypes() if st.name == sensorType), None):
            # A sensor type already exists with that name
            return False

        return True


    #############################################################
    # Generic Metadata functions

    def setupTabletypeMap(self):
        # setup a map of tables keyed by TableType
        dbclasses = dict([(name, cls) for name, cls in self.DBClasses.__dict__.items() if isinstance(cls, type)
                          and issubclass(cls, Base) and cls.__name__ != 'Base'])
        self.metaClasses = {}
        for tabletype in TableTypes:
            self.metaClasses[tabletype] = [cls for name, cls in dbclasses.items() if dbclasses[name].tabletype == tabletype]

    def getTabletypeData(self, tabletypes):
        retmap = {}
        for tabletype in tabletypes:
            for table in self.metaClasses[tabletype]:
                retmap[table.__name__] = self.session.query(table).count()
        return retmap

    def populateReference(self):
        pass

    def populateData(self):
        pass
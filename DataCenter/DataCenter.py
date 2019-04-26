import pandas as pd
import logging
from pymongo import MongoClient, TEXT

import DataCenter.Utils.dbutils as utils
import DataCenter.Graph.graph as graph
from DataCenter.Actor.Actor import Actor
from DataCenter.Graph.extraction import extractAndFilterData
import DataCenter.Tests.tests as tests

class DataCenter():
  '''
  Creates a DataCenter.
  A DataCenter is a MongoDB instance specific to
  a client's needs, tailored to their interests and regions

  TODO: Interface with MongoDB
  '''

  def __init__(self, startDate, endDate, query=None):
    '''
    Initializes a new DataCenter populated with data
    from the specified start date (inclusive) to the end date (exclusive)

    The data will be populated by data from specified geographies, as well
    as the specified actors involved in each geographies. Geographies are defined
    by the Region class.

    If no actors are specified, all actors will be included.

    Dates should be formatted as follows:
    'YYYY MM DD'
    e.g. '2019 02 19'

    TODO: Filter by regions
    '''
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='temp/datacenter.log',
                    filemode='w')
  
    print('INITIALIZING DATA CENTER')

    self._initDB()

    # initialize data analysis variables
    self.totalDataCount = 0
    self.relevantDataCount = 0

    # initialize the headers of the dataframe
    self.headers = utils.getSchemaHeaders()

    # initialize regions
    self.query = query

    # run unit tests
    tests.runTests()

    # get dates to initialize the database
    initDateStrings = utils.getDateRangeStrings(startDate, endDate)
    [self.updateDC(dateString) for dateString in initDateStrings]

    print('DataCenter Initialized')

    print('Logging information: log.txt')

    print('\nInformation:')
    print(f'* Total Data Count: {self.totalDataCount} articles processed')
    print(f'* Relevant Information: {self.relevantDataCount} articles stored')
    print(f'* Total Percentage: {self.relevantDataCount/self.totalDataCount:.0%}')

  def getDataFrame(self, dateString):
    try:
      # get data url
      url = utils.getDateURL(dateString)
      # read in data file
      df = pd.read_csv(url, compression='zip', encoding='latin1', header=None, sep='\t')
      df.columns = self.headers
      return True, df
    except Exception as e:
      logging.log(0, f'DataCenter.getDataFrame: {e}')
      return False, None

  def updateDC(self, dateString):
    '''
    Updates the database with information from a single day
    '''
    print(f'* Processing {dateString} Information...')
    success, df = self.getDataFrame(dateString)
    if not success: return False

    totalCount = len(df)
    print(f'** {totalCount} Rows')
    relevantCount = 0

    for ix, data in df.iterrows():
      if self.updateRow(data, dateString): relevantCount += 1

    self.totalDataCount += totalCount
    self.relevantDataCount += relevantCount

    print(f'  {dateString} processed.')
    print(f'\n* {dateString} Information: ')
    print(f'** Relevant Data: {relevantCount/totalCount:.0%}\n\n')
    return True

  def updateRow(self, data, dateString):
    try:
      logging.log(0, 'DataCenter.updateRow')
      data = extractAndFilterData(data, dateString, self.query, self._db)
      if not data: return False

      (articleID, actorIDs, locationIDs) = data

      # update actor Graph
      if not graph.updateGraph(articleID, actorIDs, self._db): return False

      return True
    except Exception as e:
      logging.log(0, e)
      return False

  def addRegion(self, region):
    '''
    TODO: Write a function that allows for a new region to be added
    '''
    return

  def removeRegion(self, regionName):
    '''
    TODO: Write a function that allows for a region to be removed
    '''
    return

  def addActor(self, actorName):
    '''
    TODO: Write a function that allows for a new region to be added
    '''
    return

  def removeActor(self, actorName):
    '''
    TODO: Write a function that allows for a region to be removed
    '''
    return

  def _initDB(self):
    # initializing DB client connection
    self._client = MongoClient()
    self._db = self._client.test_database_4

    # ensure querying on Actor DoubleMetaphone
    self._db[Actor._collectionKey].create_index([('_a_name', TEXT)])
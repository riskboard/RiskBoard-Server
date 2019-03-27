import pandas as pd
import DataCenter.Utils.dbutils as utils
import DataCenter.Graph.graph as graph
import DataCenter.Tests.tests as tests

class DataCenter():
  '''
  Creates a DataCenter.
  A DataCenter is a MongoDB instance specific to
  a client's needs, tailored to their interests and regions
  '''

  def __init__(self, startDate, endDate, geographies=None, relevantActors=None):
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

    # initialize regions
    self.geographies = geographies

    # initialize actors
    self.relevantActors = utils.formatActors(relevantActors)

    # initialize actor graph
    self.actorGraph = {}

    # initialize the headers of the dataframe
    self.headers = utils.getSchemaHeaders()

    # get dates to initialize the database
    initDateStrings = utils.getDateRangeStrings(startDate, endDate)
    [self.updateDB(dateString) for dateString in initDateStrings]

    # run unit tests
    tests.runTests()


  def updateDB(self, dateString):
    '''
    Updates the database with information from a single day
    '''
    try:
      # get data url
      url = utils.getDateURL(dateString)

      # read in data file
      df = pd.read_csv(url, compression='zip', encoding='latin1', header=None, sep='\t')
      df.columns = self.headers

      # update actor Graph
      self.actorGraph, updateActorList, newActorList = graph.updateActorGraph(df, self)
    except:
      return

  def visualizeGraph(self):
    '''
    Visualizes the actor graph in the database
    '''
    PGVGraph = graph.createPGVGraph(self.actorGraph)
    return graph.visualizePGVGraph(PGVGraph)

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
import pandas as pd
import DataBase.Utils.dbutils as utils
import DataBase.Utils.graph as graph
import DataBase.Utils.tests as tests

class DataBase():
  '''
  Creates a DataBase class
  '''

  def __init__(self, startDate, endDate):
    '''
    Initializes a new MongoDB Database populated with data
    from the specified start date (inclusive) to the end date (exclusive)

    Dates should be formatted as follows:
    'YYYY MM DD'
    e.g. '2019 02 19'
    '''
    # initialize actor graph
    self.actorGraph = {}

    # initialize the headers of the dataframe
    self.headers = utils.getSchemaHeaders()

    # get dates to initialize the database
    initDateStrings = utils.getDateRangeStrings(startDate, endDate)[:4]
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
      self.actorGraph, updateActorList, newActorList = graph.updateActorGraph(df, self.actorGraph)
    except:
      return


  def visualizeGraph(self):
    '''
    Visualizes the actor graph in the database
    '''
    PGVGraph = graph.createPGVGraph(self.actorGraph)
    return graph.visualizePGVGraph(PGVGraph)
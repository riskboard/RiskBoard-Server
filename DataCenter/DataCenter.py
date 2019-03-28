import pandas as pd
import DataCenter.Utils.dbutils as utils
import DataCenter.Graph.graph as graph
from DataCenter.Graph.extraction import extractData
import DataCenter.Tests.tests as tests
from DataCenter.Utils.SE import SE

class DataCenter():
  '''
  Creates a DataCenter.
  A DataCenter is a MongoDB instance specific to
  a client's needs, tailored to their interests and regions

  TODO: Interface with MongoDB
  '''

  def __init__(self, startDate, endDate, relevantGeo=None, relevantActors=None):
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
    print('INITIALIZING DATA CENTER')
    # initialize success error object
    self.se = SE()

    # initialize data analysis variables
    self.totalDataCount = 0
    self.relevantDataCount = 0

    # initialize the headers of the dataframe
    self.headers = utils.getSchemaHeaders()

    # initialize regions
    self.relevantGeo = relevantGeo

    # initialize actors
    self.relevantActors = utils.formatActors(relevantActors)

    # initialize actor graph
    self.graph = {}

    # initialize article list
    self.articleList = []

    # run unit tests
    tests.runTests()

    # get dates to initialize the database
    initDateStrings = utils.getDateRangeStrings(startDate, endDate)
    updateSE = [self.updateDC(dateString) for dateString in initDateStrings]
    map(lambda s: self.se.updateSE(s), updateSE)

    print('DataCenter Initialized')

    print('\nInformation:')
    print(f'* Total Data Count: {self.totalDataCount} articles processed')
    print(f'* Relevant Information: {self.relevantDataCount} articles stored')
    print(f'* Total Percentage: {self.relevantDataCount/self.totalDataCount:.0%}')

    print(f'\nErrors: ')
    [print(f'* Error: {err}') for err in self.se.errors]

  def updateDC(self, dateString):
    '''
    Updates the database with information from a single day
    '''
    print(f'* Updating {dateString} Information...')
    se = SE()

    # get data url
    url = utils.getDateURL(dateString)

    try:
      # read in data file
      df = pd.read_csv(url, compression='zip', encoding='latin1', header=None, sep='\t')
      df.columns = self.headers
    except Exception as e:
      return SE(False, [e])

    dataCount, relevantCount = 0, 0
    for ix, data in df.iterrows():
      dataCount += 1
      newSE = self.updateRow(data)
      if newSE.success:
        relevantCount += 1
      se.updateSE(newSE)

    print(f'  {dateString} processed.')
    print(f'\n* {dateString} Information: ')
    print(f'** Relevant Data: {relevantCount/dataCount:.0%}')
    return se


  def updateRow(self, data):
    try:
      se = SE()

      actorIDs, actors, locations, article = extractData(data)
      if not utils.isRelevantArticle(article, self.relevantActors, self.relevantGeo): return SE(success=False)

      # update actor Graph
      newSE, self.graph, updateActorIdList, newActorIdList = graph.updateGraph(actors, article, self.graph)
      se.updateSE(newSE)

      # TODO: Update actors in updateActorIDList and create newActorIds

      # udpate articleList
      self.articleList.append(article)
      return se
    except Exception as e:
      se = SE(False, [e])
      return se

  def visualizeGraph(self):
    '''
    Visualizes the actor graph in the database
    '''
    PGVGraph = graph.createPGVGraph(self.graph)
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
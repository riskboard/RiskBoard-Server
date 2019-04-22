from fuzzywuzzy import fuzz
import numpy as np
import DataCenter.Utils.dbutils as utils

class Query():
  '''
  Defines a Query object. Query objects include a combination
  of Keywords, GKG Themes, Actors, and Locations

  TODO: Increase modularization of the parameters (i.e. which parameters to query for)
  TODO: Store Queries in databasing (for use in caching)
  '''

  def __init__(self, keywords=None, actorNames=None, geographies=None, gkgThemes=None, actorSimilarityThreshold=0.8):
    '''
    Initializes a Query object with the specified parameters.
    '''
    self.keywords = keywords
    self.actorNames = utils.formatActors(actorNames)
    self.actorSimilarityThreshold = actorSimilarityThreshold
    self.geographies = geographies
    self.gkgThemes = set(gkgThemes)

  def filterArticle(self, locations, actorNames, gkgThemes):
    '''
    Returns True if the Article has the specified parameters in the Query,
    False otherwise.
    '''
    if not self.hasLocationInGeographies(locations):
      return False
    if not self.hasRelevantActor(actorNames):
      return False
    if not self.hasRelevantTheme(gkgThemes):
      return False
    return True

  def hasLocationInGeographies(self, locations):
    '''
    Returns True if locations has a location in geographies
    '''
    if not self.geographies or not locations: return True
    return bool(np.sum([self.isLocationInGeographies(loc) for loc in locations]))

  def isLocationInGeographies(self, location):
    '''
    Returns True if location is in the geographies
    '''
    return bool(np.sum([geo.includes(location) for geo in self.geographies]))

  def hasRelevantActor(self, actorNames):
    '''
    Returns True if there is a relevant Actor
    '''
    if not self.actorNames: return True
    return bool(np.sum([self.isRelevantActor(an) for an in self.actorNames]))

  def isRelevantActor(self, actorName):
    '''
    Returns a set of overlapping relevantActorNames
    '''
    return bool(np.sum([self._findTokenSimilarity(actorName, an) > self.actorSimilarityThreshold for an in self.actorNames]))

  def _findTokenSimilarity(self, string1, string2):
    '''
    Finds the similarity between two given strings
    TODO: Think about optimization with a large amount of relevant actors
    '''
    return fuzz.token_set_ratio(string1, string2)

  def hasRelevantTheme(self, gkgThemes):
    '''
    Returns True if the article has the relevant Themes
    '''
    return not self.gkgThemes.isdisjoint(gkgThemes)
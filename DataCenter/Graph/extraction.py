import numpy as np
from fuzzywuzzy import fuzz

from DataCenter.Article.Article import Article
from DataCenter.Actor.Actor import Actor
from DataCenter.Geo.GDeltLocation import GDeltLocation

TYPE_ORGANIZATION = 'organization'
TYPE_PERSON = 'person'

def extractAndFilterData(data, relevantActors, relevantGeo, db):
  '''
  Extracts the url, people, organizations, and location from
  one row in the GKG dataframe
  '''
  peopleNames = str(data['Persons']).split(';')
  orgNames = str(data['Organizations']).split(';')
  actorNames = peopleNames+orgNames

  locationStr = str(data['Locations'])
  locations = extractLocations(locationStr)

  if not isRelevantArticle(actorNames, locations, relevantActors, relevantGeo): return None
  locationIDs = [loc.storeDB(db) for loc in locations]

  peopleIDs = extractActorIDs(TYPE_PERSON, peopleNames, db)
  orgIDs = extractActorIDs(TYPE_PERSON, orgNames, db)
  actorIDs = peopleIDs+orgIDs

  url = str(data['DocumentIdentifier'])
  articleID = extractArticleID(url, actorIDs, peopleIDs, orgIDs, locationIDs, db)

  return articleID, actorIDs, locationIDs

def extractActorIDs(actorType, actorNames, db):
  if not len(actorNames): return []
  return [extractActorID(actorType, a, db) for a in actorNames]

def extractActorID(actorType, actorName, db):
  return Actor(TYPE_PERSON, actorName, db=db)._mongoID

def extractLocations(locationStr):
  '''
  Exracts locations from a row in data
  '''
  if locationStr == 'nan':
    return None
  else:
    location_infos = [location.split('#') for location in locationStr.split(';')]
    locations = [rawToGDeltLocation(loc) for loc in location_infos]
  return locations

def rawToGDeltLocation(loc):
  '''
  Converts a location in GDelt to a GDeltLocation class
  '''
  loc_type, name, latitude, longitude = loc[0], loc[1], float(loc[4]), float(loc[5])
  return GDeltLocation(type=loc_type, name=name, latitude=latitude, longitude=longitude)

def extractArticleID(url, actorIDs, peopleIDs, orgIDs, locations, db):
  '''
  Creates a new Article class with the relevant
  people, organizations, and locations
  '''
  return Article(url, actorIDs, peopleIDs, orgIDs, locations, db)._mongoID

def isRelevantArticle(actorNames, locations, relevantActors, relevantGeo):
  '''
  Returns True if article is relevant
  '''
  return (hasLocationInGeographies(locations, relevantGeo) and hasRelevantActor(actorNames, relevantActors))

def hasLocationInGeographies(locations, geographies):
  '''
  Returns True if locations has a location in geographies
  '''
  if not geographies or not locations: return True
  return bool(np.sum([isLocationInGeographies(loc, geographies) for loc in locations]))

def isLocationInGeographies(location, geographies):
  '''
  Returns True if location is in the geographies
  '''
  return bool(np.sum([inGeography(location, geo) for geo in geographies]))

def inGeography(location, geography):
  '''
  Returns True if location is in the geography
  '''
  return geography.includes(location)

def hasRelevantActor(actorNames, relevantActors):
  '''
  Returns True if there is at least one actor that is relevant, False otherwise
  TODO: Terminate early once one is found
  '''
  if not relevantActors: return True
  return bool(np.sum([isRelevantActor(actor, relevantActors) for actor in actorNames]))

def isRelevantActor(actorName, relevantActors, threshold=60):
  '''
  Returns True if there is one actor in relevantActors with a 
  similarity score of at least 0.8, False otherwise
  '''
  if not relevantActors: return True
  similarities = [findSimilarity(actorName, relevantActor) > threshold for relevantActor in relevantActors]
  return bool(np.sum(similarities))

def findSimilarity(string1, string2):
  '''
  Finds the similarity between two given strings
  TODO: Think about optimization with a large amount of relevant actors
  '''
  return fuzz.token_set_ratio(string1, string2)
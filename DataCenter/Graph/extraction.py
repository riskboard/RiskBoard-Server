import numpy as np
import logging
from fuzzywuzzy import fuzz
from metaphone import doublemetaphone

from DataCenter.Article.Article import Article
from DataCenter.Actor.Actor import Actor
from DataCenter.Geo.GDeltLocation import GDeltLocation

TYPE_ORGANIZATION = 'organization'
TYPE_PERSON = 'person'

def extractAndFilterData(data, relevantActorNames, relevantGeo, db):
  '''
  Extracts the url, people, organizations, and location from
  one row in the GKG dataframe
  '''
  peopleNames = list(filter(lambda x: x!= 'nan', str(data['Persons']).split(';')))
  orgNames = list(filter(lambda x: x != 'nan', str(data['Organizations']).split(';')))
  actorNames = peopleNames+orgNames
  if not len(actorNames): return False

  locationStr = str(data['Locations'])
  locations = extractLocations(locationStr)

  if not isRelevantArticle(actorNames, relevantActorNames, locations, relevantGeo): return False

  locationIDs = [loc.storeDB(db) for loc in locations]

  peopleIDs = extractActorIDs(TYPE_PERSON, peopleNames, db)
  orgIDs = extractActorIDs(TYPE_PERSON, orgNames, db)
  actorIDs = peopleIDs+orgIDs

  url = str(data['DocumentIdentifier'])
  articleID = extractArticleID(url, actorIDs, peopleIDs, orgIDs, locationIDs, db)

  return articleID, actorIDs, locationIDs

def extractActorIDs(actorType, actorNames, db):
  '''
  Queries the database to find actors that have similar metaphone names
  If there are more than one, uses the highest fuzzy score
  '''
  return [extractActorID(actorType, a, db) for a in actorNames]

def extractActorID(actorType, actorName, db):
  '''
  Queries the database to find actors that have similar metaphone names
  If there are more than one, uses the highest fuzzy score
  '''
  collection = db[Actor._collectionKey]
  meta = doublemetaphone(actorName)
  _a_name = actorName[0] + actorName[1]
  query = {'_a_name': _a_name}
  result = collection.find_one(query)
  
  if result:
    print('findone result: ', result)
    return result['_id']
  logging.log(3, 'extraction.extractActorID: created new actor')
  # creates a new Actor
  actorID = Actor(actorType, actorName, db=db)._mongoID
  return actorID

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

def extractArticleID(url, actorIDs, peopleIDs, orgIDs, locationIDs, db):
  '''
  Creates a new Article class with the relevant
  people, organizations, and locations
  '''
  return Article(url, actorIDs, peopleIDs, orgIDs, locationIDs, db=db)._mongoID

def isRelevantArticle(actorNames, relevantActors, locations, relevantGeo):
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

def hasRelevantActor(actorNames, relevantActorNames):
  '''
  Returns True if there is a relevant Actor
  '''
  if not relevantActorNames: return True
  return bool(np.sum([isRelevantActor(an, relevantActorNames) for an in actorNames]))

def isRelevantActor(actorName, relevantActorNames, threshold=0.8):
  '''
  Returns a set of overlapping relevantActorNames
  '''
  return bool(np.sum([findTokenSimilarity(actorName, ran) > threshold for ran in relevantActorNames]))

def findTokenSimilarity(string1, string2):
  '''
  Finds the similarity between two given strings
  TODO: Think about optimization with a large amount of relevant actors
  '''
  return fuzz.token_set_ratio(string1, string2)

def findNameSimilarity(name1, name2):
  '''
  Returns True if the double metaphone of the 
  two names are the same
  '''
  return doublemetaphone(name1) == doublemetaphone(name2)
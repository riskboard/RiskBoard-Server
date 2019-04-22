import logging
from metaphone import doublemetaphone

from DataCenter.Article.Article import Article
from DataCenter.Actor.Actor import Actor
from DataCenter.Geo.GDeltLocation import GDeltLocation

TYPE_ORGANIZATION = 'organization'
TYPE_PERSON = 'person'

def extractAndFilterData(data, query, db):
  '''
  Extracts the url, people, organizations, and location from
  one row in the GKG dataframe
  '''
  peopleNames = extractDataList('Persons', data)
  orgNames = extractDataList('Organizations', data)
  
  actorNames = peopleNames+orgNames
  if not len(actorNames):
    return False

  locations = extractLocations(data)

  gkgThemes = set(extractDataList('Themes', data))

  if query and not query.filterArticle(locations, actorNames, gkgThemes): return False

  locationIDs = [loc.storeDB(db) for loc in locations]

  peopleIDs = extractActorIDs(TYPE_PERSON, peopleNames, db)
  orgIDs = extractActorIDs(TYPE_PERSON, orgNames, db)
  actorIDs = peopleIDs+orgIDs

  url = str(data['DocumentIdentifier'])
  articleID = extractArticleID(url, actorIDs, peopleIDs, orgIDs, locationIDs, db)

  return articleID, actorIDs, locationIDs

def extractDataList(fieldName, data):
  '''
  extracts list from fieldNames
  '''
  return list(filter(lambda x: x!= 'nan', str(data[fieldName]).split(';')))

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

def extractLocations(data):
  '''
  Exracts locations from a row in data
  '''
  locationStr = str(data['Locations'])
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
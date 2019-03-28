from DataCenter.Article.Article import Article
from DataCenter.Actor.Actor import Actor
from DataCenter.Geo.GDeltLocation import GDeltLocation

TYPE_ORGANIZATION = 'organization'
TYPE_PERSON = 'person'

def extractData(data):
  '''
  Extracts the url, people, organizations, and location from
  one row in the GKG dataframe
  '''
  peopleNames = str(data['Persons']).split(';')
  peopleIDs, people = extractActors(TYPE_PERSON, peopleNames)

  orgNames = str(data['Organizations']).split(';')
  orgIDs, orgs = extractActors(TYPE_PERSON, orgNames)

  locationStr = str(data['Locations'])
  locations = extractLocations(locationStr)

  actorIDs, actorNames, actors = peopleIDs+orgIDs, peopleNames+orgNames, people+orgs

  url = str(data['DocumentIdentifier'])
  article = extractArticle(url, actorIDs, actorNames, peopleIDs, orgIDs, locations)

  return actorIDs, actors, locations, article

def extractActors(actorType, actorNames):
  actorDats = [extractActor(actorType, a) for a in actorNames]
  return [list(t) for t in zip(*actorDats)]

def extractActor(actorType, actorName):
  actor = Actor(TYPE_PERSON, actorName)
  return actor.id, actor

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

def extractArticle(url, actorIDs, actorNames, peopleIDs, orgIDs, locations):
  '''
  Creates a new Article class with the relevant
  people, organizations, and locations
  '''
  return Article(url, actorIDs, actorNames, peopleIDs, orgIDs, locations)
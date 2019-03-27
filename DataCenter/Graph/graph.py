import pandas as pd
import numpy as np
import pygraphviz as pgv
import matplotlib.pyplot as plt

import DataCenter.Utils.dbutils as utils
from DataCenter.Geo.GDeltLocation import GDeltLocation

TYPE_ORGANIZATION = 'organization'
TYPE_PERSON = 'person'

def updateActorGraph(df, datacenter):
  '''
  updates actor graphs to include new articles
  returns updateActors and newActors, which represent
  items to update and create, respectively
  '''
  actorGraph = datacenter.actorGraph
  relevantActors = datacenter.relevantActors
  geographies = datacenter.geographies
  updateActorList, newActorList = [], []

  for ix, data in df.iterrows():
    url, people, organizations, actors, locations = extractData(data)
    if not hasLocationInGeographies(locations, geographies): continue
    print('Found Relevant Location!')
    if not hasRelevantActor(actors, relevantActors): continue

    actorGraph, updateActorList, newActorList = addURLToActors(
      people, url, TYPE_PERSON, actorGraph, updateActorList, newActorList)
    actorGraph, updateActorList, newActorList = addURLToActors(
      organizations, url, TYPE_ORGANIZATION, actorGraph, updateActorList, newActorList)
    actorGraph = updateActorEdges(actors, url, actorGraph)

  print(updateActorList, newActorList)
  return actorGraph, updateActorList, newActorList

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

def hasRelevantActor(actors, relevantActors):
  '''
  Returns True if there is at least one actor that is relevant, False otherwise
  TODO: Terminate early once one is found
  '''
  if not relevantActors: return True
  return bool(np.sum([isRelevantActor(actor, relevantActors) for actor in actors]))

def isRelevantActor(actor, relevantActors, threshold=60):
  '''
  Returns True if there is one actor in relevantActors with a 
  similarity score of at least 0.8, False otherwise
  '''
  if not relevantActors: return True
  similarities = [utils.findSimilarity(actor, relevantActor) > threshold for relevantActor in relevantActors]
  return bool(np.sum(similarities))

def extractData(data):
  '''
  Extracts the url, people, organizations, and location from
  one row in the GKG dataframe
  '''
  url = str(data['DocumentIdentifier'])
  people = str(data['Persons']).split(';')
  organizations = str(data['Organizations']).split(';')
  locations = extractLocations(data)
  actors = people + organizations
  return (url, people, organizations, actors, locations)

def extractLocations(data):
  '''
  Exracts locations from a row in data
  '''
  if str(data['Locations']) == 'nan':
    return None
  else:
    location_infos = [location.split('#') for location in str(data['Locations']).split(';')]
    locations = [rawToGDeltLocation(loc) for loc in location_infos]
  return locations

def rawToGDeltLocation(loc):
  '''
  Converts a location in GDelt to a GDeltLocation class
  '''
  loc_type, name, latitude, longitude = loc[0], loc[1], float(loc[4]), float(loc[5])
  return GDeltLocation(type=loc_type, name=name, latitude=latitude, longitude=longitude)

def createNewActor(name, url, actorType, actorGraph):
  '''
  Creates a new actor based on the name and article url
  '''
  actorGraph[name] = {
    'name': name,
    'type': actorType,
    'connections': {},
    'urls': [url],
    'sentiment': 0,
  }
  return actorGraph

def addURLToActors(names, url, actorType, actorGraph, updateActorList, newActorList):
  '''
  Adds the urls to the existing actorGraph
  If the name is not currently within the graph, creates a new object
  '''
  for name in names:
    if name == 'nan': continue
    if name in actorGraph:
      actorGraph[name]['urls'].append(url)
      updateActorList.append(name)
    else:
      actorGraph = createNewActor(name, url, actorType, actorGraph)
      newActorList.append(name)
  return actorGraph, updateActorList, newActorList

def updateActorEdges(actors, url, actorGraph):
  '''
  Creates all edges between actors in the url
  '''
  for a1 in actors:
    for a2 in actors:
      if a1 == 'nan' or a2 == 'nan': continue
      if a1 == a2: continue
      if a2 in actorGraph[a1]['connections']:
        actorGraph = updateActorEdge(a1, a2, url, actorGraph)
      else:
        actorGraph = createActorEdge(a1, a2, url, actorGraph)
  return actorGraph

def updateActorEdge(a1, a2, url, actorGraph):
  '''
  Updates an existing connection between two actors
  '''
  connection = actorGraph[a1]['connections'][a2]
  connection['urls'].append(url)
  connection['strength'] += 1
  return actorGraph

def createActorEdge(a1, a2, url, actorGraph):
  '''
  Creates a new connection between two actors
  '''
  actorGraph[a1]['connections'][a2] = {
    'urls': [url],
    'strength': 1
  }
  return actorGraph

def createEdgeList(start_node, connections):
  '''
  Converts connections dict to edge list for networkx
  '''
  return [(start_node, end_node) for end_node in connections.keys()]

def createPGVGraph(actorGraph):
  '''
  Creates a PGV Graph from an actorGraph
  '''
  G = pgv.AGraph()
  for a in actorGraph.keys():
    G.add_node(a)
    G.add_edges_from(createEdgeList(a, actorGraph[a]['connections']))
  return G

def visualizePGVGraph(PGVGraph, outfp='network.svg'):
  '''
  Visualizes the PKG Graph
  '''
  PGVGraph.layout()
  PGVGraph.draw(outfp)
  return

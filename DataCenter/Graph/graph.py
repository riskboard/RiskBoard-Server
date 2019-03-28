import pandas as pd
import numpy as np
import pygraphviz as pgv
import matplotlib.pyplot as plt
import logging

import DataCenter.Utils.dbutils as utils
from DataCenter.Utils.SE import SE
from DataCenter.Geo.GDeltLocation import GDeltLocation
from DataCenter.Actor.Actor import Actor
from DataCenter.Actor.ActorConnection import ActorConnection
from DataCenter.Article.Article import Article

TYPE_ORGANIZATION = 'organization'
TYPE_PERSON = 'person'

def updateGraph(df, datacenter):
  '''
  updates actor graphs to include new articles
  returns updateActors and newActors, which represent
  items to update and create, respectively
  '''
  print('* Reading new data frame...')
  se = SE()
  graph = datacenter.graph
  relevantActors = datacenter.relevantActors
  geographies = datacenter.geographies

  for ix, data in df.iterrows():
    actorIDs, actors, article, locations = extractData(data)
    if not hasLocationInGeographies(locations, geographies): continue
    if not hasRelevantActor(actors, relevantActors): continue

    graph, updateActorIdList, newActorIdList = attachActorsToGraph(actors, graph)

    # updates actors with new articles
    newSE, graph= addArticleToActors(actors, article, graph)
    se.updateSE(newSE)

    # update edges
    newSE, graph = updateActorEdges(actors, article, graph)
    se.updateSE(newSE)

  return se, graph, updateActorIdList, newActorIdList

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
  similarities = [utils.findSimilarity(actor.name, relevantActor) > threshold for relevantActor in relevantActors]
  return bool(np.sum(similarities))

def extractData(data):
  '''
  Extracts the url, people, organizations, and location from
  one row in the GKG dataframe
  '''
  url = str(data['DocumentIdentifier'])
  article = extractArticle(url)

  peopleNames = str(data['Persons']).split(';')
  peopleIDs, people = extractActors(TYPE_PERSON, peopleNames)

  orgNames = str(data['Organizations']).split(';')
  orgIDs, orgs = extractActors(TYPE_PERSON, orgNames)

  locationStr = str(data['Locations'])
  locations = extractLocations(locationStr)

  actorIDs, actors = peopleIDs + orgIDs, people + orgs
  return actorIDs, actors, article, locations

def extractActors(actorType, actorNames):
  actorDats = [extractActor(actorType, a) for a in actorNames]
  return [list(t) for t in zip(*actorDats)]

def extractActor(actorType, actorName):
  actor = Actor(TYPE_PERSON, actorName)
  return actor.id, actor

def extractArticle(url):
  return Article(url)

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

def attachActorsToGraph(actors, graph):
  '''
  Attaches a list of actors to the graph
  '''
  updateActorList, newActorList = [], []
  for a in actors:
    if a.id in graph:
      updateActorList.append(a.id)
      continue
    graph, newActorList = attachNewActorToGraph(a, graph, newActorList)
  return graph, updateActorList, newActorList

def attachNewActorToGraph(actor, graph, newActorList):
  '''
  Attaches the new actor to the graph
  '''
  graph[actor.id] = actor
  newActorList.append(actor.id)
  return graph, newActorList

def addArticleToActors(actors, article, graph):
  '''
  Adds the article to the existing graph
  If the name is not currently within the graph, creates a new object
  '''
  se = SE()
  for actor in actors:
    if actor.id not in graph:
      error = f'(addArticleToActors): actor {actor.id} not in graph'
      logging.error(error)
      se = SE(False, [error])
      se.updateSE(se)
    graph[actor.id].addArticle(article)
  return se, graph

def updateActorEdges(actors, article, graph):
  '''
  Creates all edges between actors in the url
  '''
  se = SE()
  for a1 in actors:
    for a2 in actors:
      if a1.id == a2.id: continue
      newSE = a1.updateOrCreateConnection(a2, article)
      se.updateSE(newSE)
  return se, graph

def createEdgeList(start_node, connections):
  '''
  Converts connections dict to edge list for networkx
  '''
  return [(start_node, end_node) for end_node in connections.keys()]

def createPGVGraph(graph):
  '''
  Creates a PGV Graph from an graph
  '''
  G = pgv.AGraph()
  for actorID in graph.keys():
    G.add_node(actorID)
    G.add_edges_from(createEdgeList(actorID, graph[actorID].connections))
  return G

def visualizePGVGraph(PGVGraph, outfp='network.svg'):
  '''
  Visualizes the PKG Graph
  '''
  PGVGraph.layout()
  PGVGraph.draw(outfp)
  return

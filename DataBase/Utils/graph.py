import pandas as pd
import numpy as pd
import pygraphviz as pgv
import matplotlib.pyplot as plt

TYPE_ORGANIZATION = 'organization'
TYPE_PERSON = 'person'

def updateActorGraph(df, actorGraph):
  '''
  updates actor graphs to include new articles
  returns updateActors and newActors, which represent
  items to update and create, respectively
  '''
  updateActorList, newActorList = [], []

  for ix, data in df.iterrows():
    url = str(data['DocumentIdentifier'])
    people = str(data['Persons']).split(';')
    organizations = str(data['Organizations']).split(';')

    actorGraph, updateActorList, newActorList = addURLToActors(
      people, url, TYPE_PERSON, actorGraph, updateActorList, newActorList)
    actorGraph, updateActorList, newActorList = addURLToActors(
      organizations, url, TYPE_ORGANIZATION, actorGraph, updateActorList, newActorList)

    actors = people + organizations
    actorGraph = updateActorEdges(actors, url, actorGraph)

  return actorGraph, updateActorList, newActorList

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
  G = pgv.AGraph()
  for a in actorGraph.keys():
    G.add_node(a)
    G.add_edges_from(createEdgeList(a, actorGraph[a]['connections']))
  return G

def visualizePGVGraph(PGVGraph):
  PGVGraph.layout()
  PGVGraph.draw('network.svg')
  return

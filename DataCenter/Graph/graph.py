import pandas as pd
import numpy as np
import pygraphviz as pgv
import matplotlib.pyplot as plt
import logging

from DataCenter.Utils.SE import SE
from DataCenter.Actor.ActorConnection import ActorConnection
from DataCenter.Graph.extraction import extractData

def updateGraph(actors, article, graph):
  '''
  updates actor graphs to include new articles
  returns updateActors and newActors, which represent
  items to update and create, respectively
  '''
  se = SE()
  graph, updateActorIdList, newActorIdList = attachActorsToGraph(actors, graph)
  # updates actors with new articles
  newSE, graph= addArticleToActors(actors, article, graph)
  se.updateSE(newSE)
  # update edges
  newSE, graph = updateActorEdges(actors, article, graph)
  se.updateSE(newSE)
  return se, graph, updateActorIdList, newActorIdList

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

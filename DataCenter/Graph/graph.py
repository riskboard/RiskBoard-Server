import pandas as pd
import numpy as np
import pygraphviz as pgv
import matplotlib.pyplot as plt
import logging

from DataCenter.Actor.Actor import Actor
from DataCenter.Actor.ActorConnection import ActorConnection

def updateGraph(articleID, actorIDs, db):
  '''
  updates actor graphs to include new articles
  returns updateActors and newActors, which represent
  items to update and create, respectively
  '''
  logging.log(1, 'updateGraph')

  # updates actors with new articles
  if not addArticleToActors(articleID, actorIDs, db): return False

  # update edges
  if not updateActorEdges(articleID, actorIDs, db): return False

  return True

def addArticleToActors(articleID, actorIDs, db):
  '''
  Adds the article to the existing graph
  If the name is not currently within the graph, creates a new object
  '''
  logging.log(2, 'addArticleToActors')
  for a in actorIDs:
    query = {'_id': a}
    actor = db.actor.find_one(query)
    if not actor:
      logging.error('Actor does not exist.')
      return False
    result = db[Actor._collectionKey].update_one(query, {
      '$push': { 'articleIDs': articleID }
    })
    if not result.acknowledged:
      logging.error('graph.addArticleToActors: push not acknowledged')
      return False
  return True

def updateActorEdges(articleID, actorIDs, db):
  '''
  Creates all edges between actors in the url
  '''
  logging.log(2, 'updateActorEdges')
  if not len(actorIDs) or len(actorIDs)==1: return True
  for ix, a1 in enumerate(actorIDs):
    for a2 in actorIDs[ix+1:]:
      query1, query2 = {'_id': a1}, {'_id': a2}
      actor1Obj, actor2Obj = db.actor.find_one(query1), db.actor.find_one(query2)
      if not actor1Obj or not actor2Obj:
        logging.error('graph.updateActorEdges: one of the actors was not found')
        return False
      actor1Obj['_db'], actor2Obj['_db'] = db, db
      actor1, actor2 = Actor.fromDB(actor1Obj), Actor.fromDB(actor2Obj)
      if not actor1.updateOrCreateConnection(actor2, articleID): return False
  return True
import logging
from DataCenter.Actor.ActorConnection import ActorConnection
from DataCenter.Utils.SE import SE

class Actor():
  '''
  Defines the Actor class, which can represent
  an organization, a person, or a notable group

  TODO: Interface with MongoDB
  '''
  actorID = 0

  def __init__(self, actorType, name, location=None, articles=[], **kwds):
    '''
    Initializes an Actor object.
    '''
    self.id = Actor.actorID
    Actor.actorID += 1

    self.type = actorType
    self.name = name
    self.location = location
    self.articles = articles

    # Dictionary to ActorConnections
    self.connections = {}

  def addArticle(self, article):
    '''
    Adds an article to the Actor oject
    '''
    self.articles.append(article)

  def updateOrCreateConnection(self, actor, article):
    '''
    Adds a connection to another actor.
    If the connection already exists, adds the article
    to the existing connection

    If the connection doesn't exist, creates a new one.
    '''
    se = SE()
    if actor.id in self.connections:
      newSE = self.updateConnection(actor, article)
    else:
      newSE = self.createConnection(actor, article)
    se.updateSE(newSE)
    return se

  def createConnection(self, actor, article):
    '''
    Creates a connection to the new actor
    with the new article.
    If the connection already exists, throws an error.
    '''
    se = SE()
    if actor.id in self.connections:
      error = f"(Actor) Error: Connection already exists"
      logging.error(error)
      newSE = SE(False, [error])
      se.updateSE(newSE)
    self.connections[actor.id] = ActorConnection(self, actor, [article])
    return se

  def updateConnection(self, actor, article):
    '''
    Updates the existing connection between actors.
    If the connection doesn't exist, throws an error.
    '''
    se = SE()
    if actor.id not in self.connections:
      error = f"(Actor) Error: Connection doesn't exist"
      logging.error(error)
      newSE = SE(False, [error])
      se.updateSE(newSE)
    self.connections[actor.id].updateConnection(article)
    return se
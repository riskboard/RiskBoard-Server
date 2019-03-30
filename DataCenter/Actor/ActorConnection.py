import logging
from bson.objectid import ObjectId

class ActorConnection():
  '''
  Defines an Actor Connection.
  An Actor Connection is (usually) tied to an article
  and a 'strength'. It will have a sentiment attached as well.

  TODO: Implement sentiment in connection
  '''
  _collectionKey = 'actor_connection'

  def __init__(self, actorIDs, articleIDs=None, sentiment=None, id=None, db=None):
    '''
    Initializes an ActorConnection.
    '''

    self.actorIDs = actorIDs
    self.strength = len(articleIDs)
    self.articleIDs = articleIDs
    self.sentiment = sentiment

    if db:
      self._db = db
      self._collection = db[ActorConnection._collectionKey]
      if not id:
        self.storeDB(db)
      else:
        self._mongoID = id
        self._id = str(id)

  def updateConnection(self, articleID):
    '''
    Updates the connection with the new article
    '''
    self._updateSentiment([articleID])
    query = {'_id': self._mongoID}
    result = self._collection.update_one(query, {
      '$set': {'sentiment': self.sentiment},
      '$push': {'articleIDs': articleID},
      '$inc': {'strength': 1}
    })
    if not result.acknowledged:
      logging.error('DB: updateConnection not acknowledged')
      return False
    return True

  def _updateSentiment(self, articles):
    '''
    TODO: Updates self.sentiment with new articles
    '''
    return 0

  def storeDB(self, db):
    '''
    Stores in database
    '''
    if not db:
      logging.error('No DB provided')
      return False
    self._mongoID = self._collection.insert_one(self._serialize()).inserted_id
    self._id = str(self._mongoID)
    return self._id

  def _serialize(self, format='bson'):
    '''
    Serializes the ActorConnection
    '''
    return {
      'actorIDs': self.actorIDs,
      'strength': self.strength,
      'articleIDs': self.articleIDs,
      'sentiment': self.sentiment
    }

  @classmethod
  def fromDB(cls, obj):
    '''
    Recovers class from obj
    '''
    return cls(obj['actorIDs'], obj['articleIDs'], obj['sentiment'], obj['_id'], obj['_db'])

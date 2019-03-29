import logging

class Article():
  '''
  Defines the Article class. An article refers to
  a specific article, for example a Twitter article,
  a news article

  TODO: Write the parse_url function
  '''
  _collection = 'article'

  def __init__(self, url, actorIDs=[], peopleIDs=[], orgIDs=[], locationIDs=[], db=None, **kwds):
    '''
    Initializes an Article class from a url.
    '''
    self.url = url
    self.actorIDs = actorIDs
    self.peopleIDs = peopleIDs
    self.orgIDs = orgIDs
    self.locationIDs = locationIDs
    self.keywords = self._parse_url(url)

    if db: self.storeDB(db)

  def _parse_url(self, url):
    '''
    TODO: Takes in a url, and returns
    its summary, actors, keywords
    '''
    return None, None, None

  def storeDB(self, db):
    '''
    Stores in database
    '''
    if not db:
      logging.error('No DB provided')
      return False
    self._mongoID = db[Article._collection].insert_one(self._serialize()).inserted_id
    self._id = str(self._mongoID)
    return self._id

  def _serialize(self):
    '''
    Serializes the Article class
    '''
    return {
      'url': self.url,
      'actorIDs': self.actorIDs,
      'peopleIDs': self.peopleIDs,
      'orgIDs': self.orgIDs,
      'locationIDs': self.locationIDs,
      'keywords': self.keywords
    }
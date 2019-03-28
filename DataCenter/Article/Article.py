class Article():
  '''
  Defines the Article class. An article refers to
  a specific article, for example a Twitter article,
  a news article

  TODO: Interface with MongoDB
  TODO: Write the parse_url function
  '''
  def __init__(self, url, actorIDs=[], actorNames=[], peopleIDs=[], orgIDs=[], locations=[], **kwds):
    '''
    Initializes an Article class from a url.
    '''
    self.url = url
    self.actorIDs = actorIDs
    self.actorNames = actorNames
    self.peopleIDs = peopleIDs
    self.orgIDs = orgIDs
    self.locations = locations
    self.keywords = self._parse_url(url)

  def _parse_url(self, url):
    '''
    TODO: Takes in a url, and returns
    its summary, actors, keywords
    '''
    return None, None, None
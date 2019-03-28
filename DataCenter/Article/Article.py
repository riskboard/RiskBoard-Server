class Article():
  '''
  Defines the Article class. An article refers to
  a specific article, for example a Twitter article,
  a news article

  TODO: Interface with MongoDB
  '''
  def __init__(self, url, **kwds):
    '''
    Initializes an Article class from a url.
    '''
    self.url = url
    self.summary, self.actors, self.keywords = self._parse_url(url)

  def _parse_url(self, url):
    '''
    TODO: Takes in a url, and returns
    its summary, actors, keywords
    '''
    return None, None, None
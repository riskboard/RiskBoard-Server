class ActorConnection():
  '''
  Defines an Actor Connection.
  An Actor Connection is (usually) tied to an article
  and a 'strength'. It will have a sentiment attached as well.

  TODO: Implement sentiment in connection
  TODO: Interface with MongoDB
  '''
  def __init__(self, primaryActor, secondaryActor, articles=None):
    '''
    Initializes an ActorConnection.
    '''
    self.primaryActor = primaryActor
    self.secondaryActor = secondaryActor
    self.strength = len(articles)
    self.articles = articles
    self.sentiment = self._updateSentiment(articles)

  def updateConnection(self, article):
    '''
    Updates the connection with the new article
    '''
    self.strength += 1
    self.articles.append(article)
    self._updateSentiment([article])

  def _updateSentiment(self, articles):
    '''
    TODO: Updates self.sentiment with new articles
    '''
    return False

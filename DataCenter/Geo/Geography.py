import logging
from DataCenter.Geo.Location import Location

class Geography():
  '''
  Defines a Geography class

  TODO: Interface with MongoDB
  '''
  _collection = 'geography'

  def __init__(self, name, unit='km', description=None, db=None, **kwds):
    '''
    Initializes the Region class around the center with
    the specified radius
    '''
    self.unit = unit
    self.description = description
    self.name = name

    if db: self.storeDB(db)

  def setName(self, name):
    '''
    Sets the name of the region
    '''
    self.name = name

  def setDescription(self, description):
    '''
    Sets the description of the region
    '''
    self.description = description

  def includes(self, location):
    '''
    Returns True if location is in the Geography.
    Overrided by inherited classes.
    '''
    return True

  def storeDB(self, db):
    '''
    Stores in database
    '''
    if not db:
      logging.error('No DB provided')
      return False
    self._mongoID = db[Location._collection].insert_one(self._serialize()).inserted_id
    self._id = str(self._mongoID)
    return self._id

  def _serialize(self, format='bson'):
    '''
    Serializes the geography
    '''
    return {
      'unit': self.unit,
      'description': self.description,
      'name': self.name
    }
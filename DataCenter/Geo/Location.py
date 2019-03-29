import logging

class Location():
  '''
  Defines a location class, which involves
  Name (String): Location Name
  Latitude (Float): Location Latitude
  Longitude (Float): Location Longitude

  TODO: Interface with MongoDB
  '''
  _collection = 'location'

  def __init__(self, name, latitude, longitude, db=None, **kwds):
    '''
    Initializes a Location class
    '''
    if not self._validate(name, latitude, longitude):
      return None

    self.name = name
    self.latitude = latitude
    self.longitude = longitude

    if db: self.storeDB(db)

  def move(self, latitude, longitude):
    '''
    Moves the position of the location.
    Returns True if successful, False otherwise
    '''
    if self._validate(self.name, latitude, longitude):
      self.latitude = latitude
      self.longitude = longitude
      return True
    else:
      return False

  def _validate(self, name, latitude, longitude):
    '''
    Verifies the initialization parameters.
    '''
    error = None

    if not isinstance(name, str):
      error = 'Invalid location name.'
    elif not isinstance(latitude, float):
      error = 'Invalid latitude.'
    elif not isinstance(longitude, float):
      error = 'Invalid longitude.'

    if error:
      print(error)
      return False

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
    return self._mongoID

  def _serialize(self, format='bson'):
    '''
    Serializes the location class
    '''
    return {
      'name': self.name,
      'latitude': self.latitude,
      'longitude': self.longitude
    }

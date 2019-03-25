class Location():
  '''
  Defines a location class, which involves
  Name (String): Location Name
  Latitude (Float): Location Latitude
  Longitude (Float): Location Longitude
  '''
  def __init__(self, name, latitude, longitude):
    '''
    Initializes a Location class
    '''
    if not self._validate(name, latitude, longitude):
      return None

    self.name = name
    self.latitude = latitude
    self.longitude = longitude

  def move(self, latitude, longitude):
    '''
    Moves the position of the location.
    Returns True if successful, False otherwise
    '''
    if self._validate(name, latitude, longitude):
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

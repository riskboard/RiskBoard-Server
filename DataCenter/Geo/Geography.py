from DataCenter.Geo.Location import Location

class Geography():
  def __init__(self, name, unit='km', description=None, **kwds):
    '''
    Initializes the Region class around the center with
    the specified radius
    '''
    self.unit = unit
    self.description = description
    self.name = name

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
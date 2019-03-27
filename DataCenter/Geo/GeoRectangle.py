from DataCenter.Geo.Geography import Geography
from DataCenter.Geo import geoutils

class GeoRectangle(Geography):
  '''
  Defines the GeoRectangle class. A GeoRectangle is defined by four lines,
  boundaries = (north, south, east, west)
  which describe the boundaries of the GeoRectangle

  TODO: support 'miles' and 'km'
  '''
  def __init__(self, boundaries, **kwds):
    '''
    Initializes the Region class around the center with
    the specified radius
    '''
    (self.north, self.south, self.east, self.west) = boundaries
    super().__init__(**kwds)

  def includes(self, location):
    '''
    Returns True if the coordinate is within the region,
    False otherwise
    '''
    if location.name == self.name: return True
    coord = location.latitude, location.longitude
    return ((coord[0] < self.north and coord[0] > self.south) and
      (coord[1] < self.east and coord[1] > self.west))

  def setNorth(self, north):
    '''
    Moves the north location to the specified new location
    '''
    self.north = north

  def setSouth(self, south):
    '''
    Moves the south location to the specified new location
    '''
    self.south = south

  def setEast(self, east):
    '''
    Moves the east location to the specified new location
    '''
    self.east = east

  def setWest(self, west):
    '''
    Moves the north location to the specified new location
    '''
    self.west = west

  def setBoundaries(self, north, south, east, west):
    '''
    Sets all four boundaries to new locations
    '''
    self.setNorth(north)
    self.setSouth(south)
    self.setEast(east)
    self.setWest(west)
from DataCenter.Geo.Location import Location
from DataCenter.Geo import geoutils

class Region():
  '''
  Defines the region class. A region is defined as
  by a central Location class and a range (describing the radius
  of the surrounding area, in units).

  TODO: support 'miles' and 'km'
  '''
  def __init__(self, coord, name, radius, unit='km', description=None):
    '''
    Initializes the Region class around the center with
    the specified radius
    '''
    self.center = Location(name, coord[0], coord[1])
    self.radius = radius
    self.description = description
    self.name = name

  def includes(self, coord):
    '''
    Returns True if the coordinate is within the region,
    False otherwise
    '''
    return geoutils.distance(self.center, coord) < self.radius

  def setCenter(self, coord):
    '''
    Moves the center location to the specified new location
    '''
    self.center.move(coord)

  def setRadius(self, radius):
    '''
    Sets the new radius of the region
    '''
    self.radius = radius

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

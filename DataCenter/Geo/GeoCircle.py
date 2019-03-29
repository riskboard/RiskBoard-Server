from DataCenter.Geo.Location import Location
from DataCenter.Geo.Geography import Geography
from DataCenter.Geo import geoutils

class GeoCircle(Geography):
  '''
  Defines the GeoCircle class. A GeoCircle is defined as
  by a central Location class and a range (describing the radius
  of the surrounding area, in units).

  TODO: support 'miles' and 'km'
  TODO: Interface with MongoDB
  '''
  def __init__(self, center, radius, **kwds):
    '''
    Initializes the Region class around the center with
    the specified radius
    '''
    super().__init__(**kwds)
    self.radius = radius
    self.center = Location(self.name, center[0], center[1])

  def includes(self, location):
    '''
    Returns True if the coordinate is within the region,
    False otherwise
    '''
    return geoutils.distance(self.center, (location.latitude, location.longitude)) < self.radius

  def setCenter(self, coord):
    '''
    Moves the center location to the specified new location
    '''
    self.center.move(coord[0], coord[1])

  def setRadius(self, radius):
    '''
    Sets the new radius of the region
    '''
    self.radius = radius

  def _serialize(self, format='bson'):
    '''
    Serializes the GeoCircle class
    '''
    main = super()._serialize()
    main['radius'] = self.radius
    main['center'] = self.center._serialize()
    return main
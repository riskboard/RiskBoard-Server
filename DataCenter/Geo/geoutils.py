import geopy.distance

def distance(coord1, coord2):
  '''
  Calculates the distance between two lat-long coordinates
  in kilometers

  TODO: support other units
  '''
  return geopy.distance.vincenty(coord1, coord2)
from DataCenter.Geo.Location import Location

class GDeltLocation(Location):
  '''
  Implements the GDeltLocation class, which
  creates a location based on the information given in
  GDelt GKG

  TODO: Interface with MongoDB
  '''
  def __init__(self, type, **kwds):
    type_dict = {
      '1': 'COUNTRY',
      '2': 'USSTATE',
      '3': 'USCITY',
      '4': 'WORLDCITY',
      '5': 'WORLDSTATE'
    }
    self.type = type_dict[type]
    super().__init__(**kwds)

  def _serialize(self, format='bson'):
    '''
    Serializes the GDelt Location
    '''
    main = super()._serialize()
    main['type'] = self.type
    return main
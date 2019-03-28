class SE():
  '''
  Defines a success and error class.
  This catches bugs and allows for storage of errors.
  '''
  def __init__(self, success=True, errors=[]):
    '''
    Initializes an SE class. Default is True and empty list
    '''
    self.success = success
    self.errors = errors

  def updateSE(self, SE):
    self.success = SE.success and self.success
    if len(SE.errors): self.errors += SE.errors
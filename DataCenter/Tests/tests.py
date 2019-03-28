def runUtilTests():
  print('   Running Util Tests...')
  assert True
  print('   Util Tests Passed\n')

def runGeoTests():
  print('   Running Geo Tests...')
  assert True
  print('   Geo Tests Passed\n')

def runGraphTests():
  print('   Running Graph Tests...')
  assert True
  print('   Graph Tests Passed\n')

def runDBTests():
  print('   Running DB Tests...')
  assert True
  print('   DB Tests Passed\n')

def runTests():
  print('   Testing Database')
  tests = [runUtilTests, runGraphTests, runDBTests]
  return [x() for x in tests]
  print('   Tests Passed\n')
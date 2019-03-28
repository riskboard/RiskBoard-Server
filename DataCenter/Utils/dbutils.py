from fuzzywuzzy import fuzz
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def getDateTimeObject(date):
  '''
  Creates a datetime object corresponding to a specified date string
  Dates should be formatted as follows:
  'YYYY MM DD'
  e.g. '2019 02 19'
  '''
  return datetime.strptime(date, '%Y %m %d')

def getDateStringList(dateObject, interval=15):
  '''
  Converts a given date into a string.

  Dates should be formatted as follows:
  'YYYY MM DD'
  e.g. '2019 02 19'

  Output:
  ['YYYYMMDD000000', 'YYYYMMDD001500', ..., 'YYYYMMDD234500']
  Default corresponds to the 15-minute intervals of a given day
  for access in the GDelt GKG 2.0
  '''
  # generate numbers
  timeNums = np.arange(0, 236000, interval*100)
  # generate dateString
  dateString = dateObject.strftime("%Y%m%d")
  # return as a list of formatted strings
  return [f'{dateString}{timeNum:06}' for timeNum in timeNums]

def dateRange(startDateObject, endDateObject):
  '''
  Creates an iterable of dates corresponding to
  given start date object and end date object, inclusive.
  '''
  for n in range(int ((endDateObject - startDateObject).days)):
    yield startDateObject + timedelta(n)

def getDateRangeStrings(startDate, endDate):
  '''
  Creates a list of strings, corresponding to 15-minute intervals
  from the specified start date to end date, inclusive of the first,
  exclusive of the second
  '''
  startDateObject = getDateTimeObject(startDate)
  endDateObject = getDateTimeObject(endDate)
  output = []
  for date in dateRange(startDateObject, endDateObject):
    output += getDateStringList(date)
  return output

def getDateURL(dateString):
  '''
  Returns the corresponding GDelt 2.0 GKG URL
  '''
  return f'http://data.gdeltproject.org/gdeltv2/{dateString}.translation.gkg.csv.zip'

def getSchemaHeaders(schema='DataCenter/Utils/schema.csv'):
  return list(pd.read_csv(schema, sep='\t', header=None)[0].values)

def formatActors(actors):
  '''
  Takes in a list of actors, and returns a lowercase, non-divided version of their name
  '''
  if not actors: return None
  return list(map(lambda x: x.lower(), actors))

def findSimilarity(string1, string2):
  '''
  Finds the similarity between two given strings
  TODO: Think about optimization with a large amount of relevant actors
  '''
  return fuzz.token_set_ratio(string1, string2)

def updateSE(SE, newSE):
  '''
  Updates Success and Errors
  '''
  SE[0] = newSE[0] and SE[0]
  if newSE[1]: SE[1] += newSE(1)
  return SE
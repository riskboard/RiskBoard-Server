import pandas as pd
from geopy.point import Point

from DataCenter.DataCenter import DataCenter
from DataCenter.Geo.GeoRectangle import GeoRectangle

if __name__ == '__main__':
  start_date = input('Desired Start Date: ')
  end_date = input('Desired End Date:   ')

  """
  Brazil Sample
  """
  # get brazilian actors
  brDf = pd.read_csv('Scenarios/br_cham_legislators.csv')
  actors = list(brDf.legislator_name)
  north = Point.parse_degrees(5, 16, 27.8, 'N')
  south = Point.parse_degrees(33, 45, 4.21, 'S')
  east = Point.parse_degrees(34, 47, 35.33, 'W')
  west = Point.parse_degrees(73, 58, 58.19, 'W')
  brazil = GeoRectangle(boundaries=(north, south, east, west), name='Brazil')

  print('***INITIALIZING DATA CENTER***')
  db = DataCenter(start_date, end_date, geographies=[brazil], relevantActors=actors)
  print('Finished Initializing\n')

  print('Visualizing DataCenter...')
  db.visualizeGraph()
  print('Finished Visualizing\n')


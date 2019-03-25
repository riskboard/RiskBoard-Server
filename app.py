import pandas as pd

from DataCenter.DataCenter import DataCenter

if __name__ == '__main__':
  start_date = input('Desired Start Date: ')
  end_date = input('Desired End Date:   ')

  """
  Brazil Sample
  """
  # get brazilian actors
  brDf = pd.read_csv('Scenarios/br_cham_legislators.csv')
  actors = list(brDf.legislator_name)

  print('***INITIALIZING DATA CENTER***')
  db = DataCenter(start_date, end_date, relevantActors=actors)
  print('Finished Initializing\n')

  print('Visualizing DataCenter...')
  db.visualizeGraph()
  print('Finished Visualizing\n')


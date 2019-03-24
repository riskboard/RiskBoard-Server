from DataBase.database import DataBase

if __name__ == '__main__':
  start_date = input('Desired Start Date: ')
  end_date = input('Desired End Date:   ')

  print('***INITIALIZING DATABASE***')
  db = DataBase(start_date, end_date)
  print('Finished Initializing...\n')

  print('Visualizing Database...')
  db.visualizeGraph()
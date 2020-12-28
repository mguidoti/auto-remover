import os, logging
from datetime import datetime
from pathlib import Path

from config import path, days


def main():

  global count_deleted_files
    
  for root, folders, files in os.walk(path):
    
    
    for file in files:
      
      file_ctime = Path(root, file).stat().st_ctime
      
      if curr_time_cut >= file_ctime:
        logging.warning('FILE REMOVED (OLD): {}, created at {}'.format(file, datetime.fromtimestamp(file_ctime).strftime('%Y-%m-%d %H:%M:%S')))
        Path(root, file).unlink()
        count_deleted_files += 1
        
        if len(os.listdir(root)) == 0:
          remove_folder(Path(root))
        
      # else:
      #   next
    
       
    for folder in folders:   
        # if folder exists
      remove_folder(Path(root, folder))
    
    # for root, folders, files in os.walk(path):
      

def remove_folder(folder):
  
  global count_deleted_old_folders, count_deleted_empty_folders
  
  folder_ctime = folder.stat().st_ctime
    
  if curr_time_cut >= folder_ctime:
    folder.rmdir()
    logging.warning('FOLDER REMOVED (OLD): {}, created at {}'.format(str(folder).replace(str(path), ''), datetime.fromtimestamp(folder_ctime).strftime('%Y-%m-%d %H:%M:%S')))
    count_deleted_old_folders += 1
        
  elif len(os.listdir(str(folder))) == 0:
    folder.rmdir()
    logging.warning('FOLDER REMOVED (EMPTY): {}'.format(str(folder).replace(str(path), '')))
    count_deleted_empty_folders += 1
    
    if str(folder.parent) != path:
      remove_folder(folder.parent)
    

if __name__ == '__main__':
  
  curr_time_cut = datetime.now().timestamp() - (days * 24 * 60 * 60)
   
  log_name = datetime.today().strftime('%Y%m%d')
  
  logging.basicConfig(handlers = [logging.FileHandler(
                                    filename = 'logs/{}.log'.format(log_name), 
                                    encoding='utf-8')], 
                      level = logging.DEBUG)
  
  # initializing the count
  count_deleted_old_folders = 0
  count_deleted_empty_folders = 0
  count_deleted_files = 0
  
  main()
  
  logging.info('A total of {} old files, {} old and {} empty folders were removed.'.format(count_deleted_files, count_deleted_old_folders, count_deleted_empty_folders))
  
  
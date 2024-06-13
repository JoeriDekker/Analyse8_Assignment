import zipfile
import shutil
import os
import datetime as datetime

DB_PATH = 'assignment.db'
LOG_PATH = 'log.txt'
BACKUP_PATH_TEMP = 'backup_temp'
BACKUP_PATH = 'backups'
BACKUP_NAME = f'backup-test'
# BACKUP_NAME = f'backup-test-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}

class BackupFunc:

    def CreateBackup():
        # Create backup folder if it doesn't exist
        if not os.path.exists(BACKUP_PATH_TEMP):
            os.makedirs(BACKUP_PATH_TEMP)

        if not os.path.exists(BACKUP_PATH):
            os.makedirs(BACKUP_PATH)

        # Copy DB file to backup folder
        shutil.copy(DB_PATH, BACKUP_PATH_TEMP)
        shutil.copy(LOG_PATH, BACKUP_PATH_TEMP)

        # Zip the backup folder and put in the backups folder
        shutil.make_archive(BACKUP_NAME, 'zip', BACKUP_PATH_TEMP)

        # Remove the backup folder
        shutil.rmtree(BACKUP_PATH_TEMP)

        # Place backup in backups folder
        shutil.move(f'{BACKUP_NAME}.zip', BACKUP_PATH)

    def RestoreBackup():
        # Unpack the backup from the backups folder
        with zipfile.ZipFile(f'{BACKUP_PATH}/{BACKUP_NAME}.zip', 'r') as zip_ref:
            zip_ref.extractall(BACKUP_PATH_TEMP)

        # Copy the files back to the root folder
        shutil.copy(f'{BACKUP_PATH_TEMP}/{DB_PATH}', '.')
        shutil.copy(f'{BACKUP_PATH_TEMP}/{LOG_PATH}', '.')

        # Remove the backup folder
        shutil.rmtree(BACKUP_PATH_TEMP)
        
        
            

       


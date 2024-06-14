import zipfile
import shutil
import os
import datetime as datetime


class BackupFunc:

    def CreateBackup():

        num_files = 0
        print("\n--- Creating Backup...  ---\n")

        # Create backup folder if it doesn't exist
        if not os.path.exists('backup_temp'):
            os.makedirs('backup_temp')

        if not os.path.exists('backups'):
            os.makedirs('backups')

        # Copy DB file to backup folder
        shutil.copy('assignment.db', 'backup_temp')
        shutil.copy('log.txt', 'backup_temp')

        num_files = 0
        if os.path.exists('backups'):
            for file in os.listdir('backups'):
                if file.startswith('system-backup'):
                    num_files += 1

        date = datetime.datetime.now().strftime('%d-%m-%Y')
        # Zip the backup folder and put in the backups folder
        shutil.make_archive(f'system-backup-{date}-{num_files}', 'zip', 'backup_temp')

        # Remove the backup folder
        shutil.rmtree('backup_temp')

        # Place backup in backups folder
        shutil.move(f'system-backup-{date}-{num_files}.zip', 'backups')
        print(f"Backup created successfully: system-backup-{date}-{num_files}")

    def RestoreBackup(file_name):
        print("\n--- Restoring Backup...  ---\n")
        # Unpack the backup from the backups folder
        with zipfile.ZipFile(f'backups/{file_name}', 'r') as zip_ref:
            zip_ref.extractall('backup_temp')

        # Copy the files back to the root folder
        shutil.copy(f'backup_temp/assignment.db', '.')
        shutil.copy(f'backup_temp/log.txt', '.')

        # Remove the backup folder
        shutil.rmtree('backup_temp')
        
        
            

       


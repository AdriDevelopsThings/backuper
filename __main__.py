import logging
from resources import check_for_new_backups, delete_all_not_verified_files

if __name__ == '__main__':
    logging.info("Configuration loaded successful.")
    delete_all_not_verified_files()
    check_for_new_backups()

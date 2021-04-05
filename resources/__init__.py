import logging
from datetime import datetime

from resources.config import configuration
from resources.requesting import get_file_hash, download_file
from hashlib import new
from os import listdir, rename, remove, environ
from os.path import join

TIMESTAMP_STRING = environ.get("BACKUPER_FILE_DATETIME_FORMAT", "%d-%m-%Y-%H-%M-%S")

logging.basicConfig(level=logging.getLevelName(environ.get("BACKUPER_LOGGING_LEVEL", "INFO")))

def get_default_file_realname():
    return configuration["receiver"]["file"].split("/")[-1]


def parse_filename(filename):
    split = filename.split("_")
    if len(split) < 4:
        raise ValueError(
            f"The file {filename} seems to have a wrong filename syntax. If you created the file yourself delete it."
        )
    return (
        int(split[0]),
        datetime.strptime(split[1], TIMESTAMP_STRING),
        "_".join(split[3:]),
    )


def create_filename(counter, timestamp, real_file_name):
    counter = str(counter)
    return f"{counter.zfill(6)}_{timestamp.strftime(TIMESTAMP_STRING)}_backup_{real_file_name}"


def get_current_backup_counter():
    counter = 0
    counter_filename = None
    for file in listdir(configuration["output"]["directory"]):
        if not file.startswith(".") and "_backup_" in file:
            c, d, rfn = parse_filename(file)
            if c > counter:
                counter = c
                counter_filename = file
    return counter, counter_filename


def get_current_backup_file():
    filename = get_current_backup_counter()[1]
    if filename:
        return join(configuration["output"]["directory"], filename)


def calculate_file_hash(file):
    h = new(configuration["receiver"]["hash_algorithm"])
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def check_for_new_backups():
    online_file_hash = get_file_hash()
    current_file_hash = None
    current_backup_file = get_current_backup_file()
    if current_backup_file:
        current_file_hash = calculate_file_hash(current_backup_file)
    if online_file_hash != current_file_hash:
        fetch_new_backup(online_file_hash)


def fetch_new_backup(current_online_hash):
    filename = join(
        configuration["output"]["directory"],
        create_filename(
            get_current_backup_counter()[0] + 1,
            datetime.now(),
            get_default_file_realname() + ".not.verified",
        ),
    )
    logging.info("Download new backup...")
    download_file(filename)
    logging.info("Verification...")
    file_hash = calculate_file_hash(filename)
    if file_hash != current_online_hash:
        logging.error(f"File verification failed for {filename[:-13]}.")
        logging.error("Online hash: " + current_online_hash)
        logging.error("File hash: " + file_hash)
    else:
        rename(filename, filename[:-13])
        logging.info("File verification finished successful.")
    logging.info(f"Downloading backup {filename[:-13]} finished")


def delete_all_not_verified_files():
    for file in listdir(configuration["output"]["directory"]):
        if file.endswith(".not.verified"):
            remove(join(configuration["output"]["directory"], file))
            logging.warn(f"Removed {file} because the file is not verified.")

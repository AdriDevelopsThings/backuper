import logging
from os import environ, mkdir
from json import load
from os.path import exists
from traceback import print_exc

CONFIG_PATH = environ.get("BACKUPER_CONFIG_PATH", "config.json")
configuration = None


def validate_configuration(configuration):
    try:
        assert "receiver" in configuration and configuration["receiver"]
        assert "file" in configuration["receiver"] and configuration["receiver"]["file"]
        assert "hash_algorithm" in configuration["receiver"] and configuration["receiver"]["hash_algorithm"]
        assert (
            "file_hash" in configuration["receiver"]
            and configuration["receiver"]["file_hash"]
        )
        if (
            "auth" in configuration["receiver"]
            and configuration["receiver"]["auth"] is not None
        ):
            if (
                "http_auth" in configuration["receiver"]["auth"]
                and configuration["receiver"]["auth"]["http_auth"]
            ):
                assert (
                    "username" in configuration["receiver"]["auth"]["http_auth"]
                    and "password" in configuration["receiver"]["auth"]["http_auth"]
                    and configuration["receiver"]["auth"]["http_auth"]["username"]
                    and configuration["receiver"]["auth"]["http_auth"]["password"]
                )
            if (
                "client_certificate" in configuration["receiver"]["auth"]
                and configuration["receiver"]["auth"]["client_certificate"]
            ):
                assert (
                    "cert" in configuration["receiver"]["auth"]["client_certificate"]
                    and "key" in configuration["receiver"]["auth"]["client_certificate"]
                    and configuration["receiver"]["auth"]["client_certificate"]["cert"]
                    and configuration["receiver"]["auth"]["client_certificate"]["key"]
                )

        assert "output" in configuration and configuration["output"]
        assert (
            "directory" in configuration["output"]
            and configuration["output"]["directory"]
        )
        if not exists(configuration["output"]["directory"]):
            mkdir(configuration["output"]["directory"])

    except AssertionError as exception:
        logging.critical(
            "The configuration file is invalid. Please read the documentation or the config.py file in the line of "
            "the exception. " + str(exception)
        )
        print_exc()


def read_configuration_from_disk(filename):
    with open(filename, "r") as j_file:
        return load(j_file)


def load_config():
    global configuration
    configuration = read_configuration_from_disk(CONFIG_PATH)
    validate_configuration(configuration)


load_config()

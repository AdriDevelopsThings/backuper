import logging
from time import sleep
from traceback import print_exc

import requests
from progressbar import ProgressBar

from resources.config import configuration


def get_auth_parameters():
    parameters = {}
    if "auth" in configuration["receiver"] and configuration["receiver"]["auth"]:
        if (
            "http_auth" in configuration["receiver"]["auth"]
            and configuration["receiver"]["auth"]["http_auth"]
        ):
            parameters["auth"] = (
                configuration["receiver"]["auth"]["http_auth"]["username"],
                configuration["receiver"]["auth"]["http_auth"]["password"],
            )
        if (
            "client_certificate" in configuration["receiver"]["auth"]
            and configuration["receiver"]["auth"]["client_certificate"]
        ):
            parameters["cert"] = (
                configuration["receiver"]["auth"]["client_certificate"]["cert"],
                configuration["receiver"]["auth"]["client_certificate"]["key"],
            )
        if (
            "get_parameters" in configuration["receiver"]["auth"]
            and configuration["receiver"]["auth"]["get_parameters"]
        ):
            parameters["params"] = configuration["receiver"]["auth"]["get_parameters"]
        if (
            "headers" in configuration["receiver"]["auth"]
            and configuration["receiver"]["auth"]["headers"]
        ):
            parameters["headers"] = configuration["receiver"]["auth"]["headers"]

        if (
            "ca_file" in configuration["receiver"]
            and configuration["receiver"]["ca_file"]
        ):
            parameters["verify"] = configuration["receiver"]["ca_file"]
    return parameters


def handle_request_errors(e, target, args=None):
    if not args:
        args = ()
    logging.error("Error occurred while fetching file hash: " + str(e))
    print_exc()
    logging.error("Retrying in 30 seconds...")
    sleep(30)
    logging.info("Retry getting file hash.")
    target(*args)


def get_file_hash():
    try:
        response = requests.get(
            configuration["receiver"]["file_hash"], **get_auth_parameters()
        )
        response.raise_for_status()
        return response.text.replace("\n", "").replace("\t", "")
    except Exception as e:
        handle_request_errors(e, get_file_hash)


def download_file_range(
    request_args,
    request_kwargs,
    opend_file,
    from_range,
    progressbar,
    content_length,
    current_loaded_data,
):
    if "headers" in request_kwargs:
        request_kwargs["headers"]["Range"] = f"bytes={from_range}-"
    else:
        request_kwargs["headers"] = {"Range": f"bytes={from_range}-"}
    request_kwargs["stream"] = True
    response = requests.get(*request_args, **request_kwargs)
    response.raise_for_status()
    if not content_length:
        content_length = int(response.headers.get("content-length", 0))
        progressbar.max_value = content_length
    block_size = 1024
    for data in response.iter_content(block_size):
        current_loaded_data = len(data) + progressbar.value
        progressbar.update(current_loaded_data)
        opend_file.write(data)
    del response
    if current_loaded_data != content_length:
        return download_file_range(
            request_args,
            request_kwargs,
            opend_file,
            current_loaded_data,
            progressbar,
            content_length,
            current_loaded_data,
        )
    opend_file.close()


def download_file(output_path):
    try:
        progress_bar = ProgressBar()
        download_file_range(
            (configuration["receiver"]["file"],),
            {"stream": True, **get_auth_parameters()},
            open(output_path, "wb"),
            0,
            progress_bar,
            None,
            0,
        )
        progress_bar.finish()
    except Exception as e:
        handle_request_errors(e, download_file, args=(output_path,))

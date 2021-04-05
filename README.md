# Backuper
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

Download your backups automatically.

# Installation

You need python 3.6 with pip.
Install it on ubuntu with:
``sudo apt install python3.7 python3-pip``

## Configuration
### Environment Variables
```shell
# The path of the config file
# Default: config.json
BACKUPER_CONFIG_PATH=/the/path/of/the/config/file.json
# The datetime format of the filename, see here: https://www.programiz.com/python-programming/datetime/strftime
# WARNING: The datetime format must not contain '_' otherwise the app would crash.
BACKUPER_FILE_DATETIME_FORMAT=%d-%m-%Y-%H-%M-%S
# The level of the logging service (python logging module).
# The level can be: CRITICAL, FATAL, ERROR, WARN, WARNING, INFO or DEBUG
BACKUPER_LOGGING_LEVEL=INFO
```  
The config file should have the json format.

### Config file

```json
{
  "receiver": {
    "file": "https://the.url.of.the/downloading_file.bin",
    "file_hash": "https://the.url.of.the/downloading_file.bin.sha256sum",
    "hash_algorithm": "sha256",
    "auth": {
      "http_auth": {
        "username": "the username",
        "password": "the password"
      },
      "client_certificate": {
        "cert": "the/path/of/the/client/certificate/cert.pem",
        "key": "the/path/of/the/client/certificate/privkey.key",
      },
      "get_parameters": {
        
      },
      "headers": {
        
      }
    },
    "ca_file": "the/path/to/the/certificate/authority/certificate.pem"
  },
  "output": {
    "directory": "/the/directory/of/the/backup/files"
  }
}
```
Please remove all parts of the file, that you are not using, otherwise the application would bring an error.
So if you are not using the client_certificate authentication or other things remove it.

# Functionality

When you start the app, the app does make a request to the file_hash uri and will compare the hash with the hash of the current backup file.
If the hashes are different, the app will download the new backup file (file uri) in the data directory. The filename would have the following syntax:
`{6-digit-number}_%d-%m-%Y-%H-%M-%S_backup_{real_file_name}`.  
The file does have the suffix `.not.verified`. When the download is finished and file hash check is successful the suffix will be removed.

# Contributing
You can open a **Issue**, when you have a problem or an idea. Please describe all things detailed.

When you want to solve your Issue yourself, fork the repository and make the change in your repository.
When you checked the functionality of your change you can create a pull request to the `master` or `development` branch of this repository.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://adridoesthings.com"><img src="https://avatars.githubusercontent.com/u/45321107?v=4?s=100" width="100px;" alt=""/><br /><sub><b>AdriDevelopsThings</b></sub></a><br /><a href="https://github.com/AdriDevelopsThings/backuper/commits?author=AdriDevelopsThings" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
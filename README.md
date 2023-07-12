# lemmy_backup
A script to backup from one lemmy instance to a file.

Version 0.1 support only serialization of communities from one instance to a
file, in the future I plan to add the ability to import the file into another
instance (i.e. subscribing to the saved communities). I also plan to support
backup of other data depending on what is available through Lemmy API.

## Dependencies

This script depends on plemmy API. See [PLemmy project page](https://github.com/tjkessler/plemmy)
for details on how to install it.

## Usage

```
usage: lemmybackup.py [-h] [-e EXPORT] [--communities] [--profile] instance username password

Allows to backup various lemmy data, like subscribed communities. Output on stdout in human-readable format. Use --export option to generate a json file.

positional arguments:
  instance              Lemmy instance url (i.e. https://lemmy.ml)
  username              Lemmy username
  password              Lemmy password

optional arguments:
  -h, --help            show this help message and exit
  -e EXPORT, --export EXPORT
                        Export data to file. Location must be write-able.

Backup Data:
  Data to backup (if none specified, all will be saved)

  --communities         Backup subscribed communities
  --profile             Backup profile data (bio)
```

Output list of subscribed communities and user bio on stdout. `--export` allows
to generate a json file with the same output as on console.

TODO: The goal will be to provide a script to allow importing this data in another lemmy instance.

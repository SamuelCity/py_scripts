# py_scripts
A small collection of Python scripts that can help day to day work.

## Setup
These scripts were built using Python 3.11 and use pipenv for dependency management. Once you've cloned this repo down you can get all the dependencies by running `pipenv install`.

## Scripts
Below you will find a list of scripts, with their options and what they do.

### `log_level`
This script allows you to easily change the log level of and services running in our Kubernetes cluster. The script takes three arguments.

- `-s --service`: The name of the service you wish to change log level. `<required>`
- `-n --namespace`: The namespace the service is in. `<required>`
- `-l --logger`: The logger you wish to change the level of, this default to `com.gocity`.

Upon running the script you'll be prompted to change the log level to one of a few options. Once you select an option the script will port forward to each pod for you and change the log level.

This script is intended for use with Spring Boot Applications and will change the level of the `com.gocity` logger unless the `-l` option is provided.

If the log level is changed successfully you'll see a `204` message in the output.

## Aliases
If you wish to create bash/zsh aliases for these scripts, to make them easier to run, you can do so with the following function definitions in your `.zshrc` or `.bash_profile`

```
log_level() {
    pipenv run python /path/to/folder/log_level.py "$@"
}
```

Replace `/path/to/folder` with the location of this repository on your machine.
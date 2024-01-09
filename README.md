# typeFileTransfer
Transfer binary file via shell.
Last resort when everything is blocked except the shell.

## Mechanism
1. Convert binary file into base64 string
1. By using macro functions typeFileTransfer automatically type the base64 string to a separate console/shell
1. The (very long) base64 string can be splitted into predefined length of strings by a parameter (`--text-chunk-size`)
1. The delay between typing 1) each character and 2) echo commands can be specified by parameters (`--inter-char-delay` and `--inter-echo-delay`)

## How to run
1. `python3`, `python3-pip`, and `python3-venv` should be installed first
1. `$ python3 -m venv venv`
1. `$ source venv/bin/activate`
1. `$ cat pip-requirements | xargs -n 1 python3 -m pip install`
1. `(venv) $ python3 typeFileTransfer.py [OPTIONS] FILEPATH`
1. The countdown is diaplayed. Click the terminal to type the base64 string before it ends.
1. Do not touch the PC until the transfer is complete

## Synopsis
```
Usage: typeFileTransfer.py [OPTIONS] FILEPATH

Options:
  --logging-level [DEBUG|INFO|WARNING|ERROR]
                                  logging level for the logger  [default:
                                  INFO]
  --pre-typing-delay INTEGER      delay in seconds before actual typing
                                  simulation  [default: 5]
  --inter-char-delay FLOAT        delay inserted between each typing of a
                                  letter  [default: 0.005]
  --inter-echo-delay FLOAT        delay inserted between each 'echo' command
                                  [default: 0.1]
  --text-chunk-size INTEGER       max size of text chunk for one echo. 12
                                  chars are a unit. -1 means sending the whole
                                  file in one string.  [default: -1]
  --help                          Show this message and exit.
```

## How to recover initial binary file
Use base64 converter supported by OS
* Windows: `$ certutil -decode SENT_BINARY.base64 SENT_BINARY`
* Linux: `$ base64 -d -i SENT_BINARY.base64 > SENT_BINARY`
* macOS: `$ base64 -D -i SENT_BINARY.base64 -o SENT_BINARY`

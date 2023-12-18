import pyautogui
import time
import click
import sys
import base64
import logging
from setup_logger import setup_logger

LOGGERNAME = 'typeFileTransfer_logger'

def simulateTyping(text: str) -> None:
    logger = logging.getLogger(LOGGERNAME)
    logger.debug('typing simulation start')
    pyautogui.typewrite(text)
    logger.debug('typing simulation end')

def printCountDown(time2wait: int) -> None:
    logger = logging.getLogger(LOGGERNAME)

    logger.debug('checking time2wait > 0')
    assert time2wait > 0
    logger.debug('time2wait > 0 proceeding')

    logger.debug('countdown start')
    for timeRemaining in range(time2wait, 0, -1):
        sys.stdout.write(f'{timeRemaining}...\r')
        time.sleep(1)
    logger.debug('countdown end')

    print('')

def getBase64Chunk(filepath: str, text_chunk_size: int = -1) -> str:
    logger = logging.getLogger(LOGGERNAME)

    with open(filepath, 'rb') as fp:
        while True:
            if text_chunk_size < 0:
                chunkRead = base64.b64encode(fp.read()).decode('UTF-8')
            else:
                chunkRead = base64.b64encode(fp.read(text_chunk_size * 12)).decode('UTF-8')

            if chunkRead == '':
                break
            else:
                yield chunkRead

@click.command()
@click.option(
    '--logging-level',
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False),
    default='INFO',
    show_default=True,
    help='logging level for the logger'
)
@click.option(
    '--delay-in-seconds',
    type=click.INT,
    default=5,
    show_default=True,
    help='delay in seconds before actual typing simulation'
)
@click.option(
    '--text-chunk-size',
    type=click.INT,
    default=-1,
    show_default=True,
    help='max size of text chunk for one echo. 12 chars are a unit. -1 means sending the whole file in one string.'
)
@click.argument(
    'filepath',
    type=click.Path(exists=True, dir_okay=False),
    nargs=1
)
def main(
    logging_level,
    delay_in_seconds,
    text_chunk_size,
    filepath
):
    logger = setup_logger(LOGGERNAME, logging_level)

    print(f'Typing simulation will start in {delay_in_seconds} seconds.\n'
          'Move cursor to the shell to input text, now!')
    printCountDown(delay_in_seconds)

    for base64Chunk in getBase64Chunk(filepath, text_chunk_size=text_chunk_size):
        #print(base64Chunk)
        simulateTyping('echo \'' + base64Chunk + '\'\r')

if __name__ == '__main__':
    main()

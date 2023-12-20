import pyautogui
import time
import click
import sys
import base64
import logging
import os
from setup_logger import setup_logger

LOGGERNAME = 'typeFileTransfer_logger'

def simulateTyping(text: str, inter_char_delay: float) -> None:
    logger = logging.getLogger(LOGGERNAME)

    logger.debug('checking inter_char_delay > 0')
    assert inter_char_delay > 0
    logger.debug('inter_char_delay > 0 proceeding')

    logger.debug('typing simulation start')
    pyautogui.write(text, interval=inter_char_delay)
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
    '--pre-typing-delay',
    type=click.INT,
    default=5,
    show_default=True,
    help='delay in seconds before actual typing simulation'
)
@click.option(
    '--inter-char-delay',
    type=click.FLOAT,
    default=0.005,
    show_default=True,
    help='delay inserted between each typing of a letter'
)
@click.option(
    '--inter-echo-delay',
    type=click.FLOAT,
    default=0.1,
    show_default=True,
    help='delay inserted between each \'echo\' command'
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
    pre_typing_delay,
    inter_char_delay,
    inter_echo_delay,
    text_chunk_size,
    filepath
):
    logger = setup_logger(LOGGERNAME, logging_level)

    logger.debug('checking inter_echo_delay > 0')
    assert inter_echo_delay > 0
    logger.debug('inter_echo_delay > 0. proceeding')


    print(f'Typing simulation will start in {pre_typing_delay} seconds.\n'
          'Move cursor to the shell to input text, now!')
    printCountDown(pre_typing_delay)

    fileSizeInBytes = os.stat(filepath).st_size
    numChunk = 0
    for base64Chunk in getBase64Chunk(filepath, text_chunk_size=text_chunk_size):
        simulateTyping('echo -n \'' + base64Chunk + f'\' >> {os.path.basename(filepath)}.base64\r', inter_char_delay)
        numChunk += 1
        sys.stdout.write(f'Progress: {numChunk*(text_chunk_size*9):10d}/{fileSizeInBytes}\r')
        time.sleep(inter_echo_delay)
    simulateTyping(f'echo \'\' >> {os.path.basename(filepath)}.base64\r', inter_echo_delay)
    sys.stdout.write(f'Progress: {fileSizeInBytes:10d}/{fileSizeInBytes}\n')

if __name__ == '__main__':
    main()

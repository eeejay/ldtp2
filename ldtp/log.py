from os import environ as env
import logging

AREA = 'ldtp.client'
ENV_LOG_LEVEL = 'LDTP_LOG_LEVEL'
ENV_LOG_OUT = 'LDTP_LOG_OUT'

log_level = getattr(logging, env.get(ENV_LOG_LEVEL, 'NOTSET'), logging.NOTSET)

logger = logging.getLogger(AREA)

if not env.has_key(ENV_LOG_OUT):
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(name)-11s %(levelname)-8s %(message)s'))
else:
    handler = logging.FileHandler(env[ENV_LOG_OUT])
    handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))

logger.addHandler(handler)

logger.setLevel(log_level)

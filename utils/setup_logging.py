import os
import logging

logger = logging.getLogger(__name__)

formatter = logging.Formatter("%(asctime)s -"
                              " %(levelname)s -"
                              " %(name)s"
                              " %(message)s")
file_handler = logging.FileHandler(filename=os.path.join(*[os.getcwd(),
                                                           'config',
                                                           'logging.log']))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

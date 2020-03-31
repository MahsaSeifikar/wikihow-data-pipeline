import os
import logging

logger = logging.getLogger(__name__)

formatter = logging.Formatter("%(asctime)s -"
                              " %(levelname)s -"
                              " %(name)s"
                              " %(message)s")
abs_path = os.path.dirname(os.path.dirname(os.getcwd()))
file_handler = logging.FileHandler(filename=os.path.join(*[abs_path,
                                                           'config',
                                                           'logging.log']))

# file_handler = logging.FileHandler(filename='/config/logging.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

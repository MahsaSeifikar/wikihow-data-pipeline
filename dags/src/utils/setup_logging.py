import os
import logging

def get_costum_logger(logger):
    formatter = logging.Formatter("%(asctime)s -"
                                " %(levelname)s -"
                                " %(name)s"
                                " %(message)s")

    abs_path = '/wikihow_data_pipeline'
    file_handler = logging.FileHandler(filename=os.path.join(*[abs_path,
                                                            'data',
                                                            'log',                                                           
                                                            'logging.log']))

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger

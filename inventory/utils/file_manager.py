import json
import logging

logger = logging.getLogger(__name__)


class FileManager:
    def __inti__(self):
        pass

    @classmethod
    def read_json(cls, file_path):
        file_data = {}
        try:
            logger.info("Reading file {0}".format(file_path))
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if content:
                    file_data = json.loads(content)
                    logger.info("File read done")
                else:
                    logger.info("No file data")
        except Exception as e:
            logger.warning("Exception: {0}".format(str(e)))

        return file_data
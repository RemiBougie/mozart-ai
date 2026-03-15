import os
import logging
import datetime
import time
from uuid import uuid4
from elasticsearch import Elasticsearch


class ElasticsearchLogHandler(logging.Handler):
    def __init__(self, es_host=os.getenv("ELASTICSEARCH_HOST"), es_port=int(os.getenv("ELASTICSEARCH_PORT")), index_name='app-logs'):
        try:
            super().__init__()

            for i in range(10):
                try:
                    self.es = Elasticsearch([{"host": es_host, "port": es_port, "scheme": "http"}])

                    if self.es.ping():
                        break
                    
                except Exception as e:
                    time.sleep(2)

            self.index = index_name
        except ValueError as e:
            print(f"Error initializing Elasticsearch logger: {e}")

    def emit(self, record):
        log_entry = self.format(record)
        try:
            doc_id = str(uuid4()) # this probably isn't needed
            document = {
                    "@timestamp": datetime.datetime.now(),
                    "level": record.levelname,
                    "logger": record.name,
                    "message": record.getMessage(),
                    "pathname": record.pathname,
                    "lineno": record.lineno,
                    "funcName": record.funcName,
                    "process": record.process,
                    "thread": record.threadName,
                }
            
            self.es.index(
                index=self.index,
                id=doc_id,
                document=document)
        except ValueError as e:
            print(f"Failed to send log to Elasticsearch: {e}")

def get_logger(name=None):
    logger = logging.getLogger(name)

    if getattr(logger, "_is_configured", False):
        return logger

    debug_mode = os.getenv("DEBUG", "false").lower() == "true"
    log_level = logging.DEBUG if debug_mode else logging.INFO
    logger.setLevel(log_level)

    # set up console handler with formatting only if in debug mode
    if debug_mode:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        logger.addHandler(console_handler)

    es_handler = ElasticsearchLogHandler()
    logger.addHandler(es_handler)

    logger._is_configured = True
    return logger
import logging
from elasticsearch import Elasticsearch


class ElasticSearchHandler(logging.Handler):
    def __init__(self, es: Elasticsearch, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.es = es

    def emit(self, record: logging.LogRecord) -> None:
        log_entry = self.format(record)
        self.es.index(index="BackendPetLogs", body={"message": log_entry})


class LoggerSetup:
    def __init__(self) -> None:
        self.logger = logging.getLogger('')
        self.setup_logging()

    def setup_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        )

        es = Elasticsearch("http://localhost:9200")
        es_handler = ElasticSearchHandler(es)
        es_handler.setLevel(logging.INFO)
        self.logger.addHandler(es_handler)


if __name__ == "__main__":
    logger_setup = LoggerSetup()
    logger = logger_setup.logger
    logger.info("This is a test log message.")

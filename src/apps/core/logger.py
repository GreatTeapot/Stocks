
import json
import logging
import os
import re
from logging import LogRecord
from typing import Any, TypeAlias, Union

import yaml

LoadData: TypeAlias = dict[
    str, Union[int, bool, dict[str, dict[str, Union[str, None, bool]]]]
]


class LoggerConfig:

    """
    Class for configuring logging.
    This class loads logging settings from a YAML file and checks the existence 
    of the required directory and files for logs, creating them if necessary.
    """
    @staticmethod
    def __load_config() -> LoadData:
        """Load .yml file"""
        with open("core/log_config.yml", "r") as config:
            return yaml.safe_load(config)
    @classmethod
    def execute_config(cls) -> LoadData:

        """
        Set logging configuration.
        Additionally, check if the directory and the file where logs will be 
        recorded exist. Create them if they do not exist.
        """
        # Increase the logging level for watchfiles.main to avoid log spam 
        # and prevent system overload due to it.
        logger = logging.getLogger("watchfiles.main")
        logger.setLevel(logging.WARNING)

        if os.path.exists("logs/app.log"):
            return cls.__load_config()
        # This check is related to Docker. Docker creates the logs directory 
        # when the application is deployed because of the volume name, 
        # so it's only necessary to create the file.
        elif os.path.exists("src/apps/logs/"):
            open("logs/app.log", "w").close()
            return cls.__load_config()
        else:
            os.mkdir("logs")
            open("logs/app.log", "w").close()
            return cls.__load_config()


class JSONFormatter(logging.Formatter):
    """
    Class for a logging formatter that converts log messages into JSON format.
    This class is used for structuring logs in JSON format, with support for
    specific handling of logs from httpx and uvicorn.
    """

    @staticmethod
    def __httpx_logs(message: str) -> Union[dict[str, str], dict]:
        """Convert data from a string into a dictionary for httpx logs."""
        log_pattern = re.compile(
            r"HTTP Request: (?P<http_method>\w+) (?P<http_protocol>https?)://"
            r"(?P<http_path>\S+) \"(?P<http_version>HTTP/\d\.\d) "
            r"(?P<http_status>\d+) (?P<http_status_message>.+)\""
        )

        match = log_pattern.match(message)
        if match:
            return match.groupdict()
        return {}

    @staticmethod
    def __uvicorn_access_logs(message: str) -> Union[dict[str, str], dict]:
        """Convert data from a string into a dictionary for uvicorn logs."""
        log_pattern = re.compile(
            r"(?P<client_ip>[\d.]+):(?P<client_port>\d+) - \"(?P<http_method>\w+) "
            r"(?P<http_path>\S+) (?P<http_version>HTTP/\d\.\d)\" (?P<http_status>\d+)"
        )
        match = log_pattern.match(message)
        if match:
            return match.groupdict()
        return {}

    @staticmethod
    def __convert_to_dict_if_str_is_json_type(message: str) -> Union[dict[str, Any], str]:
        """Convert a string into a dictionary if it is of JSON type."""
        try:
            return json.loads(message)
        except json.JSONDecodeError:
            return ""

    def format(self, record: LogRecord) -> str:
        """Format log entries."""
        if record.name.__eq__("httpx"):
            message = self.__httpx_logs(record.getMessage())
        elif record.name.__eq__("uvicorn.access"):
            message = self.__uvicorn_access_logs(record.getMessage())
        else:
            message = record.getMessage()

        if isinstance(message, str):
            message = self.__convert_to_dict_if_str_is_json_type(message)
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": message,
            "name": record.name,
            "app": "users",
            "module": record.module,
            "file": record.pathname,
            "line": record.lineno,
            "func": record.funcName,
            "process": record.processName,
            "thread": record.threadName,
        }
        return json.dumps(log_record, ensure_ascii=False, indent=4)


class LoggingFilter(logging.Filter):
    """
    Class for a logging filter.
    This class allows filtering logs based on certain conditions.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter out all messages that are not dictionaries."""
        return bool(record.name in ("root", "uvicorn.access", "httpx"))
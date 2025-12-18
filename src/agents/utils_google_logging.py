'''
File: utils_google_logging.py
Project: adk-data-analytics
File Created: Wednesday, 17th September 2025 5:39:01 pm
Author: Dinesh Selvaraj (dineshselva@google.com)
-------------------------------------------------------------
Last Modified: Friday, 19th September 2025 4:00:57 am
Modified By: Dinesh Selvaraj (dineshselva@google.com>)
-------------------------------------------------------------
Copyright 2025 Google LLC. This software is provided as-is, without
warranty or representation for any use or purpose. Your use of it is
subject to your agreement with Google.
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import logging
import os

# Attempt to import Google Cloud logging client if available
try:
    from google.cloud import logging as google_cloud_logging
    from google.cloud.logging_v2.handlers import CloudLoggingHandler, setup_logging
    from google.cloud.logging_v2.handlers.transports import SyncTransport

    # For local development where the library might not be fully configured
    # or if running outside GCP, it's good to have a fallback.
    client = google_cloud_logging.Client()
    google_logging_available = True
except ImportError:
    client = None
    google_logging_available = False

# Determine log level from environment variable or default to INFO
LOG_LEVEL_STR = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL_STR, logging.INFO)


def get_logger(name: str | None = None, level: int = LOG_LEVEL) -> logging.Logger:
    """
    Configures and returns a logger instance.
    If Google Cloud Logging is available and configured, it adds a CloudLoggingHandler.
    Otherwise, it falls back to a standard stream handler.

    Args:
        name: The name of the logger. Defaults to the root logger if None.
        level: The logging level for this logger.

    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger(name if name else __name__)

    # Prevent duplicate handlers if get_logger is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(level)

    if google_logging_available and client:
        # Add Google Cloud Logging handler
        handler = CloudLoggingHandler(
            client,
            name=name if name else "python_boilerplate_log",
            transport=SyncTransport,
        )
        # setup_logging(handler) # This will exclusively use the Cloud handler
        logger.addHandler(handler)

        # Also add a stream handler for local visibility
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        stream_handler_local = logging.StreamHandler()
        stream_handler_local.setLevel(level)
        stream_handler_local.setFormatter(formatter)
        logger.addHandler(stream_handler_local)
    else:
        # Fallback to standard stream handler if Google Cloud Logging is not available
        formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s [%(name)s] [%(filename)s:%(lineno)d] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        if not google_logging_available:
            logger.info("Google Cloud Logging client library not found or not configured. Using standard stream logger.")
        elif not client:
            logger.info("Google Cloud Logging client could not be initialized (e.g. no ADC). Using standard stream logger.")

    # Prevent log propagation to the root logger if this is a named logger
    # and you want to avoid duplicate messages if the root logger also has handlers.
    if name:
        logger.propagate = False

    return logger

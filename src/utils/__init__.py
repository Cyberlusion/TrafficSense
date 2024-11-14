# Sometimes, you might want certain configurations or setups to happen when the package is imported, such as setting up logging or loading a configuration.

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

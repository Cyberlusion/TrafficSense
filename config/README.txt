Why a Root-Level /config Directory?

    Environment-Specific Configuration: Store configuration files that are environment-specific (e.g., development, production). These can include DB connection strings, API keys, etc.

    Deployment and Containerization: If you are using Docker or other deployment tools, the configuration can help set up containers and services.

    Centralized Configuration: Having this folder at the root level means that it's clear to the developer and the deployment system that these configurations are meant to be accessible across the entire project.

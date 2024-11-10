import os


class Config:
    """Base configuration with default settings."""

    # Secret key for session management and CSRF protection
    SECRET_KEY = os.getenv(
        "SECRET_KEY", "your-default-secret-key"
    )  # Replace with a real secret in production

    # Neo4j Database URI
    NEO4J_URI = os.getenv("NEO4J_URI", "neo4j:7687")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "test1234")

    # GitHub OAuth settings (if using GitHub for authentication)
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "your-github-client-id")
    GITHUB_CLIENT_SECRET = os.getenv(
        "GITHUB_CLIENT_SECRET", "your-github-client-secret"
    )

    GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    GITHUB_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
    GITHUB_API_BASE_URL = "https://api.github.com/"

    # Flask-Login settings
    SESSION_COOKIE_SECURE = True  # Enable for HTTPS in production
    REMEMBER_COOKIE_DURATION = 3600  # Duration for 'remember me' sessions (1 hour)


class DevelopmentConfig(Config):
    """Development-specific configuration."""

    DEBUG = True
    # NEO4J_URI = os.getenv("DEV_NEO4J_URI", "bolt://localhost:7687")
    SESSION_COOKIE_SECURE = False  # In development, HTTPS is typically not used


class TestingConfig(Config):
    """Testing-specific configuration."""

    TESTING = True
    DEBUG = True
    NEO4J_URI = os.getenv("TEST_NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USERNAME = os.getenv("TEST_NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("TEST_NEO4J_PASSWORD", "test-password")
    SESSION_COOKIE_SECURE = False  # Tests usually run in an HTTP context


class ProductionConfig(Config):
    """Production-specific configuration."""

    DEBUG = False
    TESTING = False
    NEO4J_URI = os.getenv("PROD_NEO4J_URI", "bolt://prod-neo4j-host:7687")
    SESSION_COOKIE_SECURE = True  # Enforce HTTPS for security in production
    REMEMBER_COOKIE_DURATION = (
        86400  # Longer 'remember me' duration in production (24 hours)
    )


# Dictionary to map configuration names
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

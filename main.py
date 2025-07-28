#!/usr/bin/env python3
"""
Main application launcher - FastAPI + Gradio with Professional Logging
Compatible with Azure deployment and local development
"""

import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI

# Add the project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

# Load environment variables
load_dotenv()


def setup_logging_environment():
    """Setup environment variables for logging"""

    # Set default log level based on environment
    if not os.getenv("GAME_LOG_LEVEL"):
        log_level = (
            "DEBUG" if os.getenv("DEV_MODE", "false").lower() == "true" else "INFO"
        )
        os.environ["GAME_LOG_LEVEL"] = log_level

    # Enable file logging in production, optional in dev
    if not os.getenv("GAME_ENABLE_FILE_LOGGING"):
        enable_file_logging = (
            "false" if os.getenv("DEV_MODE", "false").lower() == "true" else "true"
        )
        os.environ["GAME_ENABLE_FILE_LOGGING"] = enable_file_logging

    # Enable colors by default
    if not os.getenv("GAME_ENABLE_LOG_COLORS"):
        # Disable colors in production Azure environment
        enable_colors = (
            "true" if os.getenv("DEV_MODE", "false").lower() == "true" else "false"
        )
        os.environ["GAME_ENABLE_LOG_COLORS"] = enable_colors


def create_fastapi_app() -> FastAPI:
    """Create FastAPI application with logging"""

    setup_logging_environment()

    try:
        from frontend.core.logging_config import game_logger, log_startup_info

        log_startup_info()
        game_logger.info("Initializing FastAPI application")

        app = FastAPI(
            title="Detective Game",
            description="AI Detective Game",
            version="2.0.0",
        )

        import gradio as gr

        from frontend.ui.main_frontend import create_gradio_app

        game_logger.info("Creating Gradio application")
        gradio_app = create_gradio_app()

        game_logger.info("Mounting Gradio app to FastAPI")
        app = gr.mount_gradio_app(app, gradio_app, path="/")

        @app.get("/health")
        async def health_check():
            game_logger.debug("Health check requested")
            return {"status": "healthy", "logging": "enabled"}

        @app.get("/api/status")
        async def get_status():
            game_logger.debug("Status check requested")
            return {
                "message": "Detective Game API is running",
                "version": "2.0.0",
                "logging_enabled": True,
                "log_level": os.getenv("GAME_LOG_LEVEL", "INFO"),
            }

        @app.get("/api/logs/status")
        async def get_logging_status():
            """Get current logging configuration"""
            game_logger.debug("Logging status requested")
            return {
                "log_level": os.getenv("GAME_LOG_LEVEL", "INFO"),
                "file_logging": os.getenv("GAME_ENABLE_FILE_LOGGING", "false")
                == "true",
                "colors_enabled": os.getenv("GAME_ENABLE_LOG_COLORS", "true") == "true",
                "dev_mode": os.getenv("DEV_MODE", "false") == "true",
            }

        @app.get("/api/logs/level/{level}")
        async def set_log_level(level: str):
            """Change log level dynamically (dev mode only)"""
            if os.getenv("DEV_MODE", "false").lower() != "true":
                return {"error": "Log level changes only allowed in dev mode"}

            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if level.upper() not in valid_levels:
                return {"error": f"Invalid log level. Must be one of: {valid_levels}"}

            from frontend.core.logging_config import set_log_level

            set_log_level(level.upper())
            game_logger.info(f"Log level changed to {level.upper()}")

            return {"message": f"Log level set to {level.upper()}"}

        game_logger.info("FastAPI application created successfully")
        return app

    except Exception as e:
        print(f"Failed to create FastAPI app: {e}")
        raise


# Create the app instance
app = create_fastapi_app()


def run_development_mode():
    """Run in development mode with Gradio"""
    try:
        from frontend.core.logging_config import game_logger

        port = int(os.environ.get("PORT", 7860))

        launch_kwargs = {
            "server_name": "0.0.0.0",
            "server_port": port,
            "share": "--share" in sys.argv,
            "show_error": True,
            "quiet": False,
        }

        if "--debug" in sys.argv:
            from frontend.core.logging_config import enable_debug_mode

            enable_debug_mode()
            game_logger.info("Debug mode enabled via command line")

        game_logger.info("Starting in development mode", **launch_kwargs)

        from frontend.ui.main_frontend import create_gradio_app

        create_gradio_app().launch(**launch_kwargs)

    except KeyboardInterrupt:
        try:
            from frontend.core.logging_config import game_logger, log_shutdown_info

            game_logger.info("Development server stopped by user (Ctrl+C)")
            log_shutdown_info()
        except:
            print("Development server stopped")
    except Exception as e:
        try:
            from frontend.core.logging_config import game_logger

            game_logger.critical("Development server crashed", error=str(e))
        except:
            print(f"Development server error: {e}")
        raise


def run_production_mode():
    """Run in production mode with uvicorn"""
    try:
        import uvicorn

        from frontend.core.logging_config import game_logger

        port = int(os.environ.get("PORT", 8000))

        game_logger.info("Starting in production mode", port=port)

        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="warning",
            access_log=True,
        )

    except Exception as e:
        try:
            from frontend.core.logging_config import game_logger, log_shutdown_info

            game_logger.critical("Production server crashed", error=str(e))
            log_shutdown_info()
        except:
            print(f"Production server error: {e}")
        raise


def show_help():
    """Show command line help"""
    help_text = """
Detective Game - FastAPI + Gradio with Professional Logging

Usage:
    python main.py [options]

Options:
    --debug     Enable debug logging (dev mode only)
    --share     Create a public Gradio link (dev mode only)
    --help      Show this help message

Environment Variables:
    DEV_MODE                 Enable development mode (true/false)
    PORT                     Server port (default: 7860 dev, 8000 prod)
    GAME_LOG_LEVEL          Set log level (DEBUG, INFO, WARNING, ERROR)
    GAME_ENABLE_FILE_LOGGING Enable logging to file (true/false)
    GAME_ENABLE_LOG_COLORS   Enable colored console output (true/false)

Development Mode:
    DEV_MODE=true python main.py --debug --share

Production Mode:
    python main.py

API Endpoints:
    GET  /health              Health check
    GET  /api/status          Application status
    GET  /api/logs/status     Logging configuration (dev mode)
    GET  /api/logs/level/{level}  Change log level (dev mode)

Examples:
    # Development with debug logging
    DEV_MODE=true python main.py --debug
    
    # Production deployment
    PORT=8000 python main.py
    
    # Azure deployment (automatic)
    # Uses environment variables from Azure configuration
"""
    print(help_text)


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()
        sys.exit(0)

    try:
        dev_mode = os.environ.get("DEV_MODE", "false").lower() == "true"

        if dev_mode:
            run_development_mode()
        else:
            run_production_mode()

    except Exception as e:
        print(f"Application failed to start: {e}")
        sys.exit(1)
    finally:
        try:
            from frontend.core.logging_config import log_shutdown_info

            log_shutdown_info()
        except:
            print("Application shut down")
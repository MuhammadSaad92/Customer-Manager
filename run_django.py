import os
import sys
import time
import logging
from waitress import serve
from django.core.wsgi import get_wsgi_application

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        start_time = time.time()
        logger.info("Starting application")
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "customerdata.settings")
        logger.info("Loading WSGI application")
        application = get_wsgi_application()
        logger.info(f"WSGI loaded in {time.time() - start_time:.2f} seconds")
        logger.info("Starting Waitress server on http://0.0.0.0:8000")
        serve(application, host='0.0.0.0', port=8000, _quiet=False)
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
        input("Press Enter to exit...")
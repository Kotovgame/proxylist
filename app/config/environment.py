from dotenv import load_dotenv
from os import getenv

load_dotenv()

LOGGER_FORMAT = getenv("LOGGER_FORMAT", None)
URL_FOR_VERIFICATION_PROXY = getenv("URL_FOR_VERIFICATION_PROXY", None)

import logging
import logging.handlers
import time
from ConfigParser import SafeConfigParser

CONFIGURATION_FILE = "settings.conf"
parser = SafeConfigParser()
parser.read(CONFIGURATION_FILE)
BASEPATH = parser.get('settings','log_path')
log_level = parser.get('settings','log_level')
LOG_FILE = BASEPATH  + "Test_orchestrator"

logger = logging.getLogger('Tets Orchetstrator')
hdlr_uploader = logging.FileHandler(LOG_FILE + "_" + time.strftime("%Y%m%d")+'.log')
hdlr_service = logging.FileHandler(LOG_FILE + "_" + time.strftime("%Y%m%d")+'.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s',"%Y-%m-%d %H:%M:%S")
hdlr_uploader.setFormatter(formatter)
hdlr_service.setFormatter(formatter)
logger.addHandler(hdlr_uploader)
logger.setLevel(log_level)
logger.debug('Logger Initialized')

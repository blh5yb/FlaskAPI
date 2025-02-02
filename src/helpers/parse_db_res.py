import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S %Z')
logger = logging.getLogger(__name__)


def parse_db_res(data):
    print('parse', data)
    data['_id'] = str(data['_id'])
    if data.get('created_at', ''):
      data['created_at'] = format_db_date(data['created_at'])
    if data.get('updated_at', ''):
      data['updated_at'] = format_db_date(data['updated_at'])

    return json.loads(json.dumps(data)) # json.loads(json_util.dumps(data))


def format_db_date(my_date):
  return my_date if isinstance(my_date, str) else my_date.isoformat()
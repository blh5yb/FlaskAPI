import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S %Z')
logger = logging.getLogger(__name__)


def parse_db_res(data):
    if isinstance(data, list):
        for item in data:
            print('item', item)
            item['_id']= str(item['_id'])
            item['date'] = parse_db_date(item['date'])
            print('item', item)
    else:
        data['_id'] = str(data['_id'])
        data['date'] = parse_db_date(data['date'])
    print('data', json.loads(json.dumps(data)))
    return json.loads(json.dumps(data)) # json.loads(json_util.dumps(data))

def parse_db_date(my_date):
    return my_date if isinstance(my_date, str) else my_date.isoformat()
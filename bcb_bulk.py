import os
from datetime import datetime
import pandas as pd
import django
from django.conf import settings
import sgs
import requests
import pandas as pd
import concurrent.futures

# Define constants
NUMBER_OF_OBJECTS = 10000
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False
django.setup()

def process_response(CDI_CODE,):
    df = pd.DataFrame(columns=['codigo','nome','unidade','frequencia','primeiro_valor','ultimo_valor', 'origem'])
    ts = sgs.metadata(CDI_CODE,'pt')
    data = []
    if ts[0] is not None:
        data.append({'codigo': ts[0][0]['code'], 'nome': ts[0][0]['name'], 'unidade': ts[0][0]['unit'], 'frequencia': ts[0][0]['frequency'], 'primeiro_valor': ts[0][0]['first_value'], 'ultimo_valor': ts[0][0]['last_value'], 'origem': ts[0][0]['source']})
        # print(CDI_CODE, ' - ', 'Processed')
        return data
    else:
        # print(CDI_CODE, ' - ', 'Processed (None)')
        return None
    
def multi_process():
    count = 0
    combined_data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(1,30000):
            future = executor.submit(process_response, i)
            futures.append(future)
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            if data is not None:
                combined_data.append(data)
                count += 1
                print(count)
    return combined_data
                

if __name__ == '__main__':
    all_data  = multi_process()
    data = []
    for i in all_data:
        data.append(i[0])    
    df = pd.DataFrame(data)

    from revcontract.models import BCBSGS
    df = pd.read_csv('sgs.csv')
    df['primeiro_valor'] = df['primeiro_valor']
    df['ultimo_valor'] = df['ultimo_valor']
    bcb_instances = []
    for index, row in df.iterrows():
        try:
            if len(row['primeiro_valor']) == 10:
                # Use format for "1986-06-04"
                date_obj = datetime.strptime(row['primeiro_valor'], "%Y-%m-%d")
                start_date_temp = date_obj.strftime("%Y-%m-%d")
            else:
                # Use format for "2023-07-25 00:00:00"
                date_obj = datetime.strptime(row['primeiro_valor'], "%Y-%m-%d %H:%M:%S")
                start_date_temp = date_obj.strftime("%Y-%m-%d")
            
            if len(row['ultimo_valor']) == 10:
                # Use format for "1986-06-04"
                date_obj = datetime.strptime(row['ultimo_valor'], "%Y-%m-%d")
                end_date_temp = date_obj.strftime("%Y-%m-%d")
            else:
                # Use format for "2023-07-25 00:00:00"
                date_obj = datetime.strptime(row['ultimo_valor'], "%Y-%m-%d %H:%M:%S")
                end_date_temp = date_obj.strftime("%Y-%m-%d")

            bcb_instances.append(BCBSGS(
                code=row['codigo'],
                name=row['nome'],
                unit = row['unidade'],
                frequency=row['frequencia'],
                start_date = start_date_temp,
                end_date = end_date_temp,
                source = row['origem'],
            ))
        except Exception as e:
            print(e)
            print(row)
            continue
    BCBSGS.objects.bulk_create(bcb_instances)


# Path: bcb_bulk.py
from parser import items_info,item_parse
from dict_elements import headers
import time
import numpy as np
import json
import datetime

def main():
    i = 0
    info=[]
    products_len=1
    while products_len > 0:
        print(f'{i}')
        time.sleep(np.random.choice([x / 10 for x in range(7, 22)]))
        buffer=items_info(f"https://www.npeal.com/collections/all?page={i}",headers=headers)
        products_len=len(buffer['products'])
        if products_len==0:
            break
        else:
            info.append(items_info(f"https://www.npeal.com/collections/all?page={i}",headers=headers))
            i += 1


    names=[info[i]['products'][j]['variants'][0]['name'] for i in range(0,len(info)) for j in range(0,len(info[i]['products']))]
    names=list(set([i[0:i.index(' - ')].replace(' ','-').replace("'",'') for i in names if ' - ' in i]))

    jsonData=json.dumps(info)
    filename='result_general/npeal.com'+str(datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p"))

    with open(filename, 'w') as f:
        json.dump(info, f)


    full_item_info=[]
    for i in names:
        print(f'{names.index(i)} out of {len(names)}')
        time.sleep(np.random.choice([x / 10 for x in range(7, 22)]))
        full_item_info.append(item_parse(f'https://www.npeal.com/products/{i}',headers=headers))

    filename='result_full/full_item_npeal.com'+str(datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p"))
    with open(filename, 'w') as f:
        json.dump(full_item_info, f,indent=2)

if __name__ == "__main__":
    main()



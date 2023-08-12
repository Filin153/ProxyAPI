import pandas as pd
import requests
import threading
from load_poxies import load_one


def thread_job(info_list, сheck_url, file_name):

    df_work = pd.DataFrame(columns=[['proxy', 'https']])

    proxy = info_list[1]
    https = info_list[2]

    try:
        response = requests.get(
            сheck_url,
            proxies={'https://': f'http://{proxy}'},
            timeout=2)

        if response.status_code == 200:
            print("Удача - ", proxy, " | Ответ - ", response)
            df_work.loc[len(df_work.index)] = [proxy, https]
            df_work.to_csv(f'work_file/{file_name}.csv', index_label='N', mode='a', header=False)
        else:
            print("Ошибка - ", proxy, " | Ответ - ", response)
    except:
        print("Ошибка - ", proxy, " | Ответ - Не получен")


def run_threads(сheck_url: str, file_name: str):
    threads = []

    df = pd.read_csv('load_file/ip-port.csv')
    plist = df.values.tolist()
    load_one()

    for proxy in plist:
        threads.append(threading.Thread(target=thread_job, args=(proxy, сheck_url, file_name)))

    for thread in threads:
        thread.start()  # каждый поток должен быть запущен
    for thread in threads:
        thread.join()  # дожидаемся исполнения всех потоков
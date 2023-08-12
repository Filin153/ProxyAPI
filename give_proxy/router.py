import os
import re
from typing import Optional
import pandas as pd
from fastapi import APIRouter
from check import run_threads
import datetime

router = APIRouter(
    tags=['Proxy'],
    prefix='/proxy'
)


@router.get('/generate_and_give')
async def give_proxy(сheck_url: str, file_name: str, https: Optional[str] = None):

    if сheck_url.split(':')[0] not in ['https', 'http']:
        return {"answer": "Убедитесь что ссылка корректна",
                "comment": "Скорее всего check_url является текстом и никуда не ведёт",
                "status_code": "400"}

    if file_name[-3:] == "csv":
        file_name = file_name[:-4]
    if not re.match(r'^[\w\.]+$', file_name):
        return {"answer": "Название файла некорректно",
                "comment": "Скорее всего в названии файла есть недопустимые символы",
                "status_code": "400"}

    file_dirs = os.listdir("work_file")
    if file_name + ".csv" in file_dirs:
        return {"answer": "Файл уже существует",
                "comment": "Поменяйте имя файла",
                "status_code": ""}
    else:
        run_threads(сheck_url, file_name)

    df = pd.read_csv(f'work_file/{file_name}.csv')
    pro_list = df.values.tolist()
    df = pd.DataFrame(columns=[['proxy', 'https']])
    for i in pro_list:
        df.loc[len(df)] = [i[1], i[2]]

    date = str(datetime.datetime.now()).replace("-", "_").replace(" ", "_").replace(":", "T").split('.')[0]
    os.remove(f'work_file/{file_name}.csv')
    df.to_csv(f'work_file/{file_name}_{date}.csv')

    proxies = pd.DataFrame()
    df = pd.read_csv(f'work_file/{file_name}_{date}.csv')
    if https == 'yes':
        proxies['proxy'] = df[df['https'] == "yes"]['proxy']
        return {"status_code": "200", "https": "yes", "data": proxies['proxy'].tolist()}
    elif https == 'no':
        proxies['proxy'] = df[df['https'] == "no"]['proxy']
        return {"status_code": "200", "https": "no", "data": proxies['proxy'].tolist()}
    else:
        return {"status_code": "200", "https": "all_proxy", "data": df['proxy'].tolist()}

@router.get('/give_from_file')
async def give_from_file(file_name: str, https: Optional[str] = None):


    if file_name[-3:] == "csv":
        file_name = file_name[:-4]
    if not re.match(r'^[\w\.]+$', file_name):
        return {"answer": "Название файла некорректно",
                "comment": "Скорее всего в названии файла есть недопустимые символы",
                "status_code": "400"}

    file_dirs = os.listdir("work_file")
    if file_name + ".csv" not in file_dirs:
        return {"answer": "Нет файла с таким названием",
                "comment": "Посмотреть все файлы можно через /all_file",
                "status_code": "400"}

    proxies = pd.DataFrame()
    df = pd.read_csv(f'work_file/{file_name}.csv')
    if https == 'yes':
        proxies['proxy'] = df[df['https'] == "yes"]['proxy']
        return {"status_code": "200", "https": "yes", "data": proxies['proxy'].tolist()}
    elif https == 'no':
        proxies['proxy'] = df[df['https'] == "no"]['proxy']
        return {"status_code": "200", "https": "no", "data": proxies['proxy'].tolist()}
    else:
        return {"status_code": "200", "https": "all_proxy", "data": df['proxy'].tolist()}


@router.get('/all_file')
async def all_file():
    return os.listdir("work_file")



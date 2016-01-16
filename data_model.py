import json


def read_data_model(file_name: str) -> dict:
    file = open(file_name, mode='r', encoding='utf-8')
    return json.load(file)


def write_data_model(file_name: str, data_model: dict):
    file = open(file_name, mode='w', encoding='utf-8')
    json.dump(data_model, file, separators=(',', ':'), ensure_ascii=False)
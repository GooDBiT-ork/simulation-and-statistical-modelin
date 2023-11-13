import os
import shutil
import json
import base64
import argparse


def serialize_permissions(input_file, output_file):
    # Получение настроек доступа к файлу
    permissions = os.stat(input_file)

    # Сериализация настроек в JSON-формат
    serialized_permissions = json.dumps(permissions)

    # Кодирование сериализованных настроек в base64
    encoded_permissions = base64.b64encode(serialized_permissions.encode())

    # Запись сериализованных и закодированных настроек в файл
    with open(output_file, 'wb') as f:
        f.write(encoded_permissions)


def deserialize_permissions(input_file, output_file):
    # Чтение сериализованных и закодированных настроек из файла
    with open(input_file, 'rb') as f:
        encoded_permissions = f.read()

    # Декодирование настроек из base64
    decoded_permissions = base64.b64decode(encoded_permissions)

    # Десериализация настроек из JSON-формата
    permissions = json.loads(decoded_permissions.decode())

    # Восстановление настроек доступа к файлу
    shutil.copystat(input_file, output_file)
    os.chown(output_file, permissions['st_uid'], permissions['st_gid'])
    os.chmod(output_file, permissions['st_mode'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--serialize', action='store_true', help='Сохранение настроек доступа')
    parser.add_argument('--deserialize', action='store_true', help='Восстановление настроек доступа')
    parser.add_argument('--input', help='Входной файл')
    parser.add_argument('--output', help='Выходной файл')
    args = parser.parse_args()

    if args.serialize:
        serialize_permissions(args.input, args.output)
    elif args.deserialize:
        deserialize_permissions(args.input, args.output)

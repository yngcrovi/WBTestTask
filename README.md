# Запуск проекта

## Сбилдить образ проекта
```console
sudo docker compose build
```

## Создать копию файла .env из .env.example
```console
cp .env.example .env
```
Заполнить его данными, которые пришлю

## Запустить контейнеры, указав относительный путь к .env
```console
sudo docker compose --env-file ./src/.env up -d
```
Подождать, когда в корневой папке ./excel появятся 2 файла или убедиться, что контейнер pyhton закончил работу

## Очистить базу и выключиь контейнеры
```console
sudo docker compose down -v
```

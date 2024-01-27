# Architecture_Lab

Для запуска проекта требуется установить зависимости микросервисов посредством команд:
  python -m pip install -r recommendations/requirements.txt
  python -m pip install -r marketplace/requirements.txt

Поднять контейнеры Docker коммандой docker-compose up.

После завершения работы убрать за собой с помощью команд:
  docker ps -a
  docker rm <id>
  docker images
  docker image rm -f marketplace
  docker image rm -f recommendations

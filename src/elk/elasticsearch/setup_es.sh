#!/bin/bash

echo "Проверка готовности Elasticsearch на http://es01:9200..."

# Ждём, пока Elasticsearch не будет готов
until curl -s http://es01:9200 | grep -q "cluster_name"; do
  echo "Ожидаем запуск Elasticsearch..."
  sleep 5
done

echo "Elasticsearch готов!"

# Установка пароля kibana_system
echo "Попытка авторизации с текущим паролем kibana_system..."

if curl -s -XGET http://es01:9200 -u "kibana_system:kibana_store" | grep -q "cluster_name"; then
  echo "Пароль kibana_system корректен. Продолжаем."
else
  echo "Установка нового пароля для kibana_system..."
  until curl -s -XPOST -u "elastic:elastic_store" -H "Content-Type: application/json" \
    http://es01:9200/_security/user/kibana_system/_password \
    -d '{"password": "kibana_store"}' | grep -q "^{}"; do
      echo "Ожидание установки пароля kibana_system..."
      sleep 5
  done
fi

echo "Настройка Elasticsearch завершена!"

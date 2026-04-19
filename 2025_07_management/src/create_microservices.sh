#!/bin/bash
# chmod +x create_microservices.sh

# Danh sách các service bạn muốn tạo
services=("finance_jira_service" "ecommerce_ticket_service")

# Tạo thư mục gốc
mkdir -p auto_process_manager/services
mkdir -p auto_process_manager/shared_libs/ai_agent

# Tạo shared_libs
echo "Creating shared_libs..."
touch auto_process_manager/shared_libs/logger.py
touch auto_process_manager/shared_libs/utils.py
touch auto_process_manager/shared_libs/ai_agent/command_parser.py

# Tạo từng service
for service in "${services[@]}"; do
  echo "Creating service: $service"
  base="auto_process_manager/services/$service"

  mkdir -p "$base/raw"
  mkdir -p "$base/pre_processing"
  mkdir -p "$base/db"
  mkdir -p "$base/modules"
  mkdir -p "$base/menu"

  touch "$base/main.py"
  touch "$base/config.py"
  touch "$base/raw/.keep"
  touch "$base/pre_processing/__init__.py"
  touch "$base/db/.keep"
  touch "$base/modules/__init__.py"
  touch "$base/menu/loader.py"
done

echo "✅ Microservice structure created successfully!"

#!/bin/bash

# PORT環境変数が設定されていない場合は8000を使用
PORT=${PORT:-8000}

echo "Starting server on port $PORT"

# uvicornでアプリケーションを起動
python -m uvicorn main:app --host 0.0.0.0 --port $PORT
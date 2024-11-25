curl http://localhost:8090/openai/v1/chat/completions \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'X-API-Key: f10335f4109a466b49d05856fa70d6277bcd41cdbcba422a47c24f8475a27e04' \
-v -X POST -d '{
  "model": "llama3:8b",
  "messages": [
    {
      "role": "user",
      "content": "What kind of instance types to use in GCP for running an AI training model?"
    }
  ]
}'
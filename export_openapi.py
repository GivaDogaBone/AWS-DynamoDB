# export_openapi.py
import json
from main import app

# Get the OpenAPI JSON
openapi_schema = app.openapi()

# Save it to a file
with open("openapi.json", "w") as f:
    json.dump(openapi_schema, f, indent=2)

print("OpenAPI schema exported to openapi.json")

# Run this script locally to generate the OpenAPI schema file. You can then use this schema to:
# 1. Import into API Gateway as a REST API
# 2. Use with external Swagger UI tools
# 3. Generate client SDKs

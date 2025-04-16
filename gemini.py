from google import genai
from google.genai import types

client = genai.Client(api_key='your-api-key-here')

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='Current Weather of Shimla.'
)
print(response.text)
import httpx
response = httpx.get("https://www.google.com")
print(response.status_code)


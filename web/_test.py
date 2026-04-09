"""Quick test - captura corpo do erro 500."""
import urllib.request, json

boundary = 'boundary123'
filename = 'test_real.mp4'
with open(filename, 'rb') as f:
    file_data = f.read()

body = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
    f'Content-Type: video/mp4\r\n\r\n'
).encode() + file_data + f'\r\n--{boundary}--\r\n'.encode()

req = urllib.request.Request(
    'http://127.0.0.1:5000/api/convert',
    data=body,
    headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
)
try:
    resp = urllib.request.urlopen(req)
    print('OK:', resp.read().decode())
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}:')
    body = e.read().decode('utf-8', errors='replace')
    # Extract just the error parts
    for line in body.split('\n'):
        line = line.strip()
        if 'Traceback' in line or 'Error' in line or 'File' in line or 'line' in line or '    ' in line:
            print(line[:200])
    print('---FULL BODY SNIPPET---')
    print(body[:3000])

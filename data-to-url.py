import requests
import curlify
import json

# these work:
#
# curl -X POST -H "Content-Type:application/x-www-form-urlencoded" --data '{"bytes":{"type":"Buffer","data":[102,111,111]}}' "https://staging.gather.town/api/uploadImage"
#
# response = requests.post('https://staging.gather.town/api/uploadImage', headers={'Content-Type': 'application/json'}, data=b'{"bytes":{"type":"Buffer","data":[102,111,111]}}')

def data_to_upload_image_args(data):
  if isinstance(data, str):
    try:
      data = data.encode('utf8')
    except:
      data = data.encode('latin1')
  if isinstance(data, bytes):
    data = list(iter(data))
  data = {'bytes': {'type': 'Buffer', 'data': data}}
  data = json.dumps(data)
  data = data.encode('utf8')
  return data

def report_error(caught, code=200, **kwds):
  message = str(caught)
  # sys.stderr.write('Failed for {} of data size {}: {}\n'.format(kwds, len(data), message))
  print(json_response(False, message, code=code, **kwds))

def on_err(thunk, *args, handler=report_error, exception=Exception, **kwds):
  try:
    return thunk(*args)
  except exception as e:
    return handler(e, **kwds)

def data_to_url(data, raise_on_error=True):
  data = data_to_upload_image_args(data)
  response = requests.post('https://staging.gather.town/api/uploadImage', 
      headers={'Content-Type': 'application/json'},
      data=data)
  if response.ok:
    return response.text
  if raise_on_error:
    response.raise_for_status()

def json_response(ok, result, **kwds):
  kwds.update({'ok': ok, 'result': result})
  if 'data' in kwds:
    kwds['size'] = len(kwds.pop('data'))
  return json.dumps(kwds)

def data_to_url_thread(path):
  def thunk():
    data = filebytes(path)
    url = data_to_url(data)
    print(json_response(True, url, data=data, path=path))
  thread = threading.Thread(target=lambda: on_err(thunk, path=path), daemon=True)
  thread.start()
  return thread

import httpx

async def data_to_url_async(data, path='unknown'):
  data = data_to_upload_image_args(data)
  async with httpx.AsyncClient() as client:
    try:
      response = await client.post('https://staging.gather.town/api/uploadImage',
          headers={'Content-Type': 'application/json'},
          data=data,
          timeout=httpx.Timeout(timeout=None))
      if response.status_code == 200:
        url = response.text
        print(json_response(True, url, data=data, path=path))
      else:
        response.raise_for_status()
    except Exception as caught:
      report_error(caught, data=data, path=path, code=response.status_code)

def filebytes(path):
  with open(path, 'rb') as f:
    return f.read()

if __name__ == '__main__':
  import sys
  import threading
  args = sys.argv[1:]
  if len(args) <= 0:
    def thunk():
      data = sys.stdin.buffer.read()
      url = data_to_url(data)
      print(json_response(True, url, data=data, path='/dev/stdin'))
    on_err(thunk, path='/dev/stdin')
    # try:
    #   print(json_response(True, data_to_url(data), data=data, path='/dev/stdin'))
    # except Exception as caught:
    #   report_error(caught, data=data, path=path, code=response.status_code)
  else:
    import asyncio
    loop = asyncio.get_event_loop()
    async_tasks = [loop.create_task(data_to_url_async(filebytes(arg), path=arg)) for arg in args]
    loop.run_until_complete(asyncio.gather(*async_tasks))
    # threads = [data_to_url_thread(arg) for arg in args]
    # for thread in threads:
    #   thread.join()

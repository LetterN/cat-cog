import socket
import urllib
import struct

def Topic(addr:str, port:int, querystr:str or dict):
  """
	Fetch- oh i mean topic
    `getserverdata.php` (see tg repo)
	"""
  print("INFO: FETCH REQ: "+addr+":"+str(port))
  try:
    if querystr[0] != "?":
      querystr = "?"+querystr
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    query = b"\x00\x83" + struct.pack('>H', len(querystr) + 6) + b"\x00\x00\x00\x00\x00" + querystr.encode() + b"\x00"

    sock.connect((addr, port))
    sock.sendall(query)
    data = sock.recv(4096)
    parsed_data = urllib.parse.parse_qs(data[5:-1].decode())
    return {i:parsed_data[i][0] for i in parsed_data.keys()}
  except Exception as E:
    print("ERROR: fetch: ",E)
    return {}

def getSeconds(h:int=0,m:int=0,s:int=0):
    return (int(h) * 3600) + (int(m) * 60) + int(s)

def safeget(dct:dict, *keys):
  """
  get keys without ``KeyError``
  """
  for key in keys:
    try:
      dct = dct[key]
    except KeyError:
      return None
  return dct

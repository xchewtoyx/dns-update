#!/usr/bin/env python
'Detect when local IP has changed and update DNS via web API'
from rgh.dnsupdater import main

if __name__ == '__main__':
  main.run()

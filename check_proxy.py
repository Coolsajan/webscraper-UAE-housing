import threading
import queue
import requests
import os

q=queue.Queue()
valid_proxy=[]


with open("all_proxy.txt","r") as f:
    proxies=f.read().split("\n")
    for p in proxies:
        q.put(p)

def check_proxy():
    global q
    while not q.empty():
        proxy=q.get()
        try :
            res= requests.get("http://ipinfo.io/json",
                              proxies={"http":proxy,
                              "https":proxy})
        except:
            continue
        if res.status_code==200:
            print(proxy)

for _ in range(10):
    threading.Thread(target=check_proxy).start()


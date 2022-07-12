import socket
import re
from config import LOCALHOST, random_port

BACKLOG = 10

my_socket = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_STREAM,
)


def search_status(data):
    status = re.search(r"\d\d\d", data)
    if status == None:
        status = 200
    else:
        status = status.group()
    return status


def only_headers(data):
    first_string = []
    for i in data[:3]:
        first_string.append(i)
    joined_fst_string = ''.join(first_string)
    return len(joined_fst_string) + 4


adress_and_port = (LOCALHOST, random_port())
my_socket.bind(adress_and_port)
print(adress_and_port)
my_socket.listen(BACKLOG)
conn, addr = my_socket.accept()

data = conn.recv(1024)
data = data.decode("utf-8")
splitted_data = data.split()
status = search_status(splitted_data[1])
method = splitted_data[0]
num = only_headers(splitted_data)
conn.send(
    f"HTTP/1.1 {status}\n Content-Length: 100\n Connection: close\n Content-Type: text/html\n\nRequest headers:\n{data[num:]}Request method: {method}\nRequest status: {status}".encode(
        "utf-8"))

my_socket.close()

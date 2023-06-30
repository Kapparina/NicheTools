import socket
import pandas as pd

df = pd.read_excel("./hosts.xlsx")
host_dict = {}
for n in df["Name"]:
    try:
        print(s := socket.gethostbyname(n), n, sep="\t")
        host_dict[n] = s
    except:
        continue

host_df = pd.DataFrame({"Name": host_dict.keys(), "IP Address": host_dict.values()})
host_df.to_excel("./results.xlsx")

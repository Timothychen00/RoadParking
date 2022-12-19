import os

def update_ip(devices):
    stream = os.popen('arp -a')
    output = stream.read()
    data=output.splitlines()
    # print(output)
    for i in devices:
        for k in data:
            # print(i.upper())
            if (i.lower() in k) or (i.upper() in k):
                devices[i][0]=k.split()[1][1:-1]
                print(k.split()[1][1:-1])
    return devices
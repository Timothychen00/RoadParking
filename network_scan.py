import os
devices={'8:B6:1F:39:B2:FC':["0.0.0.0","lost"],'44:17:93:7E:3B:7C':["0.0.0.0","lost"],'8:B6:1F:39:AF:20':['0.0.0.0','lost']}


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
print(update_ip(devices))
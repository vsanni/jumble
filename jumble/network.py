from netifaces import interfaces, ifaddresses, AF_INET

def local_host_ip():

    LHIP = {}
    for ifName in interfaces():
        for k,v in ifaddresses(ifName).items():
            if k == AF_INET:
                LHIP[str(ifName)] = str(v[0]['addr'])

    return LHIP

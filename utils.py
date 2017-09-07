import netifaces


def inet_address(interface_name):
    ifaddresses = netifaces.ifaddresses(interface_name)
    inet_addresses = ifaddresses[netifaces.AF_INET]
    return inet_addresses[0]['addr']

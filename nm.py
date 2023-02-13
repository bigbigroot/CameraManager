from ipaddress import ip_address
import os
from sys import prefix

def get_hostname():
    res = os.popen('nmcli general hostname')
    output = res.readline().rstrip()
    if res.close() is None:
        return output
    else:
        return None


def set_hostname(hostname):
    res = os.popen('nmcli general hostname {0}'.format(hn))
    if res.close() is None:
        return True
    else:
        return False


def list_wifi_aps():
    res = os.popen('nmcli device wifi list')
    outputs = res.readlines()
    if res.close() is None:
        ssidIndexs = 0
        ssidIndexe = 0
        securityIndex = 0
        ssidIndexs = outputs[0].find('SSID')
        ssidIndexe = outputs[0].find('MODE')
        securityIndex = outputs[0].find('SSID')
        def get_ssid_security(s):
            ssid = s[ssidIndexs:ssidIndexe].rstrip()
            sec = s[securityIndex:].rstrip()
            return ssid, sec

        return list(map(get_ssid_security(value), outputs[0:]))
    else:
        print('not fonud interface: wlan0.')

        
def connect_aps(ssid, password):
    cmd: str
    if password is None:
        cmd = 'nmcli device wifi connect {0}'.format(ssid)
    else:
        cmd = 'nmcli device wifi connect {0} password {1}'.format(ssid, password)
    res = os.popen(cmd)
    if res.close() is None:
        return True
    else:
        return False


def get_ip_config_by_if(ifname):
    res = os.popen('nmcli device show {0}'.format(ifname))
    outputs = res.readlines()
    if res.close() is None:
        ip = None
        prefix: str
        gateway = None
        for o in outputs:
            if 'IP4.GATEWAY:' in o:
                gateway = o.removeprefix('IP4.GATEWAY:').strip()
            if 'IP4.ADDRESS[1]:' in o:
                ip, prefix = o.removeprefix('IP4.ADDRESS[1]:').strip().split('/')
        return ip, int(prefix), gateway
    else:
        return None


def get_dns_config_by_if(ifname):
    res = os.popen('nmcli device show {0}'.format(ifname))
    outputs = res.readlines()
    if res.close() is None:
        i = 1
        dnsList = []
        for o in outputs:
            if 'IP4.DNS[[{0}]:'.format(i) in o:
                dns = o.removeprefix('IP4.IP4.DNS[[{0}]:'.format(i)).strip()
                dnsList.append(dns)
                i += 1
        return dnsList
    else:
        return None


def set_ip_config_by_if(ifname, ip, prefix, gateway):
    res = os.popen('nmcli device modify {0} ipv4.address {1}/{2}'.format(ifname, ip, prefix))
    if res.close() is None:
        res = os.popen('nmcli device modify {0} ipv4.gateway {1}'.format(ifname, gateway))
        return res.close() is None
    else:
        return False


def dhcp_client(ifname, isAuto: bool) -> bool:
    mode: str
    if isAuto:
        mode = 'auto'
    else:
        mode = 'manual'
    res = os.popen('nmcli device modify {0} ipv4.method {1}'.format(ifname, mode))
    return res.close() is None
    

def set_dns_config_by_if(ifname, dns):
    res = os.popen('nmcli device modify {0} ipv4.dns {1}'.format(ifname, dns))
    return res.close() is None

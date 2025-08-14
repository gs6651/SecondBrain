

# Return True if ipv4 address, False if not

def is_ipv4_address(ip):
    
    octets = ip.split('.')

    if len(octets) != 4:
        return False
    elif any(not octet.isdigit() for octet in octets):
        return False
    elif any(int(octet) < 0 for octet in octets):
        return False
    elif any(int(octet) > 255 for octet in octets):
        return False

    return True

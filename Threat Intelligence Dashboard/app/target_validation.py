import ipaddress

def validate_target_type(target, target_type):

    if target_type == "ip":
        try:
            ipaddress.ip_address(target)
            return True
        except ValueError:
            return False

    elif target_type == "domain":

        try:
            ipaddress.ip_address(target)
            return False
        except ValueError:
            pass
        
        if "." not in target:
            return False
        
        if " " in target:
            return False
        
        return True

    return False
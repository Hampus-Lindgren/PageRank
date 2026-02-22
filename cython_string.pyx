def digits(str val):
    return int(''.join([n for n in val if n.isdigit()]))


def format_key(str key):
    key = key.strip() 
    if key[0] == '"' and key[1] == '"':
        key = key[1:-1]
    return key 
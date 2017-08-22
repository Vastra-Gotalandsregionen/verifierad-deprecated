import requests

def check_http_headers(url, timeout=60, verify=True):
    """ Returns HTTP headers for givn URL. Returns a CaseInsensitiveDict

        Atributes: url, timeout (optional) in seconds, verify (optional) as bool
    """
    response = requests.get(url, timeout=timeout, verify=verify)

    return response.headers

def is_redirecting(url, timeout=60):
    """Check if a URL is redirecting

    Attributes: URL, timeout in seconds (optional)
    """
    response = requests.get(url, timeout=timeout, verify=True)

    if '301' in str(response.history) or '302' in str(response.history): return True

    return False

def use_https(url, timeout=60):
    """Check if a URL is using or referring to SSL/TLS. Won't check the URL contents, just the served URL (which might not be the requested one)

    Attributes: URL, timeout in seconds (optional)
    """
    
    try:
        response = requests.get(url, timeout=timeout, verify=True)
        if 'https://' in response.url: return True

        return False
    except:
        # Defaulting to 'False', probably the web server don't know what to do
        print('Warning: The HTTPS request to {url} failed, assuming a \'False\''.format(url=url))
        return False

"""
If file is executed on itself then call a definition, mostly for testing purposes
"""
if __name__ == '__main__':
    #print(use_https('https://gp.se'))
    #print(use_https('http://vgregion.se'))
    #print(use_https('http://webbstrategiforalla.se'))
    
    #print(is_redirecting('http://vgregion.se'))
    
    #print(check_http_headers('http://amazon.com/')['Content-Type'])   # if you'd like to get a single value
    for key, value in check_http_headers('http://amazon.com/').items():
        print('Key: \'{k}\', value: \'{val}\''.format(k=key, val=value))


# /usr/bin/python3.4
import sys
import requests

def rest_api_call(host):
    """

    :param host: string - host end point
    :return:
    """
    api_url = "http://"+ host +":3000/"
    response = requests.get(api_url)
    return response.status_code

if __name__ == "__main__":
    host =sys.argv[1]
    print(rest_api_call(host))





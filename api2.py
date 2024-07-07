import time
import requests
from datetime import datetime

class EndpointChecker:
    def __init__(self, url):
        self.url = url
    
    def check_status(self):
        try:
            response = requests.get(self.url)
            return {
                'QueriedAt': datetime.now().isoformat(),
                'ResponseCode': response.status_code,
                'IsAlive': response.status_code == 200
            }
        except requests.RequestException as e:
            return {
                'QueriedAt': datetime.now().isoformat(),
                'ResponseCode': None,
                'IsAlive': False,
                'Error': str(e)
            }

if __name__ == "__main__":
    st = time.time()
    checker = EndpointChecker('https://www.google.com')
    status = checker.check_status()
    et = time.time()
    print(status)
    print(f"total script runtime {(et-st)/60} minutes")

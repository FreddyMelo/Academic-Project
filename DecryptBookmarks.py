import subprocess
import sys

a = 0x23fa259a219d2843
b = 0x9654e78f1facc0ab

for i in range(256):
    for j in range(256):
        newkey = [0, 0]
        newkey[0] = (a * i + b) & 0xFFFFFFFFFFFFFFFF
        newkey[1] = (a * j + b) & 0xFFFFFFFFFFFFFFFF
        trykey = f"{newkey[0]:016x}{newkey[1]:016x}"

        input_file = "cloud_all.ehtml"
        output_file = "try.html"

        subprocess.run(['openssl', 'aes-128-ctr', '-d', '-in', input_file, '-K', trykey, '-iv', trykey, '-out', output_file])

        grep_process = subprocess.run(['grep', '-q', '<html', output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(f"Trying values: i={i}, j={j}, key={trykey}")
        if grep_process.returncode == 0:
            print(f"Key: {trykey}, Decrypted Bookmarks Found in try.html")
            sys.exit(0)

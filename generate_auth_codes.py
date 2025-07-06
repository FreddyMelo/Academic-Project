# Create array for all generated values to be stored after calculation
# Sorts them and displays for attacker to see them.
valid_acodes = []

for value in range(256):
    auth_code = (value * 41943 + 54189) % 1048575
    if 100000 <= auth_code <= 999999:
        valid_acodes.append(auth_code)

valid_acodes = sorted(set(valid_acodes))

print("Valid authentication codes:")
for auth_code in valid_acodes:
    print(auth_code)

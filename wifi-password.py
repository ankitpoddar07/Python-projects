import subprocess

def get_wifi_password(profile_name):
    try:
        # Get password for a specific profile
        result = subprocess.check_output(f"netsh wlan show profile name=\"{profile_name}\" key=clear", shell=True).decode()
        for line in result.split("\n"):
            if "Key Content" in line:
                return line.split(":")[1].strip()
        return "🔒 No password found (Open network or not stored)"
    except subprocess.CalledProcessError:
        return "❌ Could not read password or network not found"

def main():
    profile_name = input("Enter the Wi-Fi network name (SSID) to retrieve its password: ").strip()
    password = get_wifi_password(profile_name)
    print(f"Password for {profile_name}: {password}")

if __name__ == "__main__":
    main()

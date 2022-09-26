#!/usr/bin/env python3
import subprocess
import webbrowser

import qrcode

SEC = "<WEP|WPA|blank>"
HIDDEN = "<true|false|blank>"
FMT = "WIFI:S:{ssid};T:{sec};P:{passw};H:{hidden};;"

CMD = "nmcli -t -f active,ssid dev wifi"

def get_ssid():
    ssid = subprocess.run(CMD.split(' '), capture_output=True)
    for l in ssid.stdout.decode().split('\n'):
        if l.startswith("yes:"):
            return l[4:]
    raise Exception("No SSID Found")

def main():
    ssid = get_ssid()
    names = [
        f"/etc/NetworkManager/system-connections/{ssid}.nmconnection",
        f"/etc/NetworkManager/system-connections/Auto {ssid}.nmconnection",
    ]
    passw = ""
    for fn in names:
        nmco = subprocess.run(f"sudo cat \"{fn}\"", shell=True, stdin=subprocess.PIPE, capture_output=True)
        for l in nmco.stdout.decode().split('\n'):
            if l.startswith('psk='):
                passw = l[4:]
        if passw:
            break
    if not passw:
        raise Exception(f'password not found in {fn}')
    data = FMT.format(ssid=ssid, sec='WPA', passw=passw, hidden="false")
    img = qrcode.make(data)
    img.save('/tmp/qrpass.png')
    print("Opening in browser...")
    webbrowser.open("file:///tmp/qrpass.png")

if __name__ == "__main__":
    main()

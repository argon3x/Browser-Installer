#!/usr/bin/python3
# coding: utf-8
from time import sleep
import signal, sys, os, subprocess, requests, hashlib

### --------------------------------------------------
### By: Argon3x
### Supported: Debian 10, 11 and Debian Based Systems
### Version: 1.0
### --------------------------------------------------

# Colors
green = "\033[01;32m"; blue = "\033[01;34m"; red = "\033[01;31m"
purple = "\033[01;35m"; yellow = "\033[01;33m"; end = "\033[00m"

# Context
box = f"{purple}[{green}*{purple}]{end}"

# Signals (interrupt and caceled)
def interrupt_handler(signum, frame):
    sys.stdout.write(f"{blue}>>> {red}Proccess Canceled {blue}<<<{end}")
    sys.exit(1)

def error_handler(error):
    sys.stdout.write(f"{red}Error{end}: {error}")
    sys.exit(1)

# call the signals
signal.signal(signal.SIGINT, interrupt_handler)
signal.signal(signal.SIGTERM, error_handler)


def downloading_chrome():
    # updating hash
    hash_sha256 = "6f700ff90db3a0f72ed9fb7ccbce31bd2f937366ed9b80d3ee0dafab7ba0693e"
    url = "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
    filename = "google-chrome-stable_current_amd64.deb"

    if os.path.exists(filename):
        error_handler(error=f"The {filename} File Already Exists\n")
    else:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        with open(filename, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
            if  file_hash == hash_sha256:
                print(f"{box} {green}Google Chrome Successfully...........{end}")
            else:
                error_handler(error="An Occurred Error While Downloading Google Chrome")


def install_chrome():
    command = ["sudo", "apt", "install", "./google-chrome-stable_current_amd64.deb"]

    install = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    if install.returncode == 0:
        print(f"\n{green}------------------------------------------------{end}")
        print(f" {purple}Google Chrome {green}Was Successfully Installed{end}")
        print(f"{green}------------------------------------------------{end}\n")
    else:
        error_handler(error="An Error Occurred While Install Google Chrome")

if __name__ == '__main__':
    os.system('clear')

    if os.getuid() == 0:
        print(f"\n{box} {yellow}Dowloading {purple}Google Chrome{yellow}............{end}") 
        downloading_chrome()
        sleep(1)

        print(f"\n{box} {yellow}Installing {purple}Google Chrome{yellow}...........{end}")
        install_chrome()
        sleep(1)

        os.system("rm -f google-chrome-stable_current_amd64.deb")
    else:
        print(f"\n{red}-------------------------------------------------{end}")
        print(f"{purple} Run The Script As Root{end}: {green}sudo ./InstallChrome.py{end}")
        print(f"{red}-------------------------------------------------{end}\n")


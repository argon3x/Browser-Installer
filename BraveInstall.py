#!/usr/bin/python3
# coding: utf-8
from time import sleep
import signal, sys, os, subprocess

### --------------------------------------------------
### By: Argon3x
### Supported: Debian 10, 11 and Debian Based Systems
### Version: 1.0
### --------------------------------------------------

# Colors
green = "\033[01;32m"; red = "\033[01;31m"; blue = "\033[01;34m"
purple = "\033[01;35m"; yellow = "\033[01;33m"; end = "\033[00m"

# Context
box = f"{purple}[{green}*{purple}]{end}"

# Function - interrupt and error
def interrupt_handler(signum, frame):
    sys.stdout.write(f"{blue}>>> {red}Process Canceled {blue}<<<{end}")
    sys.exit(1)

def error_handler(error):
    sys.stdout.write(f"{red}Error{end}: {error}")
    sys.exit(1)

# Call the functions
signal.signal(signal.SIGINT, interrupt_handler)
signal.signal(signal.SIGTERM, error_handler)


# Checking Dependencies
def check_dependencies():
    dependencies = ['curl', 'apt-transport-https']
    
    for d in dependencies:
        result = subprocess.check_output(["dpkg-query", "-W", "-f='${Status}'", d])
        status = result.decode().strip()

        if status == "'install ok installed'":
            print(f"{box} {green}{d} {yellow}Is Already Installed{end}")
        else:
            print(f"{box} {red}{d} {yellow}Is Not Installed{blue}, {yellow}Will Be Installed Automatically{end}")
            install = subprocess.run(["sudo", "apt-get", "install", d, "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            
            if install.returncode == 0:
                print(f"{box} {green}{d} {yellow}Was Installed{end}")
                sleep(1)
            else:
                error_handler(error=f"Error Installing {d}")


def download_gpg_key():
    command = ["sudo", "curl", "-fsSLo", "/usr/share/keyrings/brave-browser-archive-keyring.gpg", "https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg"]
    permission = ["sudo", "chmod", "644", "/usr/share/keyrings/brave-browser-archive-keyring.gpg"]

    download = subprocess.run(command, check=True)
    permissions = subprocess.run(permission, check=True)

    if download.returncode == 0 and permissions.returncode == 0 :
        print(f"{box} {green}GPG Key Downloaded and Added{end}")
    else:
        error_handler(error="Error downloading GPG Key and adding it\n")


def creating_repository():
    file_path = "/etc/apt/sources.list.d/brave-browser-release.list"
    content = "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main"

    with open(file_path, 'w') as f:
         f.write(content)

    chown = ["sudo", "chown", "root:root", file_path]
    chmod = ["sudo", "chmod", "644", file_path]
    
    owner = subprocess.run(chown, check=True)
    if owner.returncode == 0:
        permissions = subprocess.run(chmod, check=True)
        if permissions.returncode == 0:
            print(f"{box} {green}The Repository Was Created Successfully............{end}")
        else:
            error_handler(error="An Error Occurred While Giving Permissions To The Repository\n")
    else:
        error_handler(error="An Error Occurred When Changing Owner To Root\n")
    

def updating_repository():
    updating = subprocess.run(["sudo", "apt", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    if updating.returncode == 0:
        print(f"{box} {green}Repositories Updated Successfully...........{end}")
    else:
        error_handler(error="An Error Occurred While Updating The Repositories")


def install_brave():
    install = subprocess.run(["sudo", "apt", "install", "brave-browser", "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    if install.returncode == 0:
        print(f"\n{green}--------------------------------------------{end}")
        print(f"{purple}  Brave Browser {green}Was Successfully Installed {end}")
        print(f"{green}--------------------------------------------{end}\n")
    else:
        error_handler(error="An Error Occurred While Installling Brave Browser")


if __name__ == '__main__':
    os.system('clear')

    if os.getuid() == 0:
        print(f"\n{box} {yellow}Starting Installation Process {blue}({purple}Brave Browser{blue}){yellow}...........{end}")
        sleep(1)

        print(f"\n{box} {yellow}Checking Dependencies...........{end}")
        check_dependencies()
        sleep(1)

        print(f"\n{box} {yellow}Downloading GPG Key...........{end}")
        download_gpg_key()
        sleep(1)

        print(f"\n{box} {yellow}Creating The {purple}Brave-Browser {yellow}Repository...........{end}")
        creating_repository()
        sleep(1)

        print(f"\n{box} {yellow}Updating Repository...........{end}")
        updating_repository()
        sleep(1)

        print(f"\n{box} {yellow}Installing {purple}Brave Browser{yellow}...........{end}") 
        install_brave()
        sleep(1)
    else:
        print(f"\n{red}------------------------------------------------{end}")
        print(f"{purple} Run The Script As Root{end}: {green}sudo ./InstallBrave.py{end}")
        print(f"{red}------------------------------------------------{end}\n")


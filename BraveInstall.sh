#!/bin/bash
 
### --------------------------------------------------
### By: Argon3x
### Supported: Debian 10, 11 and Debian Based Systems
### Version: 1.0
### --------------------------------------------------

# Colors
green="\e[01;32m"; blue="\e[01;34m";
yellow="\e[01;33m"; red="\e[01;31m";
end="\e[00m"

CTRL_C(){
	echo -e "\n${red}>>> ${blue}Process Canceled${red} <<<${end}\n"
	tput cnorm
	exit 0
}
trap CTRL_C INT


INSTALL_DEPENDENCY(){
	sleep 1
	local dep=('apt-transport-https' 'curl')

	echo -e "${yellow}Installing dependencys......${end}"

	for list in ${dep[@]}; do
		echo -e "${yellow}Installing ${green}${list}${yellow}.......${end}\c"
		`sudo apt install ${list} -y > /dev/null 2>&1`
		if [[ $? -eq 0 ]]; then
			echo -e "${green} done ${end}"
		else
			echo -e "${red} faild ${end}"
			echo -e "${red} Ocurred an error to install ${blue}${list}${end}"
			exit 1
		fi
	done
}

INSTALL_BRAVE(){
	sleep 1
	echo -e "${yellow}Adding key GPG of Brave.......${end}\c"
	`sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg >/dev/null 2>&1`
	if [[ $? -eq 0 ]]; then
		echo -e "${green} done ${end}"
	else
		echo -e "${red} faild ${end}"
		echo -e "${red} Ocurred an error to add key GPG${end}"
		exit 1
	fi
	
	sleep 1
	echo -e "${yellow}Adding repository of Brave.......-.${end}\c"
	`echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg arch=amd64] https://brave-browser-apt-release.s3.brave.com/ stable main"|sudo tee /etc/apt/sources.list.d/brave-browser-release.list > /dev/null 2>&1`
	if [[ $? -eq 0 ]]; then
		echo -e "${green} done ${end}"
	else
		echo -e "${red} faild ${end}"
		echo -e "${red}Ocurred an error to add repository${end}"
		exit 1
	fi

	sleep 1
	echo -e "${yellow}Updating repositorys........${end}\c"
	`sudo apt update > /dev/null 2>&1`
	if [[ $? -eq 0 ]]; then
		echo -e "${green} done ${end}"
	else
		echo -e "${red} faild ${end}"
		echo -e "${red} Ocurred an error to update repository${end}"
		exit 1
	fi

	sleep 1
	echo -e "${yellow}Installing Brave Browser.......${end}\c"
	`sudo apt install brave-browser -y > /dev/null 2>&1`
	if [[ $? -eq 0 ]]; then
		echo -e "${green} done ${end}"
	else
		echo -e "${red} faild ${end}"
		echo -e "${red}Ocurred an error to install brave browser${end}"
		exit 1
	fi
}

if [[ $(id -u) -eq 0 ]]; then
	tput civis
	INSTALL_DEPENDENCY
	INSTALL_BRAVE
	tput cnorm
else
	echo -e "${blue}use: ${green}sudo ${yellow}${0}${end}"
fi

#!/usr/bin/bash

# colors
grn="\e[01;32m"
rd="\e[01;31m"
blu="\e[01;34m"
yell="\e[01;33m"
end="\e[00m"

# cancel the script process
signal_cancel(){
  echo -e "${rd} process canceled ${end}"
  exit 1
}
trap signal_cancel SIGINT

# script execution terminates due to an error
error(){
  local type_error=$1
  echo -e "\n[${rd}ERROR${end}] ${type_error}\n"
  exit 1
}
trap error SIGTERM

# Check that the execution status code is correct,
# otherwise the script ends with an error
status_code(){
  local code=$1
  local msg=$2

  if [[ $code -eq 0 ]]; then
      echo -e "${grn} OK ${end}"
  else
      echo -e "${rd} Failed ${end}"
      error $msg
  fi
}

# install the necessary dependencies, of the distribution
install_dependencies(){
  local package_manager=$1
  local packages=($2)
  local update_repos=$3

  # execute this block of code to avoid repeating the code of installing packages this block
  # is executed to synchronize the repositories
  if [[ -n $update_repos && $update_repos == 'true' ]]; then
    echo -e "${grn}[*] ${blu}synchronizing repositories${end}... \c"

    if [[ $package_manager == 'apt' ]]; then
      (sudo $package_manager update &>/dev/null)
      status_code $? "repositories could not be synchronized" 

    elif [[ $package_manager == 'dnf' ]]; then
      (sudo $package_manager makecache &>/dev/null)
      status_code $? "repositories could not be synchronized" 
    fi
  fi

  for package in ${packages[@]}; do
    echo -e "${blu}[+]${end} installing ${grn}${package}${end}... \c"

    (sudo $package_manager install -y $package &>/dev/null)
    status_code $? "${package} package could not be install" 
  done
}

# install brave and its dependencies depending on the distribution
brave_install(){
  local os=${1,,}
  local apt_package_manager=(debian ubuntu linuxmint kali)
  local rpm_package_manager=(almalinux fedora centos)

  echo -e "${blu}[*]${end} installing dependencies"

  # check the distribution type
  if [[ ${apt_package_manager[*]} =~ $os ]]; then
    echo -e "${blu}[+]${end} ${grn}${os}${end} is the current distribution..."
    # install dependencies
    install_dependencies "apt" "curl apt-transport-https"

    # add key gpg
    echo -e "${blu}[*]${end} adding key GPG... \c"
    (sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg &>/dev/null)
    status_code $? "failed to add GPG key"
    
    # add the repository
    echo -e "${blu}[*]${end} adding repository... \c"
    (echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list &>/dev/null)
    status_code $? "could not add repository"

    install_dependencies "apt" "brave-browser" "true"

  elif [[ ${rpm_package_manager[*]} =~ $os ]]; then
    echo -e "${blu}[+]${end} ${grn}${os}${end} is the current distribution..."
    # install dependencies
    install_dependencies "dnf" "dnf-plugins-core"

    # add the repository
    echo -e "${blu}[*]${end} adding repository... \c"
    (sudo dnf config-manager --add-repo https://brave-browser-rpm-release.s3.brave.com/brave-browser.repo)
    status_code $? "could not add repository"

    # add key gpg
    echo -e "${blu}[*]${end} adding key... \c"
    (sudo rpm --import https://brave-browser-rpm-release.s3.brave.com/brave-core.asc)
    status_code $? "failed to add key"

    install_dependencies "dnf" "brave-browser" "true"
  else
    error "unsupported system"
  fi
}

# check that the script, run with sudo
if [[ $(id -u) -eq 0 ]]; then
  echo -e "\n${grn}${0##*/}${end} v1.0.0-${blu}beta${end}\n"; sleep 1

  # check that brave-browser is already installed
  if [[ -e '/usr/bin/brave-browser-stable' ]]; then
    echo -e "\n[${blu}OK${end}] ${grn}Brave-Browser${end} already exists..!\n"
    exit 0
  fi

  os=$(grep '^ID' '/etc/os-release' | awk -F '=' '{print $2}')

  brave_install $os
else
  error "the script must be run with ${grn}sudo${end} privileges"
fi

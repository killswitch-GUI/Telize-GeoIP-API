#!/bin/bash

# Current supported platforms:
#   Kali-Linux
# Global Variables

# Title Function
func_title(){
  # Clear (For Prettyness)
  clear

  # Echo Title
  echo '=========================================================================='
  echo ' Setup Script | [Updated]: '
  echo '=========================================================================='
  echo ' [Web]: https://www. | [Twitter]: @'
  echo '=========================================================================='
}

# Environment Checks
func_check_env(){
  # Check Sudo Dependency going to need that!
  if [ $(which sudo|wc -l) -eq '0' ]; then
    echo
    echo ' [ERROR]: This Setup Script Requires sudo!'
    echo '          Please Install sudo Then Run This Setup Again.'
    echo
    exit 1
  fi
}

func_install_requests(){
  echo ' [*] Installing and updating requests libary'
  #Insure we have the latest requests module in python
  sudo pip install --upgrade requests
  sudo pip install geoip2
  sudo pip install geoip2 --upgrade
  echo ' [*] Installing GeoIP2 DB required'
  sudo wget http://cybersyndicates.com/wp-content/uploads/2015/08/GeoLite2-Country.mmdb_.zip
  sudo unzip -o GeoLite2-Country.mmdb_.zip
  sudo sudo rm GeoLite2-Country.mmdb_.zip
  echo ' [*] all required updated'

}

# Menu Case Statement
case $1 in
  *)
  func_title
  func_check_env
  func_install_requests
  ;;

esac
# hera-led
Contains all the relevant parts to create your own live HERA LED display.  
  
HERAlive.py is the main code. It shows the live status of HERA according to the dashboard.  
HERAtest.py is a playground with many different displays to use. Comment and uncomment lines under main() to change what displays.  
  
On the LoCo lab board, HERAlive is setup to run via systemd so that it automatically begins at startup.  
If it is not running, use the following sequence of commands to restart it.
  
sudo systemctl stop HERAlive  
sudo systemctl daemon-reload  
sudo systemctl start HERAlive  

# Installation 
Some terse clues to installation on a RPi 3B+
 - Currently running Raspbian 2022 (64 bit).
 - These lights are WS281X addressable type. 
 - The best drivers as of 2023 are found by googling Arduino Circuit Python.  
 - The RPi drivers use the linux audio system to generate the PWM signals on P18.  For this to work one must disable the audio system.
In /boot/config.txt
# Enable audio (loads snd_bcm2835)
#dtparam=audio=on
 
At the same time I also disabled the routing of audio to hdmi. This is probably redundant but I didn't feel like AB testing/
Also in /boot/config.txt

hdmi_force_hotplug=1
hdmi_force_edid_audio=1



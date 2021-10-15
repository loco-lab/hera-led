# hera-led
Contains all the relevant parts to create your own live HERA LED display.

HERAlive.py is the main code. It shows the live status of HERA according to the dashboard.

HERAtest.py is a playground with many different displays to use. Comment and uncomment lines under main() to change what displays.



On the LoCo lab board, HERAlive is setup to run via systemd so that it automatically begins at startup. 

If it is not running, use the following sequence of commands to restart it.

sudo systemctl stop HERAlive

sudo systemctl daemon-reload

sudo systemctl start HERAlive

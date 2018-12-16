**support for Sonic Pi control via OSC**

*Release 1*

The additonal files enable Spirograph drawing to be controlled from the free music program Sonic Pi (sonic-pi.net).
control is achieved by sending OSC messages to a python OSCserver, which in turn control Spirograph.py using a script
spiroRun.py

Spirograph.py and associated files have been converted to run under python3, as this is required by the version of
the python-osc library employed to support the OSC communication.

**Setting Up**

Clone the repository to a suitable location on your computer.
(I used a Mac. I haven't yet tested other computers)

Open Sonic Pi and load the program spiro.rb into an available buffer.

Open a terminal and navigate to the Spirograph folder

Install python-osc library using `pip3 install python-osc`

Run the OSC server using `python3 spiroOSCserver.py`

Run the program spiro in Sonic Pi to generate 7 drawings each accompanied by music

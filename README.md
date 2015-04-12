# ConkyTransmission
Python script to display torrents from Transmission in Conky. Output is customizable usign basi templates.

#Usage/Features:
- Use templates to customize output
- Connects to Transmission using 'transmission-remote'. Consult the Transmission documentation for details; search your distro's repos for a package providing the 'transmission-remote' command.
- Invoke from a Conky script using ${execpi interval runDefault.sh}. Customize runDefault.sh as needed.

#Problems/ToDo:
This is written many years ago and is unmaintained. There are no guarantees it still works. I don't even know if transmission-remote is still being distributed.

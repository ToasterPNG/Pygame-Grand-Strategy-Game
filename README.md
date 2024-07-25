# Pygame-Grand-Strategy-Game
Engine for pygame strategy games I might use later for bigger multiplayer strategy games

What the PDF says :

# ─ Documentation ─

All the information you need to run the game, make
you own servers and maps are in this PDF.
Table of contents :
How To Run The Game
And Information On Servers (pages 2 – 4)
How To Make A Custom Map (page 5)

## How To Run The Game (through interpreter)

Other than running the compiled version if you want to run
the source code run the Install Dependencies batch file in the
tools folder once you have python installed and pip added to
your systems path variable.
Note that you may need to uninstall some of these libraries if
you already have them, for example you may need to uninstall
the requests library through the command “pip uninstall
requests” if its not already version 2.31.0

________________

Other then this once you are actually running the game there
are some things to note about how the servers and the game
works.
If you get this message while trying to join a server but you
know for sure there are no players in that server then run the
reset server batch file in the main directory.
This will reset the server data
of the last server you joined so you
can join it again.
(last server you joined is stored in
data\current_server.txt)

Note that in the compiled version all references to file
directories can be found in the binaries folder.
Another important thing to know about how servers work in
this game is that if the game crashes there is a possibility the
port you are currently playing on is overloaded.
If this is the case users can switch the current port by running
the ports batch file or by viewing the server_list/view page on
the website host of the given server to figure out which ports
are online and then edit the data\server_id.txt file to a
currently online port.
Switching ports wont loose any progress if the server stays the
same.

Note that the website server list viewer only gets updated once
somebody runs the ports batch file so id recommend you do
that instead of viewing it from the website

________
Once you have this understanding of servers you can
make your own if you want to make a mod of the game or a
custom server for traffic reasons.
Note that you also need an understanding of python and flask
to do so.
To make a custom server you want to find a host for a python
flask server such as pythonanwhere which I use because is
free.
Note that when choosing a host you need to consider that the
server will be pinged numerous times because the game
doesn’t use sockets but just downloads and sends json files to
the same server.

All of the files to the server can be
found in the tools\server template
directory of the project.

Make sure to use a version of python
around 3.10 and a up to date web frame
work ( flask, django, web2py, etc… )

If you do end up making a custom server for the game email it
to rts71937@gmail.com so I can add it to the game.

Note this error means you
missed adding the identifier
page which returns this
string “9782364928734”

How To Make A Map
The structure of map folders are fairly strait forward, the
folder is the maps name, the maps name plus _c.png is the file
which assigns a unique color to each province, the maps name

plus a _o.png is the overlay (outline showing borders for
example)

And the file with just the maps name is the blacked out
version of the maps color version (map_c.png)
The config json file should be structured like this:
If you have any issues look at how other map folders do it.
If you are having trouble getting the colors of your map_c file
correct then I suggest using this website :
https://www.dustfreesolutions.com/CT/CT.html
Note in the game you can
press the slash key when its
your turn to check the
borders of provinces and
help you figure out errors in
the config json file.

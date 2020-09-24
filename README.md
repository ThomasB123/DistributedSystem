See ds.assignment.2020.pdf for details.


I have used 5 external libraries in total:
Pyro4, uuid, json, urllib, urllib.request, and math
All of these (except Pyro4) are installed on university machines

To install Pyro4 with pip:
pip install Pyro4

To run my distributed system from the command line:

In seperate shell/console tabs/windows, run the following commands
In this order:

1. python -m Pyro4.naming

start the 3 servers and the front end: (order here is irrelevant)
2. python R0.py
3. python R1.py
4. python R2.py
5. python frontEnd.py

Then start a client:
6. python client.py

you may have to change 'python' to 'python3.x' depending on your setup

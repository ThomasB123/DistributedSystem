
import Pyro4
import json
import urllib
import urllib.request
from math import cos, asin, sqrt

@Pyro4.expose
class server(object):
    
    def update(self, x, out): # update self, then send updates to other servers
        requestID.append(x)
        response.append(out)
        try:
            R0.getUpdate("R1", requestID, response)
        except:
            pass
        try:
            R2.getUpdate("R1", requestID, response)
        except:
            pass

    def getUpdate(self, sentBy, newRequestID, newResponse): # receive updates from other servers
        requestID = newRequestID
        response = newResponse
        # send an acknowledgement
        if sentBy == "R0":
            return R0.ack("R1")
        elif sentBy == "R2":
            return R2.ack("R1")
    
    def ack(self, sentBy):
        return True

    def validatePostcode(self, x, postcode):
        if x not in requestID: # handle message loss
            try:
                j = urllib.request.urlopen("http://api.postcodes.io/postcodes/{0}/validate".format(postcode))
                reply = j.read().decode("utf-8")
                js = json.loads(reply)
                if js["status"] != 200:
                    out = False
                else:
                    out = js["result"]
            except:
                out = False
            self.update(x, out)
        else:
            out = response[requestID.index(x)]
        return out

    def getDistance(self, x, postcode):
        if x not in requestID:
            j = urllib.request.urlopen("http://api.postcodes.io/postcodes/{0}".format("DH13LE")) # Durham University Postcode
            reply = j.read().decode("utf-8")
            js = json.loads(reply)
            lat1 = js["result"]["latitude"]
            lon1 = js["result"]["longitude"]
            j = urllib.request.urlopen("http://api.postcodes.io/postcodes/{0}".format(postcode)) # user postcode
            reply = j.read().decode("utf-8")
            js = json.loads(reply)
            lat2 = js["result"]["latitude"]
            lon2 = js["result"]["longitude"]
            p = 0.017453292519943295 #Pi/180
            a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
            out = round(12742 * asin(sqrt(a)), 1)
            self.update(x, out)
        else:
            out = response[requestID.index(x)]
        return out
    
    def checkDistance(self, x, distance):
        if x not in requestID:
            if distance <= 50 and distance >= 0:
                out = True
            else:
                out = False
            self.update(x, out)
        else:
            out = response[requestID.index(x)]
        return out

    def getMenu(self, x):
        if x not in requestID:
            out = ""
            for i in range(len(items)):
                item = "{0}. {1} (£{2})\n".format(i+1, items[i], prices[i])
                out += item
            out += "q. Checkout\n"
            self.update(x, out)
        else:
            out = response[requestID.index(x)]
        return out
    
    def getItems(self, x):
        if x not in requestID:
            out = items
            self.update(x, out)
        else:
            out = response[requestID.index(x)]
        return out
    
    def getCost(self, x, basket): # return cost of basket
        if x not in requestID:
            out = 0
            for x in basket:
                out += prices[items.index(x)]
            self.update(x, out)
        else:
            out = response[requestID.index(x)]
        return out
    
    def deliveryTime(self, x, distance):
        if x not in requestID:
            if distance <= 10:
                out = 10
            elif distance <= 20:
                out = 20
            elif distance <= 30:
                out = 30
            elif distance <= 40:
                out = 40
            elif distance <= 50:
                out = 50
            self.update(x, out)
        else:
            out = response[requestID.index(x)]
        return out

if __name__ == "__main__":
    daemon = Pyro4.Daemon() # make a Pyro daemon
    ns = Pyro4.locateNS() # find the name server

    uri = daemon.register(server) # register the JustHungry class as a Pyro object
    ns.register("R1", uri) # register the object with a name in the name server

    requestID = [] # will contain unique request ID's from the Front End
    response = [] # what the server's response was

    items = ["Burger", "Wings", "Kebab", "Pizza", "Pasta", "Chips", "Rice"] # name of each item on the menu
    prices = [5, 6, 4, 8, 9, 2, 1] # cost of each item in £

    R0 = Pyro4.Proxy("PYRONAME:R0") # another server
    R2 = Pyro4.Proxy("PYRONAME:R2") # another server

    print("Ready.")
    daemon.requestLoop() # start the event loop of the server to wait for calls

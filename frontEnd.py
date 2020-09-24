
import Pyro4
import uuid # used to generate unique ID for each request
# uuid.uuid1() generates a random unique ID based on current time

@Pyro4.expose
class front(object):

    def newPrimary(self):
        global primaryName
        global primary
        if primaryName == "R0":
            primaryName = "R1"
        elif primaryName == "R1":
            primaryName = "R2"
        elif primaryName == "R2":
            primaryName = "R0"
        primary = Pyro4.Proxy("PYRONAME:" + primaryName) # use name server object lookup uri shortcut
        print("switched primary to {0}".format(primaryName))

    def validatePostcode(self, postcode):
        x = uuid.uuid1()
        for i in range(3):
            try:
                return primary.validatePostcode(x, postcode)
            except:
                self.newPrimary()
        return None

    def getDistance(self, postcode):
        x = uuid.uuid1()
        for i in range(3):
            try:
                return primary.getDistance(x, postcode)
            except:
                self.newPrimary()
        return None

    def checkDistance(self, postcode):
        x = uuid.uuid1()
        for i in range(3):
            try:
                return primary.checkDistance(x, postcode)
            except:
                self.newPrimary()
        return None

    def getMenu(self):
        x = uuid.uuid1()
        for i in range(3):
            try:
                return primary.getMenu(x)
            except:
                self.newPrimary()
        return None
    
    def getItems(self):
        x = uuid.uuid1()
        for i in range(3):
            try:
                return primary.getItems(x)
            except:
                self.newPrimary()
        return None
    
    def getCost(self, basket):
        x = uuid.uuid1()
        for i in range(3):
            try:
                return primary.getCost(x, basket)
            except:
                self.newPrimary()
        return None
    
    def deliveryTime(self, distance):
        x = uuid.uuid1()
        for i in range(3):
            try:
                return primary.deliveryTime(x, distance)
            except:
                self.newPrimary()
        return None

if __name__ == "__main__":
    daemon = Pyro4.Daemon() # make a Pyro daemon
    ns = Pyro4.locateNS() # find the name server
    uri = daemon.register(front) # register the JustHungry class as a Pyro object
    ns.register("frontEnd", uri) # register the object with a name in the name server
    primaryName = "R0"
    primary = Pyro4.Proxy("PYRONAME:" + primaryName) # use name server object lookup uri shortcut
    client = Pyro4.Proxy("PYRONAME:client")
    print("Ready.")
    daemon.requestLoop() # start the event loop of the server to wait for calls

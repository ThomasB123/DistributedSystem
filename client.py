
import Pyro4

def welcome():
    print("\nHello and welcome to Just Hungry, the online food ordering service.\n")
    name = ""
    while name == "":
        name = input("What is your name? > ").strip()
    print("\nHello {0}, nice to meet you.".format(name))
    print("\nLet's check if we can deliver to you:")
    return name

def validatePostcode():
    validPostcode = False
    while not validPostcode:
        postcode = input("Enter your postcode > ").strip()
        if postcode != "":
            validPostcode = front.validatePostcode(postcode)
            if validPostcode is None:
                print("\nAll servers returned errors.\n")
                return None
        if not validPostcode:
            print("That is not a valid postcode, try again")
    return postcode

def getDistance():
    distance = front.getDistance(postcode)
    if distance is None:
        print("\nAll servers returned errors.\n")
        return None
    return distance

def checkDistance():
    deliver = front.checkDistance(distance)
    if deliver is None:
        print("\nAll servers returned errors.\n")
        return None
    if deliver:
        print("Excellent news {0}, you are within our delivery radius!\n".format(name))
    else:
        print("Sorry {0}, you are {1} kilometres away from Durham, which is outside our 50km delivery radius.".format(name, distance))
        print("We are unable to deliver to you.")
        print("Goodbye.")
        return None
    return True

def menu():
    options = front.getMenu()
    if options is None:
        print("\nAll servers returned errors.\n")
        return None
    items = front.getItems()
    if items is None:
        print("\nAll servers returned errors.\n")
        return None
    print("Here is the Just Hungry menu:")
    checkout = False 
    while not checkout:
        print("To add food to your order, enter it's number:")
        print(options)
        validChoice = False
        while not validChoice:
            choice = input("Your Choice > ").strip()
            if choice.upper() != "Q":
                try:
                    val = int(choice)
                except:
                    print("That is not a valid choice.")   
                else:
                    if val >= 1 and val <= len(items):
                        item = items[val-1]
                        basket.append(item)
                        print("You added {0} to your basket".format(item))
                        cost = front.getCost(basket)
                        if cost is None:
                            print("\nAll servers returned errors.\n")
                            return None
                        if len(basket) == 1:
                            print("The cost of your {0} item is £{1}\n".format(len(basket),cost))
                        else:
                            print("The cost of your {0} items is £{1}\n".format(len(basket),cost))
                        validChoice = True
                    else:
                        print("That is not a valid choice.")
            else:        
                checkout = True
                validChoice = True
    return True

def checkout():
    print("\nYou are now at the checkout.\n")
    if basket == []:
        print("Your basket is empty.\n")
        print("Goodbye.\n")
        return None
    print("Here is what you ordered:")
    for x in basket:
        print(x)
    cost = front.getCost(basket)
    if cost is None:
        print("\nAll servers returned errors.\n")
        return None
    print("\nThe total cost of your order is £{0}.\n".format(cost))
    time = front.deliveryTime(distance)
    if time is None:
        print("\nAll servers returned errors.\n")
        return None
    print("Since you are {0}km away, your food will arrive in {1} minutes.\n".format(distance, time))
    print("Thank you for ordering with Just Hungry.\n")
    print("Enjoy you food, {0}.\n".format(name))
    return True

if __name__ == "__main__":
    front = Pyro4.Proxy("PYRONAME:frontEnd") # use name server object lookup uri shortcut
    basket = []
    name = welcome()
    try:
        postcode = validatePostcode()
    except:
        print("\nCannot connect to front end server\n")
        raise SystemExit
    else:
        if postcode is None:
            raise SystemExit
    try:
        distance = getDistance()
    except:
        print("\nCannot connect to front end server\n")
        raise SystemExit
    else:
        if distance is None:
            raise SystemExit
    try:
        check = checkDistance()
    except:
        print("\nCannot connect to front end server\n")
        raise SystemExit
    else:
        if check is None:
            raise SystemExit
    try:
        check = menu()
    except:
        print("\nCannot connect to front end server\n")
        raise SystemExit
    else:
        if check is None:
            raise SystemExit
    try:
        check = checkout()
    except:
        print("\nCannot connect to front end server\n")
        raise SystemExit
    else:
        if check is None:
            raise SystemExit

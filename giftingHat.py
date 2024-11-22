import sys, csv
from random import randint, shuffle

class GiftingHat():
    '''
    A class that accepts a dictionary of name pairs and creates a gifting list for the group
    derived from the name pairs, and which conforms to a selectable set of rules.  
    
    Name pairs in the dictionary indicate spousal or significant other relationships. 
    Singles are represented with key-value pairs of "name" : "None" or "name" : "".  
    Names (either key or value) used in the dictionary must all be unique.
      - Use a naming strategy like: "BobRoberts", "BobRoss", "BobLoblaw" if necessary.

    The getGiftingPairs() method will return a set of giver : receiver pairs in a dictionary
    which conform to estabished / configured rules:
    * A giver cannot receive from themselves
    * If self.crossGift is False, if A gives to B, then B cannot give to A. Otherwise this is allowed.
    * If self.spousalGift is False, a giver cannot give to their spouse or significant other.

      - crossGift and spousalGift can be set during initialization, but default to False.

    If after 100 attempts, getGiftingPairs() fails to create a valid gift pair directory, it will return
    a value of "None".
      
    The output2File() method receives no input parameters and manages the user interaction related to
    saving gifting pair results to a text file.
    '''
    def __init__(self, namePairs, crossGift=False, spousalGift=False):
        self.namePairs = dict(namePairs)
        self.participants = []
        self.crossGift = crossGift
        self.spousalGift = spousalGift
        for name in namePairs:
            self.participants.append(name)
            if namePairs[name] != None and namePairs[name] != "":
                self.participants.append(namePairs[name])
                self.namePairs[namePairs[name]] = name
            else:
                self.namePairs[name] = name
        # Check for uniquness in list of participants
        if len(self.participants) > len(set(self.participants)):
            sys.exit("List of participants is not unique")
        self.giftPairs = {}                     # Make an empty dictionary that holds giver : receiver pairs

    def getGiftingPairs(self):
        looking = True
        lookCount = 1
        shuffle(self.participants)              # Add a little more random spice...
        while looking:                          # While looking for acceptable pairings
            self.giftPairs = {}                 # Make a fresh dictionary on each attempt to find acceptable pairings
            toList = list(self.participants)    # Make a "fresh" toList on each attempt to find acceptable pairings
            length = len(toList)
            for giver in self.participants:     # Loop through each participant as a giver
                spouse = self.namePairs[giver]  # Find the giver's spouse
                searching = True
                while searching:                # While searching for a valid receiver
                    receiver = toList[randint(0, length-1)]
                    if length > 2:              # Careful not to get stuck on the last two assignments...
                        if receiver != giver and receiver != spouse:
                            searching = False
                    else:
                        searching = False       # Allow illegal matches on last 2 assignments to avoid hanging
                toList.remove(receiver)         # Found a receiver. Remove them from toList.
                length -= 1                     # length of toList is reduced by 1
                self.giftPairs[giver] = receiver     # Add giver : receiver to the giftPairs dictionary
            
            # Test for disallowed conditions and retry if found
            looking = False
            for giver in self.giftPairs:
                receiver = self.giftPairs[giver]
                if not self.crossGift and self.giftPairs[receiver] == giver:    # Detect cross-giving if not enabled
                    looking = True 
                if not self.spousalGift and receiver == self.namePairs[giver]:  # Detect Spouse-giving if not enabled
                    looking = True                
                if receiver == giver:                                           # Detect self-giving
                    looking = True
            
            # Test for too many times through the looking loop (i.e. you get stuck)
            lookCount += 1
            if lookCount > 100:
                looking = False
                print("getGiftingPairs failed to converge")
                return None
        # end while looking

        return self.giftPairs       # Return dictionary of giver : receiver pairs

    def output2File(self):
        print()
        while True:
            inp = input("Would you like to save to file? (Y/N) ").strip().upper()
            if inp == 'Y' or inp == 'N':
                break
        if inp == 'Y':
            while True:
                year = input("Please enter the current year: ")
                try:
                    yr = int(year)
                except ValueError:
                    pass
                else:
                    break
            fname = f"giftingHat{yr}.txt"
            
            # check if file already exists and ask user if they want to overwrite...
            exists = self.fileExists(fname)
            saveAnyway = False
            if exists:
                while True:
                    inp = input(f"{fname} already exists. Save anyway? (Y/N) ").strip().upper()
                    if inp == 'Y' or inp == 'N':
                        break
                if inp == 'Y':
                    saveAnyway = True
            if not exists or saveAnyway:    
                with open(fname, "w") as file:
                    file.write(f"Gift Pairings for {yr}\n\n")
                    for giver in self.giftPairs:
                        file.write(f"{giver} is giving to {self.giftPairs[giver]}.\n")
                print(f'Data saved to "{fname}".')

    def fileExists(self, fname):
        try:
            f = open(fname)
        except FileNotFoundError:
            return False
        else:
            f.close()
            return True


# Functions not in the GiftingHat() Class:

def inputCSV(csvFileName: str) -> dict:
    '''
    This function is not part of the GiftingHat class and is provided here for convenience.
    If "giftingHat.py" is imported to a user program, the function can be accessed in a
    manner similar to:
        
        pairs = giftingHat.inputCSV("filename.csv")
    
    If the rules below were followed in the creation of "filename.csv", then the directory
    "pairs" can be used to initialize a GiftingHat object of the class.

    Rules for creating a .csv file that defines pairs and singles for the GiftingHat class:
    * No header is expected
    * All names should be unique. If necessary, use firstnameLastname as name.  
        For example:
            "BobRoberts", "BobRoss" and "BobLoblaw" 
        are all unique.
    * Singles should have their name in the first column and "None" or blank in the second column.

    Here is an example of acceptable .csv content:

    Matt,Megan
    Brian,Cameron
    Jillian,Shawn
    BobRoberts,Isobel
    BobRoss,None
    BobLoblaw,
    '''
    
    pairsD = {}
    # test if csv exists
    try:
        file = open(csvFileName)
    except FileNotFoundError:
        sys.exit(f"{csvFileName} does not exist")
    else:
        reader = csv.reader(file)
        for name1, name2 in reader:
            if name2 == "None" or name2 == "":
                pairsD[name1] = None
            else:
                pairsD[name1] = name2
        file.close()

    return pairsD       # Return a dictionary of pairs ready to pass into GiftingHat on initialization.

def main():
    ''' 
    Here is a sample dictionary of Spouse Pairs to pass to a GiftingHat object on init. 
    Singles should be listed with name as key and None or "" as value.

    pairs = {
        "Matt" : "Megan",
        "Brian" : "Cameron",
        "Jillian" : "Shawn",
        "Bob" : None,
        "Tom" : "",
    }
    '''
   
    # Enter the pairs and singles you would like to process in the dictionary below:
    pairs = {
        "Matt" : "Megan",
        "Brian" : "Cameron",
        "Jillian" : "Shawn",
    } 

    # If valid csv file present as command line, pairs will be replaced with csv input
    if len(sys.argv) == 2:
        csvFile = sys.argv[1]
        if not(csvFile.endswith(".csv")):
            sys.exit("Invalid command-line parameter.")
        else:
            pairs = inputCSV(csvFile)
       
    giftHat = GiftingHat(pairs)             # Example using a pairs dictionary defined in code
    giftPairs = giftHat.getGiftingPairs()   # If getGiftingPairs() fails, it returns "None"
    if giftPairs:
        print()
        for giver in giftPairs:
            print(f"{giver} is giving to {giftPairs[giver]}")

    giftHat.output2File()
    print("\nProgram Ended")


if __name__ == "__main__":
    main()
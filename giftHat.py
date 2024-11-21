from random import randint, shuffle
'''
This is a non-object-oriented version of the GiftingHat() class contained in giftingHat.py.
Not all of the functionality contained in GiftingHat() class is included in this program.
This program is provided for reference and is not maintained.
'''

participants = ["Matt", "Megan", "Brian", "Cameron", "Jillian", "Shawn"]
spouses = {
    "Matt" : "Megan",
    "Brian" : "Cameron",
    "Jillian" : "Shawn",
    "Megan" : "Matt",
    "Cameron" : "Brian",
    "Shawn" : "Jillian",
}
def main():
    looking = True
    lookCount = 1
    shuffle(participants)               # Add a little more random spice...
    while looking:                      # While looking for acceptable pairings
        giftPairs = {}                  # Make an empty dictionary that will hold giver : receiver pairs
        toList = list(participants)     # Make a "fresh" toList each attempt to find acceptable pairings
        length = len(toList)
        for giver in participants:      # Loop through each participant as a giver
            spouse = spouses[giver]     # Find the giver's spouse
            searching = True
            while searching:            # While searching for a valid receiver
                receiver = toList[randint(0, length-1)]
                if length > 2:          # Careful not to get stuck on the last two assignments...
                    if receiver != giver and receiver != spouse:
                        searching = False
                else:
                    searching = False   # Allow illegal matches on last 2 assignments to avoid hanging
            toList.remove(receiver)     # Found a receiver. Remove them from toList.
            length -= 1                 # length of toList is reduced by 1
            giftPairs[giver] = receiver # Add giver : receiver to the giftPairs dictionary
        
        # Test for disallowed conditions
        looking = False
        for giver in giftPairs:
            receiver = giftPairs[giver]
            if giftPairs[receiver] == giver:
                looking = True 
                print("Cross-gifting detected")
            if receiver == giver:
                looking = True
                print("Self-gifting detected")
            if receiver == spouses[giver]:
                looking = True
                print("Spousal-gifting dectected")
        if looking:
            print(f"Retrying... (loop count = {lookCount})")
        
        # Test for too many times through the looking loop
        lookCount += 1
        if lookCount > 100:
            looking = False
            print("Program Failed to converge")
    # end while looking

    # Print pairing results to the terminal
    print("\nGifting Pairs:")
    for giver in giftPairs:
        print(f"{giver} is giving to {giftPairs[giver]}")
    print()

    # Save results to file if user wants to
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
        exists = fileExists(fname)
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
                for giver in giftPairs:
                    file.write(f"{giver} is giving to {giftPairs[giver]}.\n")
            print(f'Data saved to "{fname}".')
    elif inp == 'N':
        pass

    print("\nEnd Program")


def fileExists(fname):
    try:
        f = open(fname)
    except FileNotFoundError:
        return False
    else:
        f.close()
        return True


if __name__ == "__main__":
    main()


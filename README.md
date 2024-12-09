# The Gifting Hat
#### GiftingHat() is a Python class that accepts a dictionary of name pairs as a required input parameter and creates a gifting list for the group derived from the name pairs, and which conforms to a set of established and configurable rules.

Many thanks to my children who deliberately scratched my Python itch by asking me to write this program for our family use.  It was a gift they knew I couldn't resist...

The GiftingHat() class is contained within the file "giftingHat.py", which includes a main() function that exercises the class. Included in main() is the ability to accept a .csv file from the command line as input to the program.  See the section below regarding the inputCSV() function for usage and .csv formatting requirements.

## To Do
* ~~Add .csv file input via command line~~
* ~~Add requirement for .csv file header (Name,Spouse) to help with validation of .csv format~~
<br>

### Class Methods
#### \_\_init__(self, namePairs, crossGift=False, spousalGift=False)
The \_\_init__ method will build a GiftHat() object and from the namePairs dictionary input and then:
* Construct a participants list -
    * The participants list will checked for uniqueness. If name conflicts are found, the user will be notified that the list of participants is not unique, and the program terminated.
* Extend self.namePairs to contain bi-directional pairings - 
    * For example: if key-value pair "A" : "B" is contained in namePairs originally, then key-value pair "B" : "A" will be added to the namePairs dictionary. This step simplifies the algorithm used in the getGiftingPairs() method to create the gifting list.

##### Input parameters:
* namePairs : dict - Required. A dictionary whose key-value pairs represent spousal or "significant other" relationships. 
    * Names (either key or value) used in the input namePairs dictionary must all be unique. Use a naming strategy like: "BobRoberts", "BobRoss", "BobLoblaw" if necessary.
    * Singles are represented with key-value pairs of:
        * "name" : "None", or
        * "name" : "".
* crossGift : bool - Optional. True allows scenarios where A gives to B and B gives to A. Default is False.
* spousalGift : bool - Optional. True allows participants to give to their spouse or significant other. Default is False.

Here is an example of an appropriately constructed namePairs dictionary:
```python
pairs = {
    "Matt" : "Megan",
    "Brian" : "Cameron",
    "Jillian" : "Shawn",
    "BobRoss" : "Isobel",
    "BobRoberts" : "Harper",
    "BobLobLaw" : None,
    "BobsYourUncle" : "",
} 
```
#### getGiftingPairs(self) -> dict:
This method takes no input parameters and will return a dictionary containing giver : receiver pairs which conform to estabished / configured rules defined below:
1. A giver cannot receive a gift from themselves
1. If self.crossGift is False, if A gives to B, then B cannot give to A. If True, cross-gifting is allowed.
1. If self.spousalGift is False, a giver cannot give to their spouse or significant other. If True, spousal giving is allowed.

If after 100 attempts, getGiftingPairs() fails to create a valid gift pair dictionary as defined by the rules above, it will return a value of "None".

#### output2File(self)
This method receives no input parameters and manages the user interaction related to saving gifting pair results to a text file.

#### fileExists(self, fname) -> bool:
This method receives a text file name and returns True if the file exists in the file system and False if it does not.

### Non-Class Functions
#### inputCSV(csvFileName: str) -> dict:
This function is not part of the GiftingHat class and is provided in the library for convenience.
If "giftingHat.py" is imported into a user program, the inputCSV() function can be used in a manner similar to this:
```python
pairs = giftingHat.inputCSV("filename.csv")
myHat = giftingHat.GiftingHat(pairs)
```
If the rules below were followed in the creation of "filename.csv", then "pairs" can be used as a namePairs dictionary in the initialization a GiftingHat() object as shown in the code above.

The rules for creating a .csv file that defines pairs and singles for the GiftingHat class are:
* A header row is expected, which should be: "Name", "Spouse"
* All names should be unique. If necessary, use firstnameLastname as name.  
    * For example: "BobRoberts", "BobRoss" and "BobLoblaw" are all unique.
* Singles should have their name in the first column and "None" or blank in the second column.

Here is an example of acceptable .csv content:
```
Name,Spouse
Matt,Megan
Brian,Cameron
Jillian,Shawn
BobRoberts,Isobel
BobRoss,None
BobLoblaw,
```

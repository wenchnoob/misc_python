from solveTSP import *
def main():
    uscities = { 
        "Oklahoma City": (392.8, 356.4), 
        "Montgomery": (559.6, 404.8), 
        "Saint Paul": (451.6, 186.0), 
        "Trenton": (698.8, 239.6), 
        "Salt Lake City": (204.0, 243.2), 
        "Columbus": (590.8, 263.2), 
        "Austin": (389.2, 448.4), 
        "Phoenix": (179.6, 371.2), 
        "Hartford": (719.6, 205.2), 
        "Baton Rouge": (489.6, 442.0), 
        "Salem": (80.0, 139.2), 
        "Little Rock": (469.2, 367.2), 
        "Richmond": (673.2, 293.6), 
        "Jackson": (501.6, 409.6), 
        "Des Moines": (447.6, 246.0), 
        "Lansing": (563.6, 216.4), 
        "Denver": (293.6, 274.0), 
        "Boise": (159.6, 182.8), 
        "Raleigh": (662.0, 328.8), 
        "Atlanta": (585.6, 376.8), 
        "Madison": (500.8, 217.6), 
        "Indianapolis": (548.0, 272.8), 
        "Nashville": (546.4, 336.8), 
        "Columbia": (632.4, 364.8), 
        "Providence": (735.2, 201.2), 
        "Boston": (738.4, 190.8), 
        "Tallahassee": (594.8, 434.8), 
        "Sacramento": (68.4, 254.0), 
        "Albany": (702.0, 193.6), 
        "Harrisburg": (670.8, 244.0) 
    }
    # the default size of the colony is 10 - alter the size to see what happens
    acs = TSPUsingACO(colony_size=100, steps=100, cities=uscities)
    acs.run()
    acs.plot()
main()
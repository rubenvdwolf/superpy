# SuperPy Report

This assignment was daunting at first, but while finding out how certain required modules work, I gained more confidence in coding, and even got to the point where I felt at ease. After handing it in I had some 'revelations' for using classes (which I had not yet used in the first version), so I rewrote the code. Also, I combined several functions in the second version to make the code cleaner and shorter.

The three elements that I find notable in my implementation:

1. Using 'try' and 'except' to be able to differentiate between different types of dates. For instance, I use this in the function for calculating the revenue in a certain day or month. By trying to run the code when a day is entered, it will run the code if it is a day, but if a month is entered, then it will give a ValueError. It then will try to run the code for when a month is entered. If that gives a ValueError, then the user has entered neither a day nor a month, and that will be returned.
2. Using a separate funtion for returning a table. This is not a funtion run directly in main.py, but is used when a different funtion is run, that requires a table to be returned. This saved me a lot of coding.
3. Using a class for the date makes the code a lot cleaner. I decided to add the functions for getting today's and yesterday's dates and advancing the time. 
4. One extra, I personally found it to be a handy idea to handle the expired products at the same time as the time is advanced. In normal life this would also be the case, as a day goes by, a product with that expiration date will expire. I could have put the expired products in a separate file, but for now, putting them in the sold file keeps my code simple and working well.

I realize that I can probably make the code a bit cleaner by putting certain parts of code that I use often into a separate function, but for now that might take a bit too much time for an assignment like this. 
All in all, I enjoyed the assignment.
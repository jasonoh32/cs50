For the design of our final project, my partner and I wanted to create an interactive website that would output a personalized meal plan for the user. Achieving this required a series of functions to do the following: manipulate food items and their respective serving size, consolidate cumulative totals of nutritional facts, and provide a table that displayed the HUDS menu items. Our data was derived from API array data tables provided by HUDS.

Because the meal plan was the mantlepiece of our website, my partner and I decided to have it presented proudly as our homepage. Links to other pages that accomplished the various functions mentioned earlier were listed at the top of the header to provide convenient access to other aspects of our website.

Before diving deeper into our code, we thought it would be necessary to explain the username system in place. Given that users’ meal plans are often personal, we found it imperative to establish a protection system that kept our users’ information private. To accomplish this, we dedicated three html pages to achieve this goal: a register html page to allow the user to create an account within our website, a log-in html page to allow the user to log into our website, and a change-password html page to allow the user to change his or her password. The user’s unique username and hashed password are stored into a project.db database table called “users” and referenced whenever a user attempts to log in.

From there, my partner and I thought hard about how the user would be able to freely manipulate their meal plan. We decided to create html pages that would allow the user to input a unique food ID alongside a serving size to either add or subtract food items from the user’s meal plan. Our programming would call upon the API data and output the inputted food’s nutritional facts onto the meal plan html page. However, we still had to total the values of each nutritional fact to create a proper meal plan report. In our code, we initialized variables that select sums of the nutritional facts and rendered them into our html page.
But still, how would the user be able to implement food IDs if he or she did not know them beforehand? To resolve this, my partner and I created a library of information that stored all of the HUDS food item IDs into tables. The first table presented is a consolidated list of all the food items HUDS serves throughout the year; the user is able to search through this library and find specific food items to add onto their meal plan. However, this list is very extensive. To make information more accessible and convenient to the user, we added the breakfast, lunch, and dinner menus of the current day into our menus page. By doing so, the user would have access to food he or she will eat very soon, thus allowing him or herself the ability to plan for a meal the day of. Libraries of daily updated menus and the entire HUDS menu were consolidated and presented for the user to search for food IDS and input them into their meal plan.a

Stylistically, we borrowed useful components from Week 8’s problem set, otherwise known as the finance problem set, to make a more aesthetically pleasing website. Given both my and my partner’s lack of coding experience, we felt it necessary to dedicate more time and energy into researching how to manipulate API data and produce functioning code rather than worry about stylistic components of our website. However, we were able to make contributions to the website’s template, such as changing the background color and adding tables to different html pages.
Clone repo, run the follwing once in ./ 
### `npm install`

Run the following in ./src/assets 
### `python server.py`

Run the following in ./
### `npm start`

### Description

NOTE: All JSON files as well as images are fetched from the file server.

index.js - Holds the root component for React.

App.js - The Home screen of React App. Consists of two child divs. The first div creates a fixed header to display the page name, and the second div renders Home.js 

Home.js - The homepage. Displays multiple groups(Men, Women) of categories (Shirts, Jeans etc.). Each group of categories is a React Component described by CategoryGrid.js

CategoryGrid.js - Displays a bar with the name of the group. Also displays a grid of categories with each card described by Category.js . Contains a dictionary of categories for each group, which can be modified to add a new vertical. 

Category.js - Displays a card with the image linking to the CardListTrending.js component, along with the name of the category. 

CardListTrending.js, CardListUpcoming.js - This component takes the group and the category name as its state. It then fetches the appropriate JSON from the server and displays the list of the various upcoming/trending products. Each product is described by Card.js . Also displays two links in the header to switch between Upcoming and Trending products

Card.js - Displays an image of the product along with its name. The image here hyperlinks to the product page.


### Adding a new group
 To add a new group, firstly a div enclosing a CategoryGrid component must be added to home.js 
  Further, the key-value pair of group name as key and the list of categories as value must be added to the dictionary in CategoryGrid.js
  Further, all JSONs and images must be available via the file server at the correct location.

### Adding a new category
 To add a new category, the name of the new category must be added to list of the group in the dictionary of CategoryGrid.js
  Further, all JSONs and images must be available via the file server at the correct location.

## SI507_final.py(requires BeautifulSoup, requests, json and time packages)

### Data Source
The data source is 'https://www.lego.com'. There are two hierarchies in my source data. The first hierarchy is the page for all products, the second one is
the detail page of one product, and its url is scraped by the first hierarchy request. 

### load_cache, save_cache and make_url_request_using_cache 
are three functions for loading the cache file, saving the cache file and doing the first step of web scraping by calling the request.get()
The first two functions quote open, file read and write, and json.load and dump. 
The last function will help determine whether the URL I try to request is in the cache file or not. 
The value of dictionary stores the response.text of key's URL, and would be popped up for the further processing if the requested URL is in the dictionary. 
And the response.text would be stored if there is no key related to the requested URL for improving the time complexity of next time web scraping.

### main function
After generating the URL for each age range based on the rules and assigning the URL to each age range in the web_page dictionary, 
calling the make_url_request_using_cache for requesting the URL and searching the cache file before adopting the BeautifulSoup find and findall to further 
scrape the URL contents. The first hierarchy web scraping gives me the each product's lego_url, lego_name, lego_rating, lego_price. And based on lego url, 
the second hierarchy web scraping dig out more details of product, like the amount of pieces, the inventory status to diversify the filters that I would use
for the interactive function design. 

Finally, the result dictionary will store a dictionary like this
{'URL':lego_url, 'Name':lego_name.text, 'Rating':lego_rating_revised, 'Price':lego_price_revised, 'Status': status_revised, 'Pieces':amount_pieces_revised}
in the value under the corresponding age_range key. For saving the time of web scraping every time, I choose to save the result dictionary into the cache JSON,
which can be easily opened for the next time use. [NOTICE]: The cache file should be updated every hour for the business use or real practice. 
Or the other two python files could be linked together for the execution integration and real time reflection. 

## Tree.py(requires json, copy and tabulate packages)

### Tree Design
Simple_tree Example:
('Are you looking for the products designed for the 1.5+ years old?',(lego_cache['age-4-plus-years'], None, None), (lego_cache['age-1-plus-years'], None, None))
Question/internal node consist of tuples of three things(A question to ask, what to do if the answer for question is 'yes', what to do if the answer for question is 'no')
Answer/Leaf also consist of a 3-tuple,(Answer, None, None)
Thus, the tree here is mainly for doing the age range filter and feedback the corresponding answer.

### notAnswer, isAnswer, yes, playAnswer, play_age_tree, loadTree and saveTree
All of them are designed on solving the tree problems. Except for the play_age_tree, the other functions are quite straightforward. 
play_age_tree algorithm steps:
1. identifying whether the tree is internal node or leaf.
2. asking the yes or no towards the internal node or question 
3. if yes, return the corresponding answer
4. if no, ask the next question until yes is prompted.

### expectation_rating, expectation_price, expectation_pieces, expectation_status(Interactive)
All of them are prompted functions for getting the user's expected values.

### filter_out(Interactive)
By comparing the objective's values to expected values to narrow the product options and filter out the suitable toys for user needs.

### tabulate_list(Visualization)
The visualization of filtered product information. Firstly, show the user a table including all the suitable toys' name, rating, price, inventory status and amount of pieces
After showing this table, a prompt would ask users that would they like to see the URL, name and price of each product. And user could directly buy toys through thr URL.

### main
For linking all the above functions, and coping with the error reports.

## visulization.py(requires pandas, numpy, seaborn, matplotlib and json packages)
### Exploring the Lego products 
1. Using pd.concat to concatenate six dataframe into one. 
2. sns.relplot is for seeing the relationship between pieces and price, the hue = Age_range would classify the scatter into different colors. 
That would be helpful to identify the extra clues, like the pieces and prices of each age range.
3. sns.jointplot(kde) is a great tool to check the central tendency of data points, and moreover, the distribution of pieces and price also be reflected by jointplot.
4. bar chart helps get the proportion of products designed for each age range. Obviously, 6+ and 9+ are the main customer segmentation of Lego group.
5. pairplot is a comprehensive visualizing tool for getting several plots in a big graph. It is a great tool for detecting the negligible relationship between each variable.
For instance, 1) the expensive toys are mainly distributed in 6+, 9+ and 18+; 2) Some toys' price are not that high even though they have many pieces. 
Guess: piece of such toys is smaller than regular size and saves more costs of manufacturing them. And some toys are expensive even though they have less pieces. 
Guess: Limited edition or the bigger sized pieces.




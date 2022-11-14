# Python-Project: Library system


## Genral Overview of the project 

The task of this python project was to create a simple library management system for a librarian. This program should have enabled the librarian to:
1.	Search for books by its title
2.	Check out available books
3.	Return books borrowed and flag up overdue books returned
4.	Recommend books for new or current members

## Search for a book
• To search for a book just type into the textbox on the search tab

• You can either do a search by the book’s id or the book name

• As you type book name or id results that match or are a close match to what you type will be displayed in the tree view

• The tree view will show all the details of the books

• If a book is overdue then it will show the book details in a red colour (This feature works as you have seen before) by running it on python 3.10, otherwise it will not show the books that are overdue in red
(or will show the book is overdue via the last coloumn)


## Check out a book:
• Simply type in the book id of the book that you want to check out

• And type in a member id(must have a length of 4 characters)

• After you click on the Check book out button if the member has any books overdue (on loan for more than 60 days)  then it will show the books in the tree view bellow in a red (or in black if its not on python 3.10) colour

## Return a book:
• To return a book click on 1 or multiple records from the tree view and press the return button 

• If you are returning multiple books hold down the left Ctrl button and click on the rows you would like to select and therefore return 

• You can also filter through the books that you want to return by typing  the member id or a book id into the search box 

• If a book that was returned is overdue  then it will be shown in the list box 

## Recommend a book:
• Type in a member id that is either in the database system or not

• A graph will then be displayed showing books that are recommended for that member 

• Book names are on the y axis and the rating of popularity  for the books is on the x axis (horizontal bar graph)

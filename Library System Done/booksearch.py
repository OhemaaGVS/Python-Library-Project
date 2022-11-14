"""This module contains a function used to search for books in the library system
   It then returns values to the Menu.py. Done by F122571"""
from database import *# importing the functions from the Database.py so that it can be accessed by this module


def Search_For_Book(Book,ListOfBooksFound,ListOfBookIDOverdue):
    """This Function calls the function in the Database.py that searches for a book

        Book= this is the book name or ID entered by the librarian (string)
        ListOfBooksFound= an empty list that will be populated with the books that have been found (list)
        ListOfBookIDOverdue= this is an empty list that will contain the Book ID's of the books that are overdue
        This function calls the function in the Database.py that searches for books
        which then returns those books and which ones are overdue."""
    SearchedBooks=Search_Book(Book,ListOfBooksFound,ListOfBookIDOverdue)# calling the function that searches for the books
    return SearchedBooks


#***************************TESTING FUNCTIONS*********************************************#
def Test_Search_For_Book():
    """Testing the Search For Book Function"""
    # should display all the books that have ro in the book name
    print("******Testing Search For Books where books name contains 'cy'******")
    Test=Search_For_Book("cy", ListOfBooksFound=[], ListOfBookIDOverdue=[])
    print(Test)
    print("******Testing Search For Books where books name contains 'KED'******")
    # should display all the books that have DE in the book name
    Test = Search_For_Book("KED", ListOfBooksFound=[], ListOfBookIDOverdue=[])
    print(Test)
    print("******Testing Search For Books where book id contains '1'******")
    # should display all the books that have 1 in the book name
    Test = Search_For_Book("1", ListOfBooksFound=[], ListOfBookIDOverdue=[])
    print(Test)
    print("******Testing Search For Books where book id contains '5'******")
    # should display all the books that have 1 in the book name
    Test = Search_For_Book("5", ListOfBooksFound=[], ListOfBookIDOverdue=[])
    print(Test)


#***************************CALLING TESTING FUNCTIONS*********************************************#
if __name__=="__main__":
    # calling the testing functions for all the functions in this module
    Test_Search_For_Book()




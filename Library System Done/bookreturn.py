"""This module contains functions used to return a book in the library system
   It then returns values to the Menu.py. Done by F122571"""
from database import *#importing all functions from the Database.py module


def Return_Book(BookIDs):
    """This function calls the functions used in the process of returning books

        BookIDs = this is the list of Book  ID's that have been selected by the librarian (list)
        This function calls the function that updates the database and updates the logfile
        file when the book has been returned."""
    Update_Database_After_Returned_Book(BookIDs)#calling the function that updates the database
    ReturnDate=date.today()# storing the current date (todays date)
    OverdueBooksToDisplay=Write_Return_To_Transaction(BookIDs,ReturnDate)# calling the function that writes the transaction to the logfile
    return OverdueBooksToDisplay# this returns all the books that were on loan for more than 60 days so it can be displayed


def Retrive_List_Of_Returnable_Books(ReturnableBookList):
    """This function calls the function that returns the list of books that have not been returned yet

            ReturnableBookList = this is an empty list that will contain the books that need to be returned (list)
            This function calls the function that updates the database and updates the logfile
            file when the book has been returned."""
    ReturnableBooks=Retrieve_Non_Returned_Books(ReturnableBookList)# obtaining the books that need to be returned from the function in Database.py
    return ReturnableBooks# this returns the books that have not been returned



def  Filtered_Books(Indetifier,FilteredBooksList):
    """This function calls the function that retrieves all the non returned books that have a match to the identifiers entered

              Identifier= this is the member id or book id entered by the librarian (string)
              FilteredBookList = the list that will contain the books that match or nearly match the identifiers entered (list)."""
    Books=Find_Matching_Returnable_Books(Indetifier,FilteredBooksList)# calling the funvtion that returns matching or similar book records
    return Books


#***************************TESTING FUNCTIONS*********************************************#
def Test_Retrive_List_Of_Returnable_Books():
    """This function tests the Retrive List Of Returnable Books function"""
   # this should return a list of book details that are needed to be returned
    # the last value of the records in the list should be N/A
    print("******Testing the Retrive List Of Returnable Books function******")
    Test=Retrive_List_Of_Returnable_Books(ReturnableBookList=[])
    print(Test)


def  Test_Filtered_Books():
    """This function tests the Filtered Books function."""
    print("******Testing Filtered Books function******")
    print("******Printing all books that have ja in the member id******")
    Test=Filtered_Books("ja",FilteredBooksList=[])
    # finding all the books that need to returned that have the ez in the member id
    print(Test)
    print("******Printing all books that have 1 in the book id******")
    Test=Filtered_Books("1",FilteredBooksList=[])
    # finding all the books that need to returned that have 1 in the book id
    print(Test)


def Test_Return_Book():
    """This function tests the Return Book function."""
    print("******Testing Return Book function******")
    # after testing this function please press ctrl z on the log file
    # and the database file to reverse the affects before using the system
    Return_Book("2")
    print("Book returned")


#***************************CALLING TESTING FUNCTIONS*********************************************#
if __name__=="__main__":
    # calling the testing functions for all functions within this module
    Test_Retrive_List_Of_Returnable_Books()
    print("")
    Test_Filtered_Books()
    print("")
    Test_Filtered_Books()
    print("")
    #Test_Return_Book()  this returns the book as a test


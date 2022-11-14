"""This module contains the functions used to check out a book for the member.
   It returns values back to the Menu.py. Done by F122571."""

from database import *# importing the functions from the module Database.py
import re# importing the Regular Expression module

def Validate_Book_ID(BookID):
    """Checks if the Book ID is an integer or not

       BookID = the book id entered by the librarian (string)
       This function checks if the BookID entered by the librarian has a numerical value
       (if it is an integer) if it is not it returns the value False.If has a numerical
       value then the function returns the value False."""
    if BookID.isnumeric() == False:#checks if the BookID is a numerical value or not
        return False
    else:
        return True

def Validate_Member_ID(MemberID):
    """Checks if the MemberID contains any digits and if its a length of 4

       MemberID = the member id entered by the librarian (string)
       This function checks if the MemberID entered by the librarian has any digits
       and if it has a length not equal to 4 characters.If it does have digits or
       the length of the MemberID is not equal to 4 then it returns False. Else it returns True."""
    if re.search("[0-9]",MemberID) or len(MemberID)!=4:# checks if the member id contains didgets and if its length is equal to 4
        return False
    else:
        return True


def  Check_Out_Book(BookID,MemberID):
    """This function calls functions within the Database.py that carries out the procedure of checking out a book

       BookID = the book id entered by the librarian that has been validated (string)
       MemberID= the member id entered by the librarian that has been validated (string)
       Stores the current date
       This function calls the :
       Function that updates the database after the check out has been made
       Function that obtains the genre that corresponds to the book id entered by the librarian
       Function that writes the check out transaction to the logfile."""

    Update_Database_After_Check_Out(BookID,MemberID)# this calls the function that updates the database after the check out has been made
    CheckOutDate=date.today()# this variable contains the current (todays) date
    Genre=Get_Book_Genre(BookID)# this variable contains the genre of the book that is being checked out, once it calls the function that selects the book of the genre
    BookName=Get_Book_Name_By_ID(BookID)
    Write_Transaction_To_File(BookID,CheckOutDate,MemberID,Genre,BookName) #calling the function that writes the book check out transaction to the logfile


def  Check_BookID_And_MemberID_Valid(BookID,MemberID):
    """This function checks if the validation of the MemberID and the BookID has been successfully completed

       BookID = the book id entered by the librarian (string)
       MemberID = the member id entered by the librarian (string)
       This function calls the functions that check the validity of the BookID and MemberID
       respectively. It then stores the returned values of those functions
       If the variables are both true then it will return True."""
    ValidMemberID=Validate_Member_ID(MemberID)
    ValidBookID=Validate_Book_ID(BookID)
    #storing the returned values of the validations
    if ValidBookID==True and ValidMemberID ==True:# checking if both values are true
        return True
    else:
        return False# wasnt there


def Check_Out_Book_Location(BookID):
   """This function calls the fuction in Database.py that checks if the BookID entered is a ligitiment ID in the database system

      BookID = the book id entered by the librarian (string)
      This function calls the function that checks if the book id is in the database
      It then stores the returned value in a variable and returns the value."""
   Located= Locate_Book_By_ID(BookID)#storing the results of the function, passes the BookID into the function
   return Located


def Check_Out_Books_Availability(BookID):
    """This function calls the function in Database.py that checks if a book is available for check out

       BookID = book id entered by the librarian (string)
       This function calls the function that checks the book availability that the member wants to check out
       It stores the returned value in a variable."""
    BookAvailable=Check_Book_Availability(BookID)#passing the parameter BookID into the function
    return BookAvailable


def   Check_Out_Book_Validate_Inputs(BookID,MemberID):
    """This function calls the function that validates the Member ID and the Book ID

           BookID = the book id entered by the librarian (string)
           MemberID = the member id entered by the librarian (string)."""
    ValidInputs=Check_BookID_And_MemberID_Valid(BookID, MemberID)# passing in the MemberID and BookID as a parameter in the function
    return ValidInputs#returning the value back to Menu.py


def Check_Member_Books_Overdue(MemberID,ListMemberBooks,ListMemberBooksOverdue):
    """This function calls the function in Database.py that returns the books that the member has for longer than 60 days

           MemberID = the member id entered by the librarian (string)
           ListMemberBooks = will contain the list of books that the member has (list)
           ListMemberBooksOverdue = will contain the list of books that are overdue that the member has (list)."""
    MemberBooks=Check_Database_For_Member_Books(MemberID,ListMemberBooks,ListMemberBooksOverdue)
    return MemberBooks
    #calling a function and passing the parameters MemberID,ListMemberBooks and ListMemberBooksOverdue


#***************************TESTING FUNCTIONS*********************************************#

def Test_Validate_Book_ID():
    """This function tests the Validate Book ID function."""
    print("******Testing Test For Validate Book ID******")
    Test=Validate_Book_ID("23")# this is a valid
    if Test == True:
        print("Book ID is valid")
    else:
        print("Book ID is not valid")

    Test=Validate_Book_ID("aa")
    if Test==True:
     print("Book ID is valid")
    else:
        print("Book ID is not valid")


def Test_Validate_Member_ID():
    """This function tests the Validate Member ID function."""
    print("******Testing Test For Validate Member ID******")
    Test = Validate_Member_ID("23jaze")# not a valid member ID so test = false
    if Test == True:
      print("Valid Member ID")
    else:
        print("Member ID is not valid, needs four characters and no digits")
    Test = Validate_Member_ID("javas")# not a valid member ID so test = false
    if Test==True:
     print("Valid Member ID")
    else:
        print("Member ID is not valid, needs four characters and no digits")
    Test = Validate_Member_ID("caio")# this is a valid member id so test = true
    if Test==True:
     print("Member ID is valid")
    else:
        print("Member ID is not valid, needs four characters and no digits")



def Test_Check_BookID_And_MemberID_Valid():
    """This function tests the Check Book And Member ID Valid function."""
    print("******Testing Check BookID and MemberID function******")
    Test =Check_BookID_And_MemberID_Valid("aa","aaaa")# book id is not valid therfore test = false
    if Test==True:
     print("Member ID and Book ID is valid")
    else:
        print("Member ID and Book ID is not valid MemberID should be 4 characters and Book id should be an integer")

    Test = Check_BookID_And_MemberID_Valid("23", "aaaaa")# member id is not valid therefore test = false
    if Test == True:
        print("Member ID and Book ID is valid")
    else:
        print("Member ID and Book ID is not valid MemberID should be 4 characters and Book id should be an integer")

    Test = Check_BookID_And_MemberID_Valid("23", "caoi")# book id and member id is valid therefore test = true
    if Test == True:
        print("Member ID and Book ID is valid")
    else:
        print("Member ID and Book ID is not valid MemberID should be 4 characters and Book id should be an integer")


def Test_Check_Out_Book_Location():
    """This function tests the Check Out Book Location function."""
    print("******Testing Check Out Book Location function******")
    Test = Check_Out_Book_Location("500")# this book id is not in the database->test=false
    if Test==True:
        # if the book is in the data base it will output this
        print("Book has been located")
    else:
        # if the book is not in the database then it will output this
        print("Book not in library")
    Test = Check_Out_Book_Location("abc")# abc is not in the database -> test=false
    if Test==True:
        print("Book has been located")
    else:
        print("Book not in the library")
    Test = Check_Out_Book_Location("12")# 12 is in the database so test will be true
    if Test==True:
        print("Book has been located")
    else:
        print("Book not in library")


def Test_Check_Out_Books_Availability():
    """This function tests the Check Out Book Availability function."""
    print("******Testing Check Out Book Availability function******")
    Test = Check_Out_Books_Availability("1")# this is available in the database
    if Test == True:
        # if the book is available it should output this
        print("Book is available")
    else:
        #otherwise it should output this
        print("Book is not available")
    Test = Check_Out_Books_Availability("2")# this is not available in the database
    if Test == True:
        print("Book is available")
    else:
        print("Book is not available")


def Test_Check_Out_Book_Validate_Inputs():
    """This function tests the Check Out Book Validate Inputs function."""
    print("******Testing Check Out Book Validate Inputs function******")
    Test = Check_Out_Book_Validate_Inputs("book id","caoi")# book id is not valid
    if Test == True:
        # if both of the inputs match the criteria the output this
        print("Both inputs are valid")
    else:
        # otherwise output this message
        print("Both inputs not valid")
    Test = Check_Out_Book_Validate_Inputs("1", "abcde")# member id is not valid
    if Test == True:
        print("Both inputs are valid")
    else:
        print("Both inputs not valid")
    Test = Check_Out_Book_Validate_Inputs("1", "true")# both inputs are valid
    if Test == True:
        print("Both inputs are valid")
    else:
        print("Both inputs not valid")

def Test_Check_Member_Books_Overdue():
    """This function tests the Check Member Books Overdue function ."""
    print("******Testing Check Member Books Overdue function******")
    Books=Check_Member_Books_Overdue("razz",ListMemberBooks=[],ListMemberBooksOverdue=[])# razz has overdue books
    if len(Books)>0:
        # if the member has books that are overdue the it will output this
        print("These are the books the member has overdue")
        print(Books)
    Books = Check_Member_Books_Overdue("aaaa", ListMemberBooks=[], ListMemberBooksOverdue=[])# aaaa has no overdue books
    # if the member has no books overdue it will output this
    if len(Books)==0:
        print("This member has no books overdue")



def Test_Check_Out_Book():
    """This function tests the Check out Book function."""
    print("******Testing Check Out Book function ******")
   # after you have ran this test press control z on the database and logfile as it
    # alters the content
    Check_Out_Book("157", "test")# this is a valid book id and member id
    print("Book checked out")


#***************************CALLING TESTING FUNCTIONS*********************************************#
if __name__=="__main__":
    # calling the testing functions for all functions within this module
    Test_Validate_Book_ID()
    print("")
    Test_Validate_Member_ID()
    print("")
    Test_Check_BookID_And_MemberID_Valid()
    print("")
    Test_Check_Out_Book_Location()
    print("")
    Test_Check_Out_Books_Availability()
    print("")
    Test_Check_Out_Book_Validate_Inputs()
    print("")
    Test_Check_Member_Books_Overdue()
    #Test_Check_Out_Book() this checks out a book



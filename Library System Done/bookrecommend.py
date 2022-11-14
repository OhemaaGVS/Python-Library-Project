"""This module contains the function used to recommend books for the member entered.
   It returns values back to the Menu.py. Done by F122571"""

from database import *# importing the Database.py functions so that it can be accessed
def Recommend_Book_For_Member(MemberID):
    """This Function calls the function in the Database.py that recommends the book for members
        It then returns the recommended books to the Menu.py so that it can be displayed

        MemberID = the member id entered by the librarian (string)
        This function calls the function in the Database.py
        that is used to recommend the books for a member."""
    MemberGenres=[]#creating an empty list
    RecommendedBooks=GetMemberGenres(MemberID,MemberGenres)#calling the function GetMemberGenres in the Database.py
    return RecommendedBooks# returning the value that was obtained by running the function to the Menu.py


#***************************TESTING FUNCTIONS*********************************************#
def Test_Recommend_Book_For_Member():
    """This function tests the Recommend Book For Member function."""
    print("******Testing Recommend Book For Member function******")
    print("**Recommendation for member id in the database**")
    Test = Recommend_Book_For_Member("java")  # member who is in the database
    # should return a list of books recommend for this member based on the genre of books they haveread from
    # it should not recommend the books they have already read
    # first list is the books
    # second list is the ratings
    print(Test)
    print("**Recommendation for member id not in the database**")
    Test = Recommend_Book_For_Member("test")  # a member who is not in the database
    # should return a list of books recommend for this member who is not in the database
    # so its based of what genre is the most popular
    # first list is the books
    #second list is the ratings
    print(Test)


#***************************CALLING TESTING FUNCTIONS*********************************************#
if __name__=="__main__":
    # calling the testing functions for all functions within this module
    Test_Recommend_Book_For_Member()


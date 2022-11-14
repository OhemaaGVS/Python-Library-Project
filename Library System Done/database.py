"""This module is responsible with interacting directly with the Logfile and the Database file
   This module contains functions used to read, write and append to the logfile and database file
   where necessary Done by F122571."""

import random#importing random so it can be used in the module
from datetime import date# importing the date from the date time module so it can be accessed in this module

def CalculateBookPopularity(ListofBooks,Genres):
    """This function calculates the probability of the books

       Genres= the dictionary that contains the genres and which ones have books been taken out the most by the member (dictionary)
       ListofBooks = the list of books that have been recommended (list)
       This function calculates the the popularity of the book using a random number generator. The genre that has the most books
        that have been checked out is assigned a higher rating then the genres that have the least books issued
        this function is used by two other functions."""
    RecomendedBooks = []# this will contain the list of recommended books with its ratings
    max = 0# setting max to 0 so that any number greater than it will be stored
    min = 1000# setting min to 1000 so any number less than it will replace it and be stored
    for Genre in Genres:# for each genre in the dictionary of genres
        if Genres[Genre] > max:# if the number of books in that genre is greater than the current max value
            max = Genres[Genre ]# the new max value is equal to the number of books within that genre
        if Genres[Genre ] < min:# if the number of books in that genre is less than the current min value
            min = Genres[Genre ]# then the new min value is the genre that has the smallest amount of books
        for Books in ListofBooks:# for each of the books in the book list
            word = Books.split(",")
            if Genre  in word:
                if Genres[Genre] == max:# if the number of books in this genre is the highest
                    RecomendedBooks.append(str(Books) + "," + str(random.randint(90, 100)))# assign the books a rating of 90 to 100 and add it to the list
                elif Genres[Genre ] == min:# if the number of books in the genre is the least amount
                    RecomendedBooks.append(str(Books) + "," + str(random.randint(20, 40)))# assign the books a rating of 20-40 and add it to the list
                else:
                    RecomendedBooks.append(str(Books) + "," + str(random.randint(55, 75)))# otherwise assign the books a rating between 55 to 75
    BookNames=[]
    BookPopularity=[]
    # creating the empty lists that will contain the values of the x axis and the y axis of the graph of recommended books
    for Books in RecomendedBooks:# for each of the books in the recommended books list
        word = Books.split(",")
        BookNames.append(word[1])# adding the name of the book to the book names list
        BookPopularity.append(int(word[2]))# adding the rating of the book to the book popularity list
    ReturnGraphDetails = (BookNames, BookPopularity)
    return ReturnGraphDetails# returning the results so it can be used to plot the graph


def FindRecomendedBooks(Genres,AlreadyRead):
    """This function selects the books that are under the genres that the member has issued books from

         Genres= the dictionary that contains the genres and which ones have books been taken out the most by the member (dictionary)
         AlreadyRead= this is a list that contains all the books the member has read (list)
         This function stores the books that are in the preferred genre by the member if they are in the logfile and that have not been read by the member
         so it does not recommend already read books to the members."""
    ListofBooks=[]# this will contain the list of books that are being recommended
    with open("database.txt","r") as Reader:
            for line in Reader:
                for Genre in Genres:# for all the genres in the genres dictionary
                     word=line.split(",")
                     if Genre==word[1] and word[2] not in AlreadyRead:# if the genre in the database is equal to the genre in the dictionaries
                         # and if the book is not in the list of books that the member has already read
                                    if len(ListofBooks)==0:# if the list  is empty
                                        ListofBooks.append(word[1]+","+word[2])#add the genre and the book name to the list
                                    else:
                                            if word[1]+","+word[2] not in  ListofBooks and len( ListofBooks)<10:
                                                ListofBooks.append(word[1] + "," + word[2])
                            # if  the book is not already in the list and there is not 10 books in the list of reccomended books
                            # add the book to the list
    RecommededBooks=CalculateBookPopularity(ListofBooks,Genres)# call the function that determines how popular the books are
    Reader.close()# closing the reader
    return RecommededBooks


def Popular_Books(Genres):
        """This function selects the books that are under the genres

        Genres= the dictionary that contains the genres and which ones have books been taken out the most (dictionary)
        This function stores books that are under the most popular genre. This does the recommendations for members who
        are not in the logfile or those who have read less than 3 books in the logfile."""
        ListofBooks = []# this will contain the list of books
        with open("database.txt", "r") as Reader:
            for line in Reader:
                for Genre in Genres:# for all the genres in the genre dictionary
                    word = line.split(",")
                    if Genre == word[1]:# if the genre is equal to the genre in the database
                        if len(ListofBooks) == 0:# if the list is empty
                            ListofBooks.append(word[1] + "," + word[2])# add the genre and the book name to the list
                        else:
                            if word[1] + "," + word[2] not in ListofBooks and len(ListofBooks) < 10:
                                # if the book name and genre is not in the list already, and there is less than 10 books in the list
                                ListofBooks.append(word[1] + "," + word[2])# add the name and the genre of the book to the file
        PopularBooks=CalculateBookPopularity(ListofBooks, Genres)#calling the function with the listofbooks and genres as parameters
        Reader.close()
        return PopularBooks# returning the popular books



def Select_Popular_Genres():
    """This function determines the most popular genre

        This function finds the genres that are most popular by counting how many times it occurs and puts it into a dictionary."""
    PopularGenre = []# list that will contain
    with open("logfile.txt", "r") as Reader:
        for line in Reader:
            word = line.split(",")
            if word[5] == "N/A\n":# if the returndate is at the default value of N/A
                PopularGenre.append(word[2])# adding the genre to the list
    Genres = {i: PopularGenre.count(i) for i in PopularGenre}# using a dictionary to count how many times the genre occurs
    RecomendedBooks=Popular_Books(Genres)# calling the recommendation function
    Reader.close()
    return RecomendedBooks# returning the values



def GetMemberGenres(MemberID,MemberGenres):
    """This function finds the popular genres that the member has read

          MemberID= this is the member id entered by the user (string)
          Member Genres = is a list that will contain the genres that the member has read a book from (list)
          This function finds the genres that the user has read and then determines which ones are the most popular by putting
          it into a dictionary."""
    AlreadyRead = []# this contains the books that the member has already read
    with open("logfile.txt", "r") as Reader:
        for line in Reader:
            word = line.split(",")
            if MemberID == word[1]:# of the member id is equal to the one in the logfile
                MemberGenres.append(word[2])# add the genre to the list of genres
                AlreadyRead.append(word[3])# add the name of the book to the list of books the member has read
    Genres = {Genre: MemberGenres.count(Genre) for Genre in  MemberGenres}
    # creating a dictionary that contains the genre and how many times the member has had a book that belongs to that genre
    Reader.close()
    if len(MemberGenres) <3:# if there is less than 3 genres in the member genre list
        Reccomendation=Select_Popular_Genres()# recomend the most popular books instead
        return Reccomendation
    else:
        Recomendation = FindRecomendedBooks(Genres,AlreadyRead)# call the function that recomends book based on the genre
        return Recomendation


def Calculate_Dates(CheckOut):
    """This function calculates how many days there are between a return date and the check out date

      CheckOut = the date that the book was checked out (string)
      This function calculates the difference between the check out date and the return
      date of a book
      This function is being used by multiple other functions."""
    CheckOutDates = CheckOut.split("-")# spliting the check out dates where there is a hythen
    ReturnDates = date.today()# getting todays date
    ActualCheckOutDate = date(int(CheckOutDates[0]), int(CheckOutDates[1]), int(CheckOutDates[2]))#converting the check out date to a date rather than a string so it can be used
    Days = (ReturnDates - ActualCheckOutDate).days# calculating the difference
    return Days


def Retrieve_Non_Returned_Books(ReturnableBookList):
    """This function gets the books that have not been returned

                ReturnableBookList = the list that will contain all the books that are able to be returned (list)
                This function selects all the books that need to be returned from the logfile ."""
    BookFound = False
    with open("logfile.txt", 'r') as Reader:
        for line in Reader:
            word = line.split(",")
            if "N/A\n" == word[5] or "N/A" == word[5]:# if the return date is set to the default value of N/A
                BookFound = True
                ReturnableBookList.append(line)# add the book details into the list
    if BookFound == False:
        print("")
    Reader.close()
    return ReturnableBookList# return the list that contains any books that have not been returned


def Overdue(ListOfBooksID,ListOfBookIDOverdue):
    """This function determines whether books are overdue or not

                   ListOfBooksID= this is the list of ids (list)
                   ListOfBookIDOverdue = this list will contain the book id's that are overdue (list)
                   This function determines if books are overdue and if it is it appends it to the list."""
    with open("logfile.txt","r") as Reader:
           for line in Reader:
               word=line.split(",")
               for ID in ListOfBooksID:# for each of the ID's  in the list
                   if (ID==word[0] and "N/A\n"==word[5]) or(ID==word[0] and "N/A"==word[5]):
                       # if the id is equal to the one in the logdile and there is no return date for that book id
                       CheckOut = word[4]# store the checkout date
                       Days=Calculate_Dates(CheckOut)# calling the function that calculates the difference between the return date and check out date
                       if Days>60:
                          ListOfBookIDOverdue.append(ID)# adding  the id to the list  if the days its overdue by is greter than 60
    Reader.close()#close reader
    return ListOfBookIDOverdue

def Search_Book(Book,ListOfBooksFound,ListOfBookIDOverdue):
    """This function searches for the books in the data base

               Book= this is the id or the book name the user enters (string)
               ListOfBooksFound = a list that will contain all the books that have been found (list)
               ListOfBookIDOverdue = a list that will contain all the ID's of the books that are overdue (list)
               This function searches through the database to find the books that have a close match or match
               the name or the book id entered by the librarian."""
    ListOfBooksID=[]#this list will contain all the ids of  the books found
    BookFound = False
    with open("database.txt", 'r') as Reader:# opening the database file
        for line in Reader:
            word = line.split(",")# splitting each line wup into indervidual strings
            if Book.lower() in word[2].lower() or Book in word[0]:
                # if the name of the book entered is in the book name within the database(lower case version to make it easier to compare)
                # or if the book id entered is in the book id's in the database
                BookFound = True
                ID=word[0]#storing the ID of the Book
                ListOfBooksID.append(ID)# adding the id to the list
                ListOfBooksFound.append(line)# adding the details of the books found into the list
    Overdue(ListOfBooksID,ListOfBookIDOverdue)# calling the function that determines which book are overdue
    Reader.close()# closing the reader
    if BookFound == False:
      pass
    return ListOfBooksFound


def Get_Book_Name_By_ID(BookID):
    """This function gets the book name of the book that is going to be checked out

            BookID = this is the id that the librarian enters (string)
            This function retrieves the name of the book that is going to be checked out
            it does this by checking in the database where the book id is equal to the one entered
            and selects the book name that corresponds to that book id."""
    BookFound = False
    with open("database.txt", 'r') as Reader:
        for line in Reader:
            word = line.split(",")
            if BookID == word[0]:# if the book id matches the book id entered by the librarian
                BookFound = True
                Book=word[2]# storing the title of the book
    if BookFound == False:
        pass
    Reader.close()
    return Book# returning the book name


def Check_Book_Availability(BookID):
    """This function checks if a book is available

               BookID = this is the id that the librarian enters (string)
               This function checks the availability of a book by checking
               if the member id is set to the default value of N/A
               if it is not then it returns false, if it is available then it
               returns true."""
    Available=False# setting the boolean false
    with open("database.txt", 'r',) as Reader:
        for line in Reader:
            word = line.split(",")
            if (BookID == word[0] and word[5]=="N/A") or(BookID == word[0] and word[5]=="N/A\n"):
                # if the book id is the same as the one entered and the member id is set to N/A which is the default value
                Available= True# set boolean to true
                return True# returning true
    if Available==False:
            return False# if it is not available then it will return false
    Reader.close()# closing the reader


def Write_Return_To_Transaction(BookIDs,ReturnDate):
    """This function writes to the logfile when a book has been returned

           BookIDs = this contains the list of book ids selected by the librarian (list)
           Returndate = today's current date (date)
           This function updates the logfile when a book or books have been returned. by writing over
           the old data and adding the return date to the data in the file."""
    reader = open("logfile.txt", "r")
    OverdueBooks = []# empty list that will contain books that are overdue
    files = reader.readlines()
    for ID in BookIDs:# for each of the ID's in the list of Book ID's
        for data in files:
            words = data.split(",")
            if (str(ID) == words[0] and words[5] == "N/A") or (str(ID) == words[0] and words[5] == "N/A\n"):
                # if the book id is the same as the one in the logfile and the return date is currently set to N/A
                CheckOut = words[4]# store the check out date
                Days=Calculate_Dates(CheckOut)#calling the function that calculates if a book is overdue
                DataToUpdate = data
                if Days > 60:
                    OverdueBooks.append("Book ID : %s has been loaned for %d days" % (words[0], Days))# adding the book if its overdue to the list of overdue books
                files.remove(DataToUpdate)
                NewData = DataToUpdate.replace("N/A", ("%s" % (str(ReturnDate))))# adding the return date to that specific file
                files.append(NewData)# adding the new data
    reader.close()
    writer = open("logfile.txt", "w")
    writer.writelines(files)#writing the new data to the file
    writer.close()
    return OverdueBooks#returning the list of overdue books


def Get_Book_Genre(BookID):
    """This function obtains the genre that corresponds to the book id that the librarian had entered

        BookID = this is the book id entered by the librarian (string)
        This function retrieves the genre of the book that corresponds to the book id that was entered
        it then returns the genre of that book."""
    reader = open("database.txt", "r")
    files = reader.readlines()
    for data in files:
        words = data.split(",")
        if BookID == words[0]:# if the book id entered is the same as the one in the database
            Genre = words[1]# storing the genre from the database
            return Genre# returning that genre
    reader.close()


def Write_Transaction_To_File(BookID,CheckOutDate,MemberID,Genre,BookName):
    """This function writes to the logfile when a book has been checked out

            BookID = this is the book id entered by the librarian (string)
            CheckoutDate= is equal to the current date (today's date) (date)
            MemberID= the member id entered by the librarian (string)
            Genre= the genre that the book that is being checked out belongs to (string)
            BookName= the name of the book that is being checked out (string)
            This function updates the logfile when a book has been checked out
            It does this by writing to the logfile the new transaction of the check out."""
    TransactionToLog="%s,%s,%s,%s,%s,N/A\n"%(BookID,MemberID,Genre,BookName,str(CheckOutDate))
    # this variable contains the string of the bookid,memberid,genre,bookname and check out date that is going to be writen into the file
    writer = open("Logfile.txt", "a")# opening the logfile to be appended to
    writer.writelines(TransactionToLog)# appending the transaction log to the logfile
    writer.close()


def  Update_Database_After_Returned_Book(BookIDs):
    """This function updates the database after a book has been returned

        BookIDs = this is the list of book ids that was selected by the librarian (list)
        This function updates the database when a book or multiple books have been returned
        It does this by writing to the database the new data and changes the member id back to its default value N/A."""
    reader = open("database.txt", "r")
    files = reader.readlines()# storing the contents of the database
    for ID in BookIDs:# for each of the ID's that the user selected that have been stored in the list
        for data in files:
            words = data.split(",")
            if str(ID) == words[0]:# if the id selected is the same as the one in the database
                DataToUpdate = data
                files.remove(DataToUpdate)# removing the old data
                NewData = DataToUpdate.replace(words[5], "N/A\n")# changing the member id back to the default value
                files.append(NewData)# adding the new data
        reader.close()# closing the reader
    files.sort()#sorting the file
    writer = open("Database.txt", "w")# opening the database to be written to
    writer.writelines(files)# writing the contents to the database
    writer.close()#closing the file


def  Update_Database_After_Check_Out(BookID,MemberID):
    """This function updates the database after a book has been checked out

            BookID = the book id entered by the librarian (string)
            MemberID = the member id entered by the librarian (string)
            This function updates the database when a check out has been made by
            editing the record in the file that corresponds to the book id
            entered."""
    reader=open("database.txt","r")# opening the file
    files=reader.readlines()
    for data in files:
        words=data.split(",")
        if BookID==words[0]:# checking if the book id entered is equal the book id in the database
            DataToUpdate = data# storing that line of data
            files.remove(DataToUpdate)# removing that data from the file
            NewData = DataToUpdate.replace(words[5],MemberID+"\n")#adding the member id to the file
            files.append(NewData)# adding the new data to the files
    reader.close()
    files.sort(key=lambda x: int(x.split(",")[0]))#sorting the list of the files by its book id
    writer=open("database.txt","w")# opening the database to write to it
    writer.writelines(files)# writiong the new files into the database
    writer.close()# closing the writer


def Locate_Book_By_ID(BookID):
    """This function checks if the book id is actually present in the database system

        BookID = the book id entered by the librarian (string)
        This function reads the data in the database and checks if
        the book id entered is equal to one in the database."""
    BookFound = False
    with open("database.txt", 'r') as Reader:#open the database
        for line in Reader:
            word = line.split(",")#spliting up the lines in the database into words
            if BookID== word[0]:# if the book id entered is equal to the one in the database
                return True# returning true if the book has been found
    if BookFound == False:
       pass
       return False# returning false if the book has not been found
    Reader.close()#closing the reader


def Check_Member_Overdue_Books(MemberID,ListMemberBooksOverdue):
    """This function stores the list of books that are currently overdue by the member that corresponds to the member ID

           MemberID = the member id entered by the librarian (string)
           ListMemberBooksOverdue = this is currently an empty list that will be populated with the books that are overdue
           it populates this by calculating which books have been loaned for over 60 days (list)
           This function reads the data in the logfile where the member id entered is the same as the one in the logfile
           It then calls a function that determines how long the book is overdue."""
    with open("logfile.txt", "r") as Reader:#open the logfile
        for line in Reader:
                word = line.split(",")#splitting up each line in the database into words
                if ((str(MemberID)).strip("") == word[1] and "N/A\n" == word[5]) or ((str(MemberID)).strip("") == word[1] and "N/A" == word[5]):
                    # if the member id entered is in the logfile and the returndate of the book equals N/A
                    CheckOut = word[4]# storing the check out date from the logfile
                    Days=Calculate_Dates(CheckOut)# calling the function that calculates the dates
                    if Days > 60:
                        ListMemberBooksOverdue.append(line)# adding the book details to the list of overdue books
                        # if the days is greater than 60
    Reader.close()# closing the reader
    return  ListMemberBooksOverdue

def Check_Database_For_Member_Books(MemberID,ListMemberBooks,ListMemberBooksOverdue):
    """This function stores the list of books that the member has checked out

       MemberID = the member id entered by the librarian (string)
       ListMemberBooks = this is the list that will be populated with the books that the member has checked out (list)
       ListMemberBooksOverdue = this is currently an empty list that will be populated with the books that are overdue
       it populates it by passing it as a parameter into another function (list)
       This function reads the data in the database file and then adds the contents
       to a list if the member id entered is equal to the member id in the database."""
    with open("database.txt", 'r') as Reader:# opening the database
        for line in Reader:# each row of data in the database file
            word = line.split(",")# spliting the rows into words(spliting it where the commas are)
            if str(MemberID+"\n")== word[5]:#if the member id entered is equal to the one in database
                ListMemberBooks.append(line)# adds the book and its details to the list
    Reader.close()#closing the reader
    OverdueBooks=Check_Member_Overdue_Books(MemberID,ListMemberBooksOverdue)#passing in the parameters of the list that has been populated
    return OverdueBooks
   # and the member id


def Find_Matching_Returnable_Books(Indetifier,FilteredBooksList):
    """This function returns books that are similar or conatin the identifier that was entered

           Identifier = the member id entered or the book id entered by the librarian (string)
           FilteredBookList= this is the list that will be populated with the books that the member has not returned (list)."""
    BookFound = False
    with open("logfile.txt", 'r') as Reader:  # opening the database file
        for line in Reader:
            word = line.split(",")  # splitting each line wup into individual strings
            if (Indetifier.lower() in word[1].lower() or Indetifier in word[0]) and ("N/A\n" == word[5] or "N/A"==word[5] ):
                # if the id of the book entered is in the book id  within the logfile
                #or if the id of the member that is entered is within the logfile(lowercase allows it to be compared easily)
                # and the return date is at the default value of N/A
                BookFound = True
                FilteredBooksList.append(line)  # adding the details of the book to the list
    Reader.close()  # closing the reader
    if BookFound == False:
        pass
    return FilteredBooksList# returning the list


#***************************TESTING FUNCTIONS*********************************************#
def Test_Find_Matching_Returnable_Books():
     """This function tests the Find Matching Returnable Books function."""
     print("******Testing Find Matching Returnable Books function****** ")
     print("******Print all books that have zz in its member id")
     Test=Find_Matching_Returnable_Books("zz",FilteredBooksList=[])
     # should print all the books that have a corresponding member id that has ja in it
     print(Test)
     print("******Print all books that have 3 in its book id")
     Test = Find_Matching_Returnable_Books("3", FilteredBooksList=[])
     # should print all the books that have a corresponding book id that has 23 in it
     print(Test)

def Test_Check_Database_For_Member_Books():
    """This function tests the Check Database For Member Books function"""
    print("******Testing Check Database For Memeber Books function******")
    print("******Print books that member 'chez' has checked out and not returned******")
    Test=Check_Database_For_Member_Books("chez",ListMemberBooks=[],ListMemberBooksOverdue=[])
    # print the list of books that the member razz has checked out
    print(Test)
    print("******Print books that member 'fizz' has checked out and not returned******")
    Test = Check_Database_For_Member_Books("fizz", ListMemberBooks=[], ListMemberBooksOverdue=[])
    # print the list of books that the member fizz has checked out
    print(Test)
    print("******Print books that member 'jace' has checked out and not returned******")
    Test = Check_Database_For_Member_Books("jace", ListMemberBooks=[], ListMemberBooksOverdue=[])
    # print the list of books that the member jace has checked out
    print(Test)

def  Test_Check_Member_Overdue_Books():
    """This function tests the Check Member Overdue Books function"""
    print("******Testing Check Member Overdue Books function******")
    print("******Print books that member 'razz' that are overdue******")
    Test = Check_Member_Overdue_Books("razz", ListMemberBooksOverdue=[])
    print(Test)



def Test_Locate_Book_By_ID():
    """This function tests the Locate Book By ID function"""
    print("******Testing Locate Book By ID  function******")
    print("******Testing Locate Book By ID when the book id does not exist in the database******")
    Test=Locate_Book_By_ID("200")# this book id does not exist so test will equal false
    if Test==True:
      print("Book id in the libary")
    else:
        print("Book id not in libary")
    print("******Testing Locate Book By ID when the book id does exist in the database******")
    Test = Locate_Book_By_ID("7")# this book id does exist so test will equal true
    if Test==True:
      print("Book id in the libary")
    else:
        print("Book not in libary")
def  Test_Get_Book_Genre():
    """This function tests the Get Book Genre function"""
    print("******Testing Get Book Genre function******")
    print("******Testing Get Book Genre when the book id is 34 ******")
    Test = Get_Book_Genre("34") # should show the genre that corresponds to the book id
    print(Test)
    print("******Testing Get Book Genre when the book id is 1 ******")
    Test = Get_Book_Genre("1")  # should show the genre that corresponds to the book id
    print(Test)
def  Test_Check_Book_Availability():
    """This function tests the Check Book Availability function."""
    print("******Testing Check Book Availability function******")
    Test = Check_Book_Availability("1")  # this is available in the database
    if Test == True:
        # if the book is available it should output this
        print("Book is available")
    else:
        # otherwise it should output this
        print("Book is not available")
    Test = Check_Book_Availability("2")  # this is not available in the database
    if Test == True:
        print("Book is available")
    else:
        print("Book is not available")

def Test_Get_Book_Name_By_ID():
    """This function tests the Get Book Name By ID function."""
    print("******Testing Get Book Name By ID function******")
    Test=Get_Book_Name_By_ID("1")# name of the book that has the id of 1 is Cinder
    print("the name of the book is",Test)
    Test = Get_Book_Name_By_ID("56")# name of the book with id 56 is Remote
    print("the name of the book is", Test)

def Test_Search_Book():
    """Testing the Search BookFunction"""
    # should display all the books that have ro in the book name
    print("******Testing Search For Books where books name contains 'ro'******")
    Test = Search_Book("ro", ListOfBooksFound=[], ListOfBookIDOverdue=[])
    print(Test)
    print("******Testing Search For Books where books name contains 'DE'******")
    # should display all the books that have DE in the book name
    Test = Search_Book("DE", ListOfBooksFound=[], ListOfBookIDOverdue=[])
    print(Test)
    print("******Testing Search For Books where book id contains '1'******")
    # should display all the books that have 1 in the book name
    Test = Search_Book("1", ListOfBooksFound=[], ListOfBookIDOverdue=[])
    print(Test)
    print("******Testing Search For Books where book id contains '5'******")
    # should display all the books that have 1 in the book name
    Test = Search_Book("5", ListOfBooksFound=[], ListOfBookIDOverdue=[])
    print(Test)



def Test_Overdue():
 """Testing the Overdue function."""
 print("******Testing the Overdue function******")
 Test=Overdue(ListOfBookIDOverdue=[],ListOfBooksID=["1","6","24","27","19"])
#if there is a book id from the list of book ids that is overdue then output those id's
 print("Book ids that are overdue are",Test)





def  Test_Retrieve_Non_Returned_Books():
    """This function tests the Retrieve Non Returned Books function"""
    # this should return a list of book details that are needed to be returned
    # the last value of the records in the list should be N/A
    print("******Testing the Retrieve Non Returned Books function******")
    Test = Retrieve_Non_Returned_Books(ReturnableBookList=[])
    print(Test)



def Test_Calculate_Dates():
    """This function tests the Check Dates function"""
    print("******Testing the Check Dates function******")
    #passing in the dates so that it can calculate the difference in the dates
    Test=Calculate_Dates("2020-4-23")
    print("%d days difference between date entered and today's current date"%(Test))


def Test_GetMemberGenres():
    """This function tests the GetMemberGenres function """
    print("******Testing the GetMemberGenres function******")
    # this function should return the values that will be used for creating the recomendation graph
    # as the values are returned back to this function
    Test=GetMemberGenres("jagg",MemberGenres=[])
    print(Test)


def Test_Update_Database_After_Check_Out():
    """This function Update Database After Check Out function"""
    print("******Testing the Update Database After Check Out******")
    # this is testing the function that updates the database when a check out has been made
    # once tested please press ctrl z on the database file to undo this action
    Update_Database_After_Check_Out(BookID="157",MemberID="Test")# check database to see
    print("Book has been checked out")

def  Test_Update_Database_After_Returned_Book():
    """This function tests the Update Database After Returned Book function"""
    print("******Testing the Update Database After Returned Book function******")
    # this is testing the function that updates the database when a creturn has been made
    # once tested please press ctrl z on the database file to undo this action
    Update_Database_After_Returned_Book([157])
    print("Book returned")


def Test_Write_Transaction_To_File():
    """This function tests the Write Transaction To File function"""
    # checking if the transaction gets written to the log file (check)
    print("******Testing Write Transaction To File function******")
    Write_Transaction_To_File("157",str(date.today()),"test","test genre","Test book")
    print("Transaction of Check out done")

def Test_Write_Return_To_Transaction():
    """This function tests the Write Return To Transaction function"""
    # checking if the transaction gets written to the log file (check)
    print("******Testing Write Transaction To File function******")
    Write_Return_To_Transaction([157],date.today())# should change from N/A to todays date
    print("Transaction of Return done")


#***************************CALLING TESTING FUNCTIONS*********************************************#
# calling the test functions for all the functions within this module


if __name__=="__main__":
    Test_Find_Matching_Returnable_Books()
    print("")
    Test_Check_Database_For_Member_Books()
    print("")
    Test_Check_Member_Overdue_Books()
    print("")
    Test_Locate_Book_By_ID()
    print("")
    Test_Get_Book_Genre()
    print("")
    Test_Check_Book_Availability()
    print("")
    Test_Get_Book_Name_By_ID()
    print("")
    Test_Search_Book()
    print("")
    Test_Overdue()
    print("")
    Test_Retrieve_Non_Returned_Books()
    print("")
    Test_Calculate_Dates()
    print("")
    # **these alter the database and log file**
    #Test_Update_Database_After_Check_Out()
    #Test_Update_Database_After_Returned_Book()
    #Test_Write_Transaction_To_File()
   # Test_Write_Return_To_Transaction()
    Test_GetMemberGenres()  # the same test result occurs when the following functions are run:
    #GetMemberGenres
    #Select_Popular_Genres
    #Popular_Books
    #FindRecomendedBooks
    #CalculateBookPopularity
    #This is because each function is returning back to the main function that is
    # returning the value back to the recommend book module



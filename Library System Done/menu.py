
"""This module is used to generate and run the Gui. It contains all the tkinter objects and contains functions that are used to
determine what outputs and messages should be displayed depending on what actions occur
Tkinter widgets being created is under the functions that have been defined
All the other modules return values to this module and this module. Done by F122571"""


from booksearch import *#importing the functions from the booksearch module so this module can call functions from it
from bookcheckout import *#importing the functions from the bookcheckout module so this module can call functions from it
from bookreturn import *#importing the functions from the bookreturn module so this module can call functions from it
from bookrecommend import *#importing the functions from the bookrecommend module so this module can call functions from it
import re# importing the module regular expressions so it can be used for validation purposes
import tkinter as tk# importing tkinter
from tkinter import ttk#  accessing the tkinter widgets

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg# getting the canvas from matplotlib
from matplotlib.figure import Figure# importing figure from matplotlib



def  Display_Returnable_Books(ReturnableBookList):
    """This function displays what books need to be returned

    ReturnableBookList = the list of books that are able to be returned (list)
    this function constantly shows what books need to be returned so that the user can select books and return them."""
    ReturnableBookList.sort(key=lambda x: int(x.split(",")[0]))# sorting the list by the book id so that its easier to read
    if len(ReturnableBookList)>=1:# if there is at least
        for Book in ReturnableBookList:# for each book in the list
            words=Book.split(",")
            #add the book id, member id and the checkout date of the books to the treeview so it can be displayed
            ReturnBooksTable.insert('', 'end', values=(words[0],words[1],words[4]),tag='Style')
    else:
        # if there are no books that need to be returned then it produces this message
        ReturnBookMessages.configure(text="There are no books that are on loan")


def  Display_OverDue_Books_ListBox(ObtainOverdueBooks):
    """This function displays what books are overdue when they have been returned
     ObtainOverdueBooks = list that contains all the books that were overdue (list)
     This function displays the books that are overdue in a listbox to warn the librarian that books were overdue
     by more than 60 days."""
    if len(ObtainOverdueBooks)>=1:# if there is at least one overdue book
        ReturnBookMessagesOverdue.configure(text="There are %d books overdue"%(len(ObtainOverdueBooks)))# display this message
        for OverDueBooks in ObtainOverdueBooks:
            ReturnBookMessageListBox.insert("end",OverDueBooks)# display the overdue books in the listbox
    else:
        ReturnBookMessagesOverdue.configure(text="There are no overdue books")# if there ar no overdue books print this message


def Return_Button_Clicked():
    """This function carries out the procedures when the return button is clicked
    it takes the selected rows from the treview and stores the ID of the books in a list so that it can be used in the
    return."""
    SelectedRows=[]# will contain the selected rows
    BookIDs=[]# will contain the book id's of the selected rows
    for selected_item in ReturnBooksTable.selection():
        item = ReturnBooksTable.item(selected_item)
        SelectedRows.append(item['values'])# adding the selected row to the list of selected rows
    for IDs in SelectedRows:
        BookIDs.append(IDs[0])# adding the ID's from that selected rows
    if len(BookIDs)>=1:
        # calling the function that gets the overdue books
        ObtainOverdueBooks=Return_Book(BookIDs)
        Clear_Fields()# this function clears all the fields
        Display_OverDue_Books_ListBox(ObtainOverdueBooks)# displaying all the overdue books in the listbox
        ReturnBookMessages.configure(text="Book(s) have been\n returned successfully")# showing the return was successful
    else:
        # if no rows were selected output this message
        ReturnBookMessages.configure(text="Please select at least one row from\n the table to return a book")


def Retrive_Books_For_Return():
    """This function gets the books that need to be returned by calling a function that returns the books
    it then calls the function that displays the books that can be returned."""
    ReturnableBookList=[]
    Retrive_List_Of_Returnable_Books(ReturnableBookList)# calling the function that will add the books to the returnable book list
    if len(ReturnableBookList)>0:
     Display_Returnable_Books(ReturnableBookList)# calling the function that displays what books can be returned
    else:
        # if there are no books that need to be returned then display this message
        ReturnBookMessages.configure(text="No books to be returned")


def Display_Filtered_Books_For_Return(FilteredBooksList):
    """This function displays the books that need to be returned when the librarian types in a member id or book id
       FilteredBooksList = the list of books that match or nearly match the book id or member id entered (list)."""
    FilteredBooksList.sort(key=lambda x: int(x.split(",")[0]))# sorting the list by the book id  so that its easier to read
    if len(FilteredBooksList) >= 1:# if the list of books has atleast one book
        for Book in FilteredBooksList:
            words = Book.split(",")
            # this displays the book id, the member id of who has the books and the check out date
            ReturnBooksTable.insert('', 'end', values=(words[0], words[1], words[4]), tag='Style')


def Clear_Fields():
    """This function clears all the textboxes and fields that were displaying old data
    It clears textboxes, labels and treeviews that were showing data that is not new ."""
    #clearing the values for the widgets in the SearchBookTab frame
    BookFoundLabel.configure(text="")
    SearchBookTextbox.delete('1.0','end-1c')
    for Results in ResultsTableForSearchingBooks.get_children():
      ResultsTableForSearchingBooks.delete(Results)
    SearchBookErrorMessage.configure(text="")
    # clearing the values for the widgets in the CheckOutBookTab frame
    CheckOutProcessLabel.configure(text="")
    BookIDTextbox.delete('1.0','end-1c')
    MemberIDTextbox.delete('1.0','end-1c')
    for Results in ResultsTableOverDueBooks.get_children():
      ResultsTableOverDueBooks.delete(Results)
    BooksOverdueLabel.configure(text="")
    # clearing the values for the widgets in the RecommendBookTab frame
    RecommendMemberIDTextbox.delete('1.0','end-1c')
    RecommendBookMessageLabel.configure(text="")
    # clearing the values for the widgets in the ReturnBookTab frame
    ReturnBookMessages.configure(text="")
    FilterReturnTextBox.delete('1.0', 'end-1c')
    ReturnBookMessageListBox.delete(0,'end')
    for Books  in ReturnBooksTable.get_children():
         ReturnBooksTable.delete(Books)
    ReturnBookMessagesOverdue.configure(text="")
    #calling the function that displays the books that need to be returned so that it is always loaded with the most updated version of the table
    Retrive_Books_For_Return()


def  Display_Overdue_Books(ListMemberBooksOverdue,ListMemberBooks):
    """This function displays the books that the member has overdue

       ListMemberBooksOverdue = list of books that the member has over due (list)
       ListMemberBooks =  the list of books that the member has loaned (list)
       This function shows the details of the books that the member has on loan
       if the book is overdue then it will display it in a red colour."""
    ListMemberBooks.sort(key=lambda x: int(x.split(",")[0]))# sorting the list by the book id's to aid readablity
    for Books in ListMemberBooks:
       for OverDueBooks in ListMemberBooksOverdue:
        Details=Books.split(",")
        Word=OverDueBooks.split(",")
        if Details[0]==Word[0]:# if the book id is also the same as the book id in the list of overdue books
            # show the book details in the treeview in a red colour, or black colour depending on the pyhton version
            ResultsTableOverDueBooks.insert('', 'end', values=(Details[0],Details[2],Details[1],Details[3],Details[4],Word[4]),tag='Overdue')
            BooksOverdueLabel.configure(text="These are the books the member has overdue")
    if len(ListMemberBooksOverdue)==0:
            # if the member has no books overdue then show this message
            BooksOverdueLabel.configure(text="There are no books that the user has that are overdue (all on loan for less than 60 days)")



def Display_Books_Found(ListOfBooksFound,ListOfBookIDOverdue):
    """This function displays the books that are being searched for
     ListOfBooksFound= list hat contains the books that are exactly the same or similar to the book id or name that was entered (list)
     ListOfBookIDOVerde = list that contains the book ids for books that are overdue
     This function displays the books that match or are similar to the book id
     and book name entered. if the book is overdue it displays it in a red colour."""
    ListOfBooksFound.sort(key=lambda x: int(x.split(",")[0]))# sorting the list of books by its id so its easier to read
    for Details in ListOfBooksFound:
        words=Details.split(",")
        if words[0] in ListOfBookIDOverdue:# if the book id of the book is equal to an id in the list that contains the id's of overdue books
            #display the book details in red, on certain python versions it will not show it in the colour red therefore it will now say if itsoverdue in the last column
            ResultsTableForSearchingBooks.insert('', 'end', values=(words[0],words[1],words[2],words[3],words[4],words[5],"Yes This Book is Overdue"),tag='Overdue')# this tag makes he text be red
        else:
            # display the book details in black as normal
            ResultsTableForSearchingBooks.insert('', 'end', values=(words[0], words[1], words[2], words[3], words[4], words[5]),tag='NotOverdue')


def Check_Out_Button_Clicked():
    """This function carries out the process of checking out books.
    it outputs messages according to what processes have or havent occurred"""
    for Results in ResultsTableOverDueBooks.get_children():
      ResultsTableOverDueBooks.delete(Results)# clearing the table that shows which books are overdue
    if BookIDTextbox.get("1.0",'end')=="\n":
        Clear_Fields()
        # if there is nothing in the textbox then display this message
        CheckOutProcessLabel.configure(text="Please enter a Book ID")
    elif MemberIDTextbox.get("1.0",'end')=="\n":#if there is nothing in the textbox
        Clear_Fields()
        # if there is nothing in the textbox then display this message
        CheckOutProcessLabel.configure(text="Please enter a Member ID")
    else:
            BookID = BookIDTextbox.get("1.0",'end-1c')  # 1.0 makes it read from the first line and the first character
            # end -1c will deletes the last character which would be a space
            MemberID = MemberIDTextbox.get("1.0",'end-1c')
            IsInputsValid=Check_Out_Book_Validate_Inputs(BookID,MemberID)
            if IsInputsValid==True:
                IsBookLocated=Check_Out_Book_Location(BookID)# checking if the book exists in the database
                if IsBookLocated==True:
                    IsBookAvailable=Check_Out_Books_Availability(BookID)# checking if the book is available
                    if IsBookAvailable==True:
                       Check_Out_Book(BookID,MemberID)# checking out the book
                       ListMemberBooks=[]
                       ListMemberBooksOverdue=[]
                       # finding out if the member has any overdue books
                       Check_Member_Books_Overdue(MemberID,ListMemberBooks,ListMemberBooksOverdue)
                       Clear_Fields()# clearing rhe contents in the widgets
                       Display_Overdue_Books(ListMemberBooksOverdue,ListMemberBooks)# calling the function that displays the members overdue books
                       CheckOutProcessLabel.configure(text="Check out Completed")
                    else:
                        Clear_Fields()
                        # if the book is not available output this message
                        CheckOutProcessLabel.configure(
                            text="The Book that corrosponds to the Book ID entered is not currently available,\n please enter a different Book ID")
                else:
                    # if the book id does not exist in the database then print out this message
                    Clear_Fields()
                    CheckOutProcessLabel.configure(
                            text="There is no book in the system that has the book id entered, please enter a new one")
            else:
                Clear_Fields()
                # if the book id and member id are not valid inputs then it displays this message
                CheckOutProcessLabel.configure(text="Please enter valid Member ID that consists\nof 4 letters and a valid Book ID which is an integer")


def Draw_Recomendation_Graph(BookNames,BookPopularity) :
    """This is responsible for instantiating the recommend book graph

     Book Names = the list of book names that are being recommended (list)
     Book popularity = the list of book ratings that corresponds to a book (list)
     This function creates the axis and the bar chart."""
    Fig = Figure(figsize=(7, 5))# adjusting the size of the graph
    Axis = Fig.add_subplot(1, 1, 1)
    Axis.barh(BookNames,BookPopularity,color="m")# creating the horizontal bar chart
    Display_Graph(Fig)# calling the function that displays the graph


def Recommend_Button_Clicked():
    """This is function controls the process of recommending books
      it out puts messages according to what processes have occurred."""
    if RecommendMemberIDTextbox.get("1.0", 'end') == "\n":# if the textbox is empty
        Clear_Fields()
        RecommendBookMessageLabel.configure(text="Please enter ID")# display this message
    else:
        MemberID = RecommendMemberIDTextbox.get("1.0", 'end-1c')
        # if the member id has digits in it or does not have a length of 4 characters
        if re.search("[0-9]",MemberID) or len(MemberID)!=4:# validation check
            Clear_Fields()
            # display this message
            RecommendBookMessageLabel.configure(text="Please enter valid member id that does not\n consist of digits and has a length of 4")
        else:
            # call the function for recommending the books
            RecommendedBooks=Recommend_Book_For_Member(MemberID)
            # book names is the first list returned
            BookNames=RecommendedBooks[0]
            # book popularity is the second list returned
            BookPopularity=RecommendedBooks[1]
            Draw_Recomendation_Graph(BookNames, BookPopularity)# calling the function that creates the graph using
            # these parameters
            Clear_Fields()
            # displaying this ,message
            RecommendBookMessageLabel.configure(
                text="The following books are recommended for the member\n graph is read by book names against\n the popularity")



def  Display_Graph(Fig):
    """This function embeds the graph into the tkinter frame and
     displays it in the frame
     Fig = the returned graph from the function that draws the graph."""
    canvas=FigureCanvasTkAgg(Fig,master=ReccomendBookTab)# creating the canvas space
    canvas.draw()# drawing the graph on the frame
    canvas.get_tk_widget().place(x=500,y=0)# placing the graph on the frame



def Search_ForBooks(event):
    """This function calls the search function when ever the user types into the textbox

     this enables the system to show which books match or have a close match to the book id or
     the name of the book whilst the user is typing in case the user does not remember the specific book id or book name they
     are searching for."""
    SearchedValue = SearchBookTextbox.get("1.0", 'end-1c')
    if SearchedValue == "":# if nothing has been typed
        Clear_Fields()
        for Results in ResultsTableForSearchingBooks.get_children():
            ResultsTableForSearchingBooks.delete(Results)# clear the display of books

    else:
        ListOfBooksFound = []
        ListOfBookIDOverdue = []
        # creating two empty new lists
        # Book is the value typed into the text box, can be a word or a number for the book id
        Book = SearchBookTextbox.get("1.0",
                                         'end-1c')  # 1.0 makes it read from the first line and the first character, end -1c will deletes the last character which would be a space
        Search_For_Book(Book, ListOfBooksFound, ListOfBookIDOverdue)# calling the search function with the lists and the parameter of the book
        if len(ListOfBooksFound) != 0:# if there were books found
            for Results in ResultsTableForSearchingBooks.get_children():
                ResultsTableForSearchingBooks.delete(Results)
            BookFoundLabel.configure(text="Books Found: %s. Books in red are overdue" % (len(ListOfBooksFound)))
            Display_Books_Found(ListOfBooksFound, ListOfBookIDOverdue)# call the function that displays the books

        else:
            # if no books had been found
            for Results in ResultsTableForSearchingBooks.get_children():
                ResultsTableForSearchingBooks.delete(Results)
            BookFoundLabel.configure(text="No Books Found")


def Filter_Return(event):
        """This function calls the retrieve books for return function each time something has been typed into the text box

        this enables the system to show which books match or have a close match to the book id or
        the member id whilst the user is typing in case the user does not remember the specific book id or member id they
        are searching for
        this makes it easier if they want to check out a specific Book by its id or a specify member by their id."""
        SearchedValue = FilterReturnTextBox.get("1.0", 'end-1c')
       # if the textbox is empty
        if SearchedValue == "":
            Clear_Fields()
            for Results in ReturnBooksTable.get_children():
                ReturnBooksTable.delete(Results)# clear the table as there is no match
            # call the function that gets the list of books that eed to be returned ad then displays it so there
            # is always contents in the treeview that the user can select from (this is the default list)
            Retrive_Books_For_Return()
        else:
            FilteredBooksList = []# this list will contain all the books that contain a similar
            # or identical name or id to the one entered
            Indetifier = FilterReturnTextBox.get("1.0",
                                                 'end-1c')
            # 1.0 makes it read from the first line and the first character, end -1c will deletes the last charecter which would be a space
            # identifier is the value in the textbox whether its  a number or a word or letter
            Filtered_Books(Indetifier, FilteredBooksList)# calling the function that filters through the books to return
            if len(FilteredBooksList) != 0 and event.keysym!='Control_L':
               # if there are books found and the left control key is not pressed
                for Results in ReturnBooksTable.get_children():
                    ReturnBooksTable.delete(Results)# clear the treeview of the current results
                # call the function that displays the filtered throuh books
                Display_Filtered_Books_For_Return(FilteredBooksList)

            elif event.keysym=='Control_L' or event.keysym=='Control_R':
                # if the left control button or the right control button is pressed or held down
                pass# do nothing
            else:
                # otherwise clear the table and display a message
                for Results in ReturnBooksTable.get_children():
                    ReturnBooksTable.delete(Results)
                ReturnBookMessages.configure(text="No matching member\n id or book id")



#**************CREATING THE TKINTER WIDGETS MAIN CODE***************#

My_Root = tk.Tk()# creating the root that creates the application window
My_Root.geometry('1500x550')# creating the window size
My_Root.title('LIBRARIAN SYSTEM')# title of the window

Mystyle = ttk.Style()# creating the style
Mystyle.configure("Heading", font = ('arial', 12))# setting the style for the tkinter tree views used

# creating a notebook
notebook = ttk.Notebook(My_Root)
notebook.pack(pady=10, expand=True)


# creating all the widgets on the search tab
SearchBookTab = tk.Frame(notebook, width=2000, height=2000,bg="pink")# creating the search tab
SearchBookTab.pack(fill='both', expand=True)
#creating label that shows how many books were found and placing it in the frame
BookFoundLabel = tk.Label(SearchBookTab,bg="pink",fg="magenta",font=('arial', 12))
BookFoundLabel.place(x=0, y=170)
#creating label that notifies the user on typing in a name or id to search for a book and placing it in the frame
SearchBookLabel=tk.Label(SearchBookTab,text="Type in the Name or ID of the book you want to search for",bg="pink",fg="magenta",font=('arial', 12))
SearchBookLabel.place(x=40,y=65)
#creating the textbox that the user can type into to search for a book and placing it in the frame
SearchBookTextbox=tk.Text(SearchBookTab,height=1,width=45)
SearchBookTextbox.place(x=40,y=100)
SearchBookTextbox.bind("<KeyRelease>",Search_ForBooks)# adding a bind which enables detection when a key is pressed. it calls the function that deals with this detection
#creating the label that displays messages when searches are being made and placing it in the frame
SearchBookErrorMessage=tk.Label(SearchBookTab,bg="pink",fg="magenta",font=('arial', 12))
SearchBookErrorMessage.place(y=100,x=650)


# Creating the tree view for the search tab frame
ResultsTableForSearchingBooksColumns = ('ID', 'Genre', 'Title','Author','Purchase Date','Member ID','Overdue?')# columns for the tree view
ResultsTableForSearchingBooks = ttk.Treeview(SearchBookTab,columns=ResultsTableForSearchingBooksColumns, show='headings',height=5)# creating the tree view
#creating the column headings for the treeview , the anchor w makes text shift to the left position
ResultsTableForSearchingBooks.heading('ID', text='Book ID',anchor='w')
ResultsTableForSearchingBooks.heading('Genre', text='Book Genre',anchor='w')
ResultsTableForSearchingBooks.heading('Title', text='Book Title',anchor='w')
ResultsTableForSearchingBooks.heading('Author', text='Book Author',anchor='w')
ResultsTableForSearchingBooks.heading('Purchase Date', text='Purchase Date',anchor='w')
ResultsTableForSearchingBooks.heading('Member ID', text='Member ID',anchor='w')
ResultsTableForSearchingBooks.heading('Overdue?', text='Overdue?',anchor='w')
ResultsTableForSearchingBooks.place(y=200)# assigning the positioning of the treeview
# creating the tags that will be used in the treeview
ResultsTableForSearchingBooks.tag_configure('Overdue', foreground='red', font=('arial', 12))
ResultsTableForSearchingBooks.tag_configure('NotOverdue', foreground='black', font=('arial', 12))
# creating the scroll bar for this tree view  and configuring it to work alongside the treeview
SearchBookScrollBar= ttk.Scrollbar(SearchBookTab,orient="vertical",command=ResultsTableForSearchingBooks.yview)#creating the vertical scroll bar
ResultsTableForSearchingBooks.configure(yscrollcommand = SearchBookScrollBar.place(x=1420,y=200))# positioning the scrollbar for the treeview


#Creating the widgets on the Check out tab
# creating the check out tab frame
CheckOutBookTab = tk.Frame(notebook, width=800, height=800,bg="pink")
CheckOutBookTab.pack(fill='both', expand=True)
# creating a label that displays messages that occur when processes occur during the check out and placing it in the frame
CheckOutProcessLabel=tk.Label(CheckOutBookTab,bg="pink",fg="magenta",font=('arial', 12))
CheckOutProcessLabel.place(x=400, y=125)
# creating a label and placing it in the frame
BookIDLabel = tk.Label(CheckOutBookTab,text="Enter Book ID",bg="pink",fg="magenta",font=('arial', 12))
BookIDLabel.place(x=20, y=100)
# creating a label and placing it in the frame
MemberIDLabel = tk.Label(CheckOutBookTab,text="Enter Member ID",bg="pink",fg="magenta",font=('arial', 12))
MemberIDLabel.place(x=20, y=150)
# creating a textbox where the user types in the Book id and placing it in the frame
BookIDTextbox=tk.Text(CheckOutBookTab,height=1,width=25)
BookIDTextbox.place(x=160,y=100)
# creating a textbox where the user types in the Member id and placing it in the frame
MemberIDTextbox=tk.Text(CheckOutBookTab,height=1,width=25)
MemberIDTextbox.place(x=160,y=150)
# creating a button that enables the user to check out a book by calling the function associated to its comand, and placing it on the frame
CheckOutBookButton=tk.Button(CheckOutBookTab,text="Check Out Book",command=Check_Out_Button_Clicked,bg="white",fg="magenta",font=('arial', 12))
CheckOutBookButton.place(x=20,y=200)


#Creating the tree view for the overdue books to be displayed
#creating the columns for the tree view
ResultsTableOverDueBooksColumns = ('BookID','Title','Genre','Author','Purchase Date','Check Out Date')
# creating the tree view
ResultsTableOverDueBooks= ttk.Treeview(CheckOutBookTab, columns=ResultsTableOverDueBooksColumns , show='headings',height=5)
# creating the headings for the treeview
ResultsTableOverDueBooks.heading('BookID', text='Book ID',anchor='w')#makes the position go to the left
ResultsTableOverDueBooks.heading('Title', text='Book Title',anchor='w')
ResultsTableOverDueBooks.heading('Genre', text='Genre',anchor='w')
ResultsTableOverDueBooks.heading('Author', text='Author',anchor='w')
ResultsTableOverDueBooks.heading('Purchase Date', text='Purchase Date',anchor='w')
ResultsTableOverDueBooks.heading('Check Out Date', text='Check Out Date',anchor='w')
# creating a tag for the treeview that has the colour red
ResultsTableOverDueBooks.tag_configure('Overdue', foreground='red', font=('arial', 12))
# creating a scroll bar for the treeview
CheckOutBookScrollBar= ttk.Scrollbar(CheckOutBookTab,orient="vertical",command=ResultsTableOverDueBooks.yview)#creating the vertical scroll bar
ResultsTableOverDueBooks.configure(yscrollcommand = CheckOutBookScrollBar.place(x=1205,y=300))# configuring the scroll bar
ResultsTableOverDueBooks.place(y=285)# assigning the place of the tree view
#creating a lablel that shows if books are overdue or not and placing it on the frame
BooksOverdueLabel = tk.Label(CheckOutBookTab,bg="pink",fg="magenta",font=('arial', 12))
BooksOverdueLabel.place(x=0, y=250)


#Creating the widgets on the return book tab frame
#creating the ReturnBook tab frame
ReturnBookTab = tk.Frame(notebook, width=800, height=800,bg="pink")
ReturnBookTab.pack(fill='both', expand=True)
#creating the label that shows messages when returning a book  and placing it on the frame
ReturnBookMessages=tk.Label(ReturnBookTab,bg="pink",fg="magenta",font=('arial', 12))
ReturnBookMessages.place(x=0, y=360)
#creating the label that shows messages when returning a book  and placing it on the frame
ReturnBookMessagesOverdue=tk.Label(ReturnBookTab,bg="pink",fg="magenta",font=('arial', 12))
ReturnBookMessagesOverdue.place(x=800, y=180)
#creating the label that shows where the user enters the book id when returning a book  and placing it on the frame
ReturnBookIDLabel= tk.Label(ReturnBookTab,text="Select Book ID from table to return Books",bg="pink",fg="magenta",font=('arial', 12))
ReturnBookIDLabel.place(x=0, y=170)
#creating the label tht shows where the user enters the book id or the member id and placing it in the frame
ReturnFilterLabel= tk.Label(ReturnBookTab,text="Type in Member ID or Book ID that you are looking for",bg="pink",fg="magenta",font=('arial', 12))
ReturnFilterLabel.place(x=0, y=70)


#Creating the treeview for the Return book tab
# creating the columns for the treeview
ReturnBooksTableColumns = ('ID','MemberID' ,'CheckOutDate')
# creating the treeview
ReturnBooksTable = ttk.Treeview(ReturnBookTab,columns=ReturnBooksTableColumns, show='headings',height=5)
#creating the headings for the treeview
ReturnBooksTable.heading('ID', text='Book ID',anchor='w')#makes the position go to the left
ReturnBooksTable.heading('MemberID', text='Member ID',anchor='w')
ReturnBooksTable.heading('CheckOutDate', text='Check Out Date',anchor='w')
ReturnBooksTable.place(y=200)# placing treeview on the frame
#adding a scroll bar
ReturnBookTableScrollBar= ttk.Scrollbar(ReturnBookTab,orient="vertical",command=ReturnBooksTable.yview)#creating the vertical scroll bar
ReturnBooksTable.configure(yscrollcommand = ReturnBookTableScrollBar.place(x=620,y=200))#configuring the scroll bar so it works with the treeview
#adding a button that enables the librarian to return a book by clicking on it as it calls the return button clicked function
ReturnBookButton=tk.Button(ReturnBookTab,text="Return the Books",command=Return_Button_Clicked,bg="white",fg="magenta",font=('arial', 12))
ReturnBookButton.place(x=470,y=360)# placing it on the frame
# creating a listbox that will display which books are overdue  and placing it on the frame
ReturnBookMessageListBox=tk.Listbox(ReturnBookTab,fg="red",width=50,height=5,font=('arial', 12))
ReturnBookScrollBarListBox= ttk.Scrollbar(ReturnBookTab,orient="vertical",command=ReturnBookMessageListBox.yview)#creating a scroll bar that works with the listbox
ReturnBookMessageListBox.configure(yscrollcommand=ReturnBookScrollBarListBox.place(x=1260,y=210))# configuring the listbox and scroll bar
ReturnBookMessageListBox.place(x=800,y=210)
ReturnBooksTable.tag_configure('Style', foreground='black', font=('arial', 12))# making the font size bigger and colour to black
# this textbox is used for the librarian to filter through the books that need to be returned in case they want to return all books that belong to a member
# or look for s specific Book ID to be removed
FilterReturnTextBox=tk.Text(ReturnBookTab,height=1,width=45)
FilterReturnTextBox.place(x=0,y=100)# placing it in the frame
FilterReturnTextBox.bind("<KeyRelease>",Filter_Return)# binding the textbox so that when a key is pressed a function is called


#Creating the widgets needed for the Recommend book tab
ReccomendBookTab = tk.Frame(notebook, width=800, height=800,bg="pink")
ReccomendBookTab.pack(fill='both', expand=True)
RecommendMemberIDTextbox=tk.Text(ReccomendBookTab,height=1,width=10)
RecommendMemberIDTextbox.place(x=220,y=100)
RecommendMemberIDLabel = tk.Label(ReccomendBookTab,text="Type Member's\n ID for book recommendation",bg="pink",fg="magenta",font=('arial', 12))
RecommendMemberIDLabel.place(x=15, y=100)
RecommendBookMessageLabel=tk.Label(ReccomendBookTab,bg="pink",fg="magenta",font=('arial', 12))
RecommendBookMessageLabel.place(x=0,y=300)
RecommendButton=tk.Button(ReccomendBookTab, text="Recommend\n Book", command=Recommend_Button_Clicked,bg="white",fg="magenta",font=('arial', 12))#have it above
RecommendButton.place(x=50,y=200)


# adding the SearchBookTab,CheckOutTab,ReturnBookTab and ReccomendBookTab to the notebook with their respective texts
notebook.add(SearchBookTab, text='Search For Book')
notebook.add(CheckOutBookTab, text='Check Out Book')
notebook.add(ReturnBookTab, text='Return Book')
notebook.add(ReccomendBookTab, text='Recommend Book')


# calling the function that shows all the books that need to be returned so that its visible as soon as the program is ran
Retrive_Books_For_Return()
My_Root.mainloop()#keeps the window visible on the screen.

#****************Testing Remarks*************************#
# for this module there is no testing as if the GUI operates as intended then that is a test in itself
# as this module is actually directly in use



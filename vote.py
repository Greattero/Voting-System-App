from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector



db = mysql.connector.connect(host ="localhost",
                             user="root",
                             password="Greattero123",
                             database="voting"
                             )

cur=db.cursor()




class EntryApp:
    def __init__(self,root):
        self.root = root
        
    
    def entry(self):
        self.root.title("Logins")
        self.root.geometry("300x200")
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.root.resizable(False,False)
        self.icon_image = Image.open("C:\\Users\\great\\OneDrive\\Desktop\\Voting\\umaticon.ico")
        self.icon_photo = ImageTk.PhotoImage(self.icon_image)
        self.root.iconphoto(False, self.icon_photo)

        # Load the background image
        self.backpic = PhotoImage(file="C:\\Users\\great\\OneDrive\\Desktop\\Voting\\background.png")

        # Create a label for the background image
        self.background_label = Label(self.root, image=self.backpic)
        self.background_label.place(x=0, y=0, relheight=1, relwidth=1)


        Label(root, text="Student Voting Portal", font="arial 14 bold").pack(pady = 10)
        self.v1 = StringVar()
        self.v2 = StringVar()
        self.v3 = StringVar()
        def clear_watermark(event):
                if self.e1.get() == "Enter Index Number":
                    self.e1.delete(0,END)
                if self.e2.get() == "Enter Password":
                    self.e2.delete(0,END)
        self.e1= ttk.Entry(root, textvariable=self.v1,font= "arial 15 bold ")
        self.e1.insert(0,"Enter Index Number")
        self.e1.bind("<FocusIn>",clear_watermark)
        self.e1.pack(side = TOP, pady = 10)

        self.e2 = ttk.Entry(root, textvariable=self.v2, font= "arial 15 bold",show="*")
        self.e2.insert(0,"Enter Password")
        self.e2.bind("<FocusIn>",clear_watermark)
        self.e2.pack(side = TOP, pady = 10)

        
        self.verify_instance = Verify(self.root, self.v1, self.v2, self.v3)

        Button(root, text =" Login ", bg="black", fg="white", font=("Arial", 15, "bold"),command =self.verify_instance.verify).pack()

class Verify(EntryApp):
    def __init__(self,root,v1,v2,v3):
        super().__init__(root)
        self.root = root
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.cur = cur


    def verify(self):
        user = self.v1.get()
        pas = self.v2.get()
        self.cur.execute("SELECT * FROM student_names WHERE index_no = %s AND password = %s", (user, pas))
        self.result = self.cur.fetchone()
        if self.result:
            self.m1 = messagebox.showinfo("Message", "You have successfully logged in")
            self.root.withdraw()
            Vote(self.root, self.v1, self.v2, self.v3,self.m1).vote()

        else:
            self.m1 = messagebox.showinfo("Message", "Not successful")



class Vote(EntryApp):
    def __init__(self, root, v1, v2, v3,m1):
        super().__init__(root)
        self.root = root
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.cur = cur
        self.db = db
        self.m1 = m1
        self.g = 0
        self.cur.execute("SELECT verification FROM student_names WHERE index_no = %s", (self.v1.get(),))
        self.verification = self.cur.fetchone()


        # Variables to store the selected candidate for each category
        self.selected_president = StringVar()
        self.selected_financial_secretary = StringVar()

        self.selected_president.set("o")
        self.selected_financial_secretary.set("o")

    def vote(self):
        self.top = Toplevel(root)
        self.top.title("Voting System")
        self.top.geometry("700x670")
        self.top.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.icon_image = Image.open("C:\\Users\\great\\OneDrive\\Desktop\\Voting\\umaticon.ico")
        self.icon_photo = ImageTk.PhotoImage(self.icon_image)
        self.top.iconphoto(False, self.icon_photo)



        def submit_votes():
            messagebox.showinfo("Votes Submitted",
                                f"JCR President: {self.selected_president.get()}\n"
                                f"Financial Secretary: {self.selected_financial_secretary.get()}")
            
            self.cur.execute("SELECT verification FROM student_names WHERE index_no = %s", (self.v1.get(),))
            self.verification = self.cur.fetchone()
            


        # Create a Notebook (tab container)
        self.notebook = ttk.Notebook(self.top)
        self.notebook.pack(expand=True, fill="both")

        # Create three tabs
        self.tab1 = Frame(self.notebook, bg="white")
        self.tab2 = Frame(self.notebook)


        # Add the tabs to the notebook
        self.notebook.add(self.tab1, text="Candidates")
        self.notebook.add(self.tab2, text="View Results")

                # Function to move the text
        def move_text():
            # Update the position of the text
            self.canvas.move(self.text, -2, 0)  # Move the text 2 pixels to the left
            self.x -= 2
            
            # Check if the text has moved out of view
            if self.x < -self.text_width:
                self.x = self.canvas_width
                self.canvas.coords(self.text, self.x, self.y)  # Reset the position to the right end
            
            # Schedule the function to run again after 30 ms
            self.canvas.after(30, move_text)

        # Create a Canvas widget
        self.canvas_width = 800
        self.canvas_height = 35
        self.canvas = Canvas(self.tab1, width=self.canvas_width, height=self.canvas_height, bg="green")
        self.canvas.pack(expand=True, fill="both")

        # Add text to the Canvas
        self.marquee_text = "SELECT THE CANDIDATES YOU WANT TO VOTE FOR. CLICK ON SUBMIT VOTES TO SUBMIT YOUR VOTES. YOU CAN ONLY VOTE ONCE!!!"
        self.text = self.canvas.create_text(self.canvas_width, self.canvas_height // 2, text=self.marquee_text, anchor='w', font=('Helvetica', 16))

        # Get the width of the text
        self.text_width = self.canvas.bbox(self.text)[2] - self.canvas.bbox(self.text)[0]

        # Initial position of the text
        self.x = self.canvas_width
        self.y = self.canvas_height // 2

        # Start the text moving
        move_text()



        # Categories in tab2
        pe = Button(self.tab1, text="JCR President", bg="white", font=("Oxygen",13), relief="sunken")
        pe.place(x=270, y=50)

        self.president_candidates = ["Richy","Bacho","Sir Fred"]
        self.fs_candidates = ["Yajen","Lomo","Forex"]

        # Candidates for JCR President
        img1=Image.open("C:\\Users\\great\\OneDrive\\Desktop\\Voting\\richie.jpg")
        img1=img1.resize((200,150),Image.LANCZOS)
        img1=ImageTk.PhotoImage(img1)
        l1=Label(self.tab1,image=img1)
        l1.place(x=0,y=100)

        img=Image.open("C:\\Users\\great\\OneDrive\\Desktop\\Voting\\bacho.jpg")
        img=img.resize((200,150),Image.LANCZOS)
        img=ImageTk.PhotoImage(img)
        l1=Label(self.tab1,image=img)
        l1.place(x=230,y=100)

        img3=Image.open("C:\\Users\\great\\OneDrive\\Desktop\\Voting\\fred.jpg")
        img3=img3.resize((200,150),Image.LANCZOS)
        img3=ImageTk.PhotoImage(img3)
        l1=Label(self.tab1,image=img3)
        l1.place(x=460,y=100)

        vertical_line =Frame(self.tab1, bg='black', width=2, height=200)
        vertical_line.place(x=200,y=100)

        vertical_line =Frame(self.tab1, bg='black', width=2, height=200)
        vertical_line.place(x=460,y=100)


        candidate_radio = Radiobutton(self.tab1, text="Richy", variable=self.selected_president, value="Richy", bg="white", font=("Oxygen", 12))
        candidate_radio.place(x=50 ,y=270)
        candidate_radio = Radiobutton(self.tab1, text="Bacho", variable=self.selected_president, value="Bacho", bg="white", font=("Oxygen", 12))
        candidate_radio.place(x=280 ,y=270)
        candidate_radio = Radiobutton(self.tab1, text="Sir Fred", variable=self.selected_president, value="Sir Fred", bg="white", font=("Oxygen", 12))
        candidate_radio.place(x=520 ,y=270)

        # Candidates for General Secretary
        pe = Button(self.tab1, text="Financial Secretary", bg="white", font=("Oxygen",13), relief="sunken")
        pe.place(x=250, y=320)

        img4=Image.open("C:\\Users\\great\\OneDrive\\Desktop\\Voting\\yajen.jpg")
        img4=img4.resize((200,150),Image.LANCZOS)
        img4=ImageTk.PhotoImage(img4)
        l1=Label(self.tab1,image=img4)
        l1.place(x=0,y=370)

        img5=Image.open("C:\\Users\\great\\OneDrive\\Desktop\\Voting\\lomo.jpg")
        img5=img5.resize((200,150),Image.LANCZOS)
        img5=ImageTk.PhotoImage(img5)
        l1=Label(self.tab1,image=img5)
        l1.place(x=230,y=370)

        img6=Image.open("C:\\Users\\great\\OneDrive\\Desktop\\Voting\\forex.jpg")
        img6=img6.resize((200,150),Image.LANCZOS)
        img6=ImageTk.PhotoImage(img6)
        l1=Label(self.tab1,image=img6)
        l1.place(x=460,y=370)

        candidate_radio = Radiobutton(self.tab1, text="Yajen", variable=self.selected_financial_secretary, value="Yajen", bg="white", font=("Oxygen", 12))
        candidate_radio.place(x=50 ,y=540)
        candidate_radio = Radiobutton(self.tab1, text="Lomo", variable=self.selected_financial_secretary, value="Lomo", bg="white", font=("Oxygen", 12))
        candidate_radio.place(x=280 ,y=540)
        candidate_radio = Radiobutton(self.tab1, text="Forex", variable=self.selected_financial_secretary, value="Forex", bg="white", font=("Oxygen", 12))
        candidate_radio.place(x=520 ,y=540)


        vertical_line1 =Frame(self.tab1, bg='black', width=2, height=200)
        vertical_line1.place(x=200,y=370)

        vertical_line1 =Frame(self.tab1, bg='black', width=2, height=200)
        vertical_line1.place(x=460,y=370)

        self.cur.execute("CREATE TABLE IF NOT EXISTS presidents_table (name VARCHAR(255) NOT NULL, votes INT DEFAULT 0,PRIMARY KEY (name))")
        self.db.commit()
        self.cur.execute("CREATE TABLE IF NOT EXISTS financial_secretary (name VARCHAR(255) NOT NULL, votes INT DEFAULT 0,PRIMARY KEY (name))")
        self.db.commit()


        def put():
            self.setter_president=[StringVar(value=name[:2]) for name in self.president_candidates]
            self.first_two_names_president=[IntVar(value=0) for _ in self.setter_president]

            for name,num in zip(self.president_candidates,self.first_two_names_president):
                var = num.get()
                self.cur.execute("insert ignore into presidents_table (name,votes) VALUES(%s,%s)",(name,var))
            
            self.db.commit()
            
            if self.selected_president.get():
                    self.cur.execute("INSERT INTO presidents_table (name, votes) VALUES (%s, %s) ON DUPLICATE KEY UPDATE votes = votes + 1",(self.selected_president.get(), 1))
                    self.db.commit()

            self.cur.execute("SELECT name, votes FROM presidents_table")
            self.voteno_president = self.cur.fetchall()
            
            if self.voteno_president:
                self.data = [list(pair) for pair in self.voteno_president]
            
            h1=Label(self.tab2,text= "JCR PRESIDENT", font="arial 20 bold")
            h1.grid(row=0,columnspan=2)

       
            i = 0
            r1=2
            for i in range(len(self.data)):
                c1=0
                for j in range(2):
                    self.entry1 = Entry(self.tab2,width=20,font = "arial 23")
                    self.entry1.grid(row=r1, column=c1)
                    self.entry1.insert(0,self.data[i][j])
                    self.entry1.config(state = "readonly")
                    c1+=1
                r1+=1


            #Financial Secretary
            self.setter_fs=[StringVar(value=name[:2]) for name in self.fs_candidates]
            self.first_two_names_fs=[IntVar(value=0) for _ in self.setter_fs]

            for name,num in zip(self.fs_candidates,self.first_two_names_fs):
                var = num.get()
                self.cur.execute("insert ignore into financial_secretary (name,votes) VALUES(%s,%s)",(name,var))
            
            self.db.commit()
            
            if self.selected_financial_secretary.get():
                    self.cur.execute("INSERT INTO financial_secretary (name, votes) VALUES (%s, %s) ON DUPLICATE KEY UPDATE votes = votes + 1",(self.selected_financial_secretary.get(), 1))
                    self.db.commit()

            self.cur.execute("SELECT name, votes FROM financial_secretary")
            self.voteno_fs = self.cur.fetchall()
            
            if self.voteno_fs:
                self.data_fs = [list(pair) for pair in self.voteno_fs]


            h2=Label(self.tab2,text= "FINANCIAL SECRETARY", font="arial 20 bold")
            h2.grid(row=5,columnspan=2)

            f = 4
            r2=6
            for f in range(len(self.data_fs)):
                c2 = 0
                for j in range(2):
                    self.entry2 = Entry(self.tab2,width=20,font = "arial 23")
                    self.entry2.grid(row=r2, column=c2)
                    self.entry2.insert(0,self.data_fs[f][j])
                    self.entry2.config(state = "readonly")
                    c2+=1
                r2+=1



        def comb():
            if self.verification[0] == "Voted":
                memes()
            
            else:
                if self.selected_president.get() == "o" or self.selected_financial_secretary.get() == "o":
                    if self.submit_button:
                        self.m1=messagebox.showinfo("Message", "You have to select the candidates\nbefore you click on Submit Vote")
                else:
                    update_verify()
                    submit_votes()
                    put()
                    print("Done")


            


        def memes():
            def resize_image(image_path, size):
                image = Image.open(image_path)
                image = image.resize(size)  # Resize image
                return ImageTk.PhotoImage(image)

            # Create the Toplevel window

            # Desired size for resizing
            size = (300, 300)

            # Resize and load images
            self.ph1 = resize_image("C:\\Users\\great\\OneDrive\\Desktop\\Voting\\m1.jpg", size)
            self.ph2 = resize_image("C:\\Users\\great\\OneDrive\\Desktop\\Voting\\m2.jpg", size)
            self.ph3 = resize_image("C:\\Users\\great\\OneDrive\\Desktop\\Voting\\m3.jpg", size)
            self.ph4 = resize_image("C:\\Users\\great\\OneDrive\\Desktop\\Voting\\m4.jpg", size)
            self.ph5 = resize_image("C:\\Users\\great\\OneDrive\\Desktop\\Voting\\m5.jpg", size)
            self.ph6 = resize_image("C:\\Users\\great\\OneDrive\\Desktop\\Voting\\m6.jpg", size)

            # # Example usage in a Label
            # label = Label(self.meme, image=self.ph1)
            # label.pack(fill="both", expand=True)  # Fill the Toplevel window

            self.pictures=[self.ph1,self.ph2,self.ph3,self.ph4,self.ph5,self.ph6]

        # Display images in the Toplevel window
            while self.submit_button:
                self.meme = Toplevel()
                self.meme.title("Meme")
                self.meme.geometry("300x300")
                self.meme.resizable(False,False)
                label = Label(self.meme, image=self.pictures[self.g])
                label.grid(row=self.g // 2, column=self.g % 2, padx=5, pady=5)
                self.g+=1
                break
            if self.g == 6:
                self.g = 0  


    # Submit Vote button
        self.submit_button = Button(self.tab1, text="Submit Vote", font=("Oxygen", 14), command=comb)
        self.submit_button.place(x=270, y=600)
        def update_verify():
            self.cur.execute("""
                UPDATE student_names
                SET verification = 'Voted'
                WHERE index_no = %s
            """, (self.v1.get(),))
            self.db.commit()

        def view():
            self.setter_president=[StringVar(value=name[:2]) for name in self.president_candidates]
            self.first_two_names_president=[IntVar(value=0) for _ in self.setter_president]

            for name,num in zip(self.president_candidates,self.first_two_names_president):
                var = num.get()
                self.cur.execute("insert ignore into presidents_table (name,votes) VALUES(%s,%s)",(name,var))
            
            self.db.commit()
            
            if self.selected_president.get() != "o" or self.selected_financial_secretary.get() != "o":
                    self.cur.execute("INSERT INTO presidents_table (name, votes) VALUES (%s, %s) ON DUPLICATE KEY UPDATE votes = votes + 1",(self.selected_president.get(), 1))
                    self.db.commit()

            self.cur.execute("SELECT name, votes FROM presidents_table")
            self.voteno_president = self.cur.fetchall()
            
            if self.voteno_president:
                self.data = [list(pair) for pair in self.voteno_president]
            
            h1=Label(self.tab2,text= "JCR PRESIDENT", font="arial 20 bold")
            h1.grid(row=0,columnspan=2)

       
            i = 0
            r1=2
            for i in range(len(self.data)):
                c1=0
                for j in range(2):
                    self.entry1 = Entry(self.tab2,width=20,font = "arial 23")
                    self.entry1.grid(row=r1, column=c1)
                    self.entry1.insert(0,self.data[i][j])
                    self.entry1.config(state = "readonly")
                    c1+=1
                r1+=1


            #Financial Secretary
            self.setter_fs=[StringVar(value=name[:2]) for name in self.fs_candidates]
            self.first_two_names_fs=[IntVar(value=0) for _ in self.setter_fs]

            for name,num in zip(self.fs_candidates,self.first_two_names_fs):
                var = num.get()
                self.cur.execute("insert ignore into financial_secretary (name,votes) VALUES(%s,%s)",(name,var))
            
            self.db.commit()
            
            if self.selected_president.get() != "o" or self.selected_financial_secretary.get() != "o":
                    self.cur.execute("INSERT INTO financial_secretary (name, votes) VALUES (%s, %s) ON DUPLICATE KEY UPDATE votes = votes + 1",(self.selected_financial_secretary.get(), 1))
                    self.db.commit()

            self.cur.execute("SELECT name, votes FROM financial_secretary")
            self.voteno_fs = self.cur.fetchall()
            
            if self.voteno_fs:
                self.data_fs = [list(pair) for pair in self.voteno_fs]


            h2=Label(self.tab2,text= "FINANCIAL SECRETARY", font="arial 20 bold")
            h2.grid(row=5,columnspan=2)

            f = 4
            r2=6
            for f in range(len(self.data_fs)):
                c2 = 0
                for j in range(2):
                    self.entry2 = Entry(self.tab2,width=20,font = "arial 23")
                    self.entry2.grid(row=r2, column=c2)
                    self.entry2.insert(0,self.data_fs[f][j])
                    self.entry2.config(state = "readonly")
                    c2+=1
                r2+=1
        view_button = Button(self.tab2,text="View Votes",font = "arial 15",command=view)
        view_button.place(x=270, y=600)
        self.top.mainloop()

   



root = ThemedTk(theme="arc")
app = EntryApp(root)
app.entry()
root.mainloop()

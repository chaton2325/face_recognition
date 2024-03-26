def enregistrer():
    import sqlite3
    import tkinter 
    from tkinter import messagebox
    from fonctions_utiles import hora , capture_photo

    #Fonction pour l'enregistrement
    def enregistre():
        #Récupération de la date actuelle 
        date_actuelle=hora()
        conn1=sqlite3.connect("database.db")
        cur_add=conn1.cursor()
        get_nom=entry_nom.get()
        get_password=entry_pwd.get()
        get_telephone=entry_numero.get()
        requete=f''' INSERT INTO photos("user_name","phone_number","pass_word","date") VALUES("{get_nom}","{get_telephone}","{get_password}","{date_actuelle}")  '''
        cur_add.execute(requete)

        capture_photo(get_nom)
        
        conn1.commit()
        conn1.close()
        messagebox.showinfo(title='Information', message="Ajouté avec succès")
        

    #Définition de la fenetre
    app=tkinter.Tk()
    app.geometry("500x300")
    app.resizable(False,False)
    app.config(bg="white")
    fonts= font=("Calibri",20)

    #Les widgets
    label_enregistrer=tkinter.Label(app , text="Enregistrement"  , font=("Calibri",20))
    label_nom=tkinter.Label(app , text = "Nom d'utilsiateur" , font=("Calibri",20))
    entry_nom=tkinter.Entry(app ,font=("Calibri",20))
    label_pwd=tkinter.Label(app , text="pass_word", font=("Calibri",20))
    entry_pwd=tkinter.Entry(app ,font=("Calibri",20))
    label_numero=tkinter.Label(app , text="Telephone",font=("Calibri",20))
    entry_numero=tkinter.Entry(app , font=("Calibri",20))
    button_valider=tkinter.Button(app,text="enregistrer" , command=enregistre )

    #On place les widgetsn
    label_enregistrer.grid(row=0 , column=0 , columnspan=2 )
    label_nom.grid(row=1 , column=0)
    entry_nom.grid(row=1 , column=1)
    label_pwd.grid(row=2 , column=0)
    entry_pwd.grid(row=2 , column=1)
    label_numero.grid(row=3 , column=0)
    entry_numero.grid(row=3 , column=1)
    button_valider.grid(row=4 , column=1)

    global conn
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS
    photos(idn INTEGER autoincrements PRIMARY KEY, user_name TEXT NOT NULL, phone_number TEXT NOT NULL, pass_word TEXT NOT NULL)            
                
                ''')
    conn.commit()
    conn.close()

    app.mainloop()
                

    # fonction pour enregistrer un nouvel utilisateur

    from tkinter import messagebox
    def register_user(user_name,image_path,phone_number):
        user_name=input("entrez votre nom:")
        image_path=input("entrez le chemin de votre fichier image:")
        phone_number=input("entrez le numero de telephone:")
        pass_word=input("entrez le mot de passe")
        conn=sqlite3.connect('photo_database')
        cur=conn.cursor()
        try:
            cur.execute("INSERT INTO photos(user_name,image_path,phone_number,pass_word)VALUES(?,?,?,?)",(user_name,image_path,phone_number,pass_word))
            messagebox.showinfo (" title=infomartion,message=Enregistrement reussi.")
        except sqlite3.IntegrityError:
            messagebox.showerror("erreur: ce chemin d'image existe deja dans la base de donnees.")
            conn.commit()
            conn.close()
            
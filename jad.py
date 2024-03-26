def ecran(username):
    import tkinter as tk 
    from tkinter import ttk
    import sqlite3

    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    requete=f''' SELECT * FROM photos where "user_name"="{username}" LIMIT 1 '''
    cur.execute(requete)
    list_p=cur.fetchall()
    print(list_p)
    conn.close()

    # Création de la fenetre principale
    root = tk.Tk()
    root.title("Menu des personnes")
    root.geometry("500x300")
    fonts=("Calibri",20)
    root.resizable(False,False) 


    #set des variables
    nom=list_p[0][1]
    tel=list_p[0][2]
    pwd=list_p[0][3]
    date=list_p[0][4]
    
    # Création widgets
    label_nom_=tk.Label(root ,font=fonts , text="Nom" )
    label_afficher_nom=tk.Label(root , font=fonts , text=nom )
    label_telephone=tk.Label(root , font=fonts , text="Telephone")
    label_afficher_tel=tk.Label(root , font=fonts , text=tel)
    label_password=tk.Label(root , font=fonts , text="Mot de passe")
    label_afficher_pwd=tk.Label(root , font=fonts , text=pwd)
    label_date=tk.Label(root , font=fonts , text="Dernière authentification")
    label_afficher_date=tk.Label(root , font=fonts , text=date)

    label_nom_.grid(row=0 , column=0)
    label_afficher_nom.grid(row=0 , column=1)
    label_telephone.grid(row=1 , column=0)
    label_afficher_tel.grid(row=1 , column=1)
    label_password.grid(row=2 , column=0)
    label_afficher_pwd.grid(row=2 , column=1)
    label_date.grid(row=3 , column=0)
    label_afficher_date.grid(row=3 , column=1)


    # Boucle principale
    root.mainloop()
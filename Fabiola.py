import tkinter as tk
from tkinter import messagebox
import sqlite3
from ralph import face_recognition , fen_admin
from benji import enregistrer
from jad import ecran


# Connexion à la base de données
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Création de la table "users" si elle n'existe pas déjà
"""cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,  ²
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')

# Exemple d'insertion d'utilisateurs pour tester
users = [
    ('john_doe', 'password123'),
    ('jane_doe', 'pass456')
]
cursor.executemany("INSERT INTO users (username, password) VALUES (?, ?)", users)"""

# Valider et fermer la connexion
conn.commit()
conn.close()

def register():
    enregistrer()

def face_authentication():
    global auth_choice_window
    face_recognition(auth_choice_window)

def id_authentication(username_entry, password_entry, auth_choice_window):
    global auth_id_window
    username = username_entry.get()
    password = password_entry.get()

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Requête pour vérifier si l'utilisateur existe avec les identifiants donnés
    cursor.execute("SELECT * FROM photos WHERE user_name=? AND pass_word=?", (username, password))
    user = cursor.fetchone()

    if username=="admin" and password=="admin":
        fen_admin(auth_id_window)

    if user:
        messagebox.showinfo("Authentification Réussie", "Vous êtes authentifié avec succès!")
        ecran(username)
    else:
        messagebox.showerror("Erreur d'Authentification", "Nom d'utilisateur ou mot de passe incorrect!")
    


    conn.close()
    auth_choice_window.destroy()

def choose_authentication():
    global auth_choice_window
    global fonts
    

    auth_choice_window = tk.Toplevel(root)
    frame=tk.Frame(auth_choice_window , bg="yellow" , width=200 , height=50)
    frame.grid(row=0 , column=0)
    auth_choice_window.title("Choix d'authentification")
    auth_choice_window.geometry("500x300")  # Définir la taille de la fenêtre

    label = tk.Label(auth_choice_window, text="Choisissez une méthode d'authentification:",font=fonts)
    label.grid(row=1,column=0 , pady=10)

    face_auth_button = tk.Button(auth_choice_window, text="Authentification Faciale", command=face_authentication, font=fonts)
    face_auth_button.grid(row=2 , column=0 , pady=10)

    id_auth_button = tk.Button(auth_choice_window, text="Authentification par Identifiants", command=lambda: auth_id(auth_choice_window) , font=fonts)
    id_auth_button.grid(row=3,column=0 , pady=10 )
    auth_choice_window.config(bg="yellow")   
    

def auth_id(auth_choice_window):
    global fonts
    global auth_id_window

    auth_choice_window.destroy()

    auth_id_window = tk.Toplevel(root)
    auth_id_window.title("Authentification par Identifiants")
    auth_id_window.geometry("500x300")  # Définir la taille de la fenêtre

    username_label = tk.Label(auth_id_window, text="Nom d'utilisateur:",font=fonts)
    username_label.pack()
    
    username_entry = tk.Entry(auth_id_window,font=fonts , bg="gray")
    username_entry.pack()

    password_label = tk.Label(auth_id_window, text="Mot de passe:",font=fonts)
    password_label.pack()
    
    password_entry = tk.Entry(auth_id_window, show="*",font=fonts,bg="gray")
    password_entry.pack()

    authenticate_button = tk.Button(auth_id_window, text="S'authentifier", command=lambda: id_authentication(username_entry, password_entry, auth_choice_window),font=fonts)
    authenticate_button.pack()
    
    auth_id_window.config(bg="yellow")

fonts=("Calibri",20)

root = tk.Tk()
root.title("Authentification")
root.geometry("435x335")  # Définir la taille de la fenêtre principale

label_frame=tk.Frame(root,bg="yellow",width=200,height=92)
label_frame.grid(row=0 , column=0) 

label = tk.Label(root, text="Veuillez choisir une option :",font=fonts)
label.grid(row=1,column=0,columnspan=2,pady=10)

authenticate_button = tk.Button(root, text="S'authentifier", font=fonts ,command=choose_authentication)
authenticate_button.grid(row=2,column=0,padx=10,pady=8)

register_button = tk.Button(root, text="S'enregistrer", font=fonts, command=register)
register_button.grid(row=2,column=1,padx=10,pady=8)
root.config(bg="yellow")
root.resizable(False,False)

root.mainloop()
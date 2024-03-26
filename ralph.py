def face_recognition():
    import face_recognition
    import cv2
    import os
    from tkinter import messagebox 
    from jad import ecran

    #Création d'une variable pour quitter ou conserver la capture vidéo
    recording=True

    list_visages=os.listdir("visages")
    print(list_visages) #On obtient ici la liste des visages du dossier visages
    indice=0 #On crÃ©e l'indice pour la comparaison des visqges dans la liste list_encoding

    #Pour pallier au problème de lenteur , on encode d'abord tout les visages de la base de donnÃ©es
    list_encodig=[] #On crée une liste vide ou on va encoder tout les visages
    for personnes in list_visages:
        image_2 = face_recognition.load_image_file(f"visages\{personnes}")
        face_locations_2 = face_recognition.face_locations(image_2)
        face_encodings_2 = face_recognition.face_encodings(image_2, face_locations_2)[0]
        list_encodig.append(face_encodings_2)
    #print(list_encodig)

    #Chargement du classificateur de visage prÃ©-entrainÃ©
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    #Demarrer la capture video a travaer la webcam
    cap = cv2.VideoCapture(0)
    
    #Création d'une variable pour quitter ou conserver la capture vidéo
    recording=True

    while recording:
        # Capture d'une frame
        ret, frame = cap.read()
        
        # Convertir la frame en niveaux de gris
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # DÃ©tecter les visages dans la frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Dessiner des rectangles autour des visages dÃ©tectÃ©s et enregistrer chaque visage
        for (x, y, w, h) in faces:
            x_new = max(0, x - 20) 
            y_new = max(0, y - 20) 
            w_new = min(frame.shape[1] - x_new, w + 90) 
            h_new = min(frame.shape[0] - y_new, h + 90) 
            # Dessiner un rectangle autour du visage dÃ©tectÃ©
            cv2.rectangle(frame, (x_new, y_new), (x_new+w_new, y_new+h_new), (255, 0, 0), 2)
            
            # Extraire le visage de la frame
            face = frame[y_new:y_new+h_new, x_new:x_new+w_new]
            
            # Enregistrer le visage extrait au format JPG
            face_name = "actual_face.jpg"
            cv2.imwrite(face_name, face)
            #print(f"Visage enregistrÃ© sous : {face_name}")

            # Afficher la frame avec les visages dÃ©tectÃ©s
            cv2.imshow('Face Detection', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                recording=False

            if cv2.waitKey(1) & 0xFF == ord('s'):
                for visages in list_visages:
                    list_nom=[]
                    #On charger les images
                    image_1 = face_recognition.load_image_file("actual_face.jpg")

                    #On cherche la position des visages
                    face_locations_1 = face_recognition.face_locations(image_1)

                    #on encode les faces
                    face_encodings_1 = face_recognition.face_encodings(image_1, face_locations_1)[0]

                    #on traite maintenant les deux images et on stoque dans rÃ©sultat (une liste boolÃ©enne)
                    resultat = face_recognition.compare_faces([face_encodings_1], list_encodig[indice])
                    #print(resultat)
                    indice +=1 #On incrÃ©mente l'indice

                    if resultat[0] ==True:
                        #print(visages)

                        #Pour pallier au problème d'affichage d'extension dans le nom après l'authentification faciale
                        for lettre in visages:
                            list_nom.append(lettre)
                        print("Voici la list_Nom",list_nom)
                        
                        #On supprime les 3 éléments qui composent l'extension du  fichier
                        list_nom.pop(-1) #g
                        list_nom.pop(-1) #p
                        list_nom.pop(-1) #j
                        list_nom.pop(-1) #.
                        nom="".join(list_nom)
                        
                        

                        nom_texte=visages
                        cv2.putText(frame, nom_texte, (x_new, y_new-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                        messagebox.showinfo(title="Visage détecté",message=f"C'est le visage de {nom}\nBievenue Mr/Mme {nom}")
                        indice=0 #On renvoie la valeur a 0 si un visage est dÃ©tectÃ©
                        recording=False
                        break
                    else:
                        pass


            
        
    # LibÃ©rer la capture vidÃ©o et fermer les fenÃªtres
    cap.release()
    cv2.destroyAllWindows()
    ecran(nom) #On appelle maintenant la fonction de jad pour ouvrir la fenetre


#Fonction pour la fenetre administrateur 
def fen_admin(auth_id_window):
    #Fonction pour le clic d'une listbox 
    import sqlite3
    import tkinter
    import subprocess 

    def afficher_selection(event):
        selected_index = listbox_produits.curselection()
        if selected_index:
            selected_item = listbox_produits.get(selected_index[0])
            selected_nom, selected_tel, selected_date  = selected_item
            nom_var.set(selected_nom)
            tel_var.set(selected_tel)
            date_var.set(selected_date)

            #Maintenant on traite l'affichage de l'image(ouvrir avec subprocess)
            subprocess.run(["start", f"visages\{nom_var.get()}.jpg"], shell=True) #Spécifique a windows


    #Fonction pour la recherche de produits
    def search_in_listbox(event):
        import tkinter
        query = entry_search_products.get().lower()
        listbox_produits.delete(0, tkinter.END)
        for item in list_produits_créer:
            stringified_tuple = tuple(str(it) for it in item)
            if any(query in element.lower() for element in stringified_tuple):
                listbox_produits.insert(tkinter.END, item)


    import sqlite3
    import tkinter
    connect=sqlite3.connect("database.db")
    cur_list_produits=connect.cursor()
    cur_list_produits.execute('''SELECT "user_name" , "phone_number" , "date" FROM photos;''')
    list_produits_créer=cur_list_produits.fetchall()


    modify_products=tkinter.Toplevel(auth_id_window)
    modify_products.config(bg="gray")
    entry_color="#FFE3EE"
    fonts=("Calibri",13)


    #Variables associés a ce qui va s'afficher dans les zones d'entrées
    nom_var=tkinter.StringVar()
    tel_var=tkinter.StringVar()
    date_var=tkinter.StringVar()


    #Les Labels frame
    label_frame_part=tkinter.LabelFrame(modify_products,text="Attributs des utilisateurs")
    label_frame_modify_products=tkinter.LabelFrame(modify_products,text="Liste des utilisateurs")
    label_frame_photo=tkinter.LabelFrame(modify_products , text="Photo" , bg="yellow")

    #Les widgets label_frame__modify_products
    scrollbar_list_products=tkinter.Scrollbar(label_frame_modify_products)
    label_list_produits_creer=tkinter.Label(label_frame_modify_products,font=("Calibri",30),bg="pink",text="Liste des utilisateurs")
    listbox_produits=tkinter.Listbox(label_frame_modify_products,bg="pink",font=fonts,width=55,height=10,yscrollcommand=scrollbar_list_products.set)
    entry_search_products=tkinter.Entry(label_frame_modify_products,font=fonts,width=30,bg=entry_color)

    #Les widgets label_frame_part
    label_nom=tkinter.Label(label_frame_part,font=fonts,bg="blue",text="Nom ")
    entry_nom=tkinter.Entry(label_frame_part,font=fonts,textvariable=nom_var,bg=entry_color)
    label_tel=tkinter.Label(label_frame_part,font=fonts,bg="blue",text="Telephone")
    entry_tel=tkinter.Entry(label_frame_part,font=fonts,textvariable=tel_var,bg=entry_color)
    label_date=tkinter.Label(label_frame_part , font=fonts , text="Dernière vue", bg="blue")
    entry_date=tkinter.Label(label_frame_part , font=fonts ,textvariable=date_var , bg=entry_color)

    #Les widgets label_frame_photo
    bouton_img=tkinter.Label(label_frame_photo , width=35 , height=10)






    #On insère les éléments dans la listbox
    for i in list_produits_créer:
        listbox_produits.insert(tkinter.END,i)




    #On place les widgets label_frame_modify_products
    label_frame_modify_products.grid(row=0,column=0,padx=10,pady=10 , rowspan=2)
    scrollbar_list_products.pack(side=tkinter.RIGHT,fill=tkinter.Y)
    label_list_produits_creer.pack()
    entry_search_products.pack()
    listbox_produits.pack()



    #On place les widgets label_frame_part
    label_frame_part.grid(row=0,column=1,padx=7,pady=6)
    label_nom.grid(row=0,column=0,padx=7,pady=6)
    entry_nom.grid(row=0,column=1,padx=7,pady=6)
    label_tel.grid(row=1,column=0,padx=7,pady=6)
    entry_tel.grid(row=1,column=1,padx=7,pady=6)
    label_date.grid(row=2,column=0,padx=7,pady=6)
    entry_date.grid(row=2,column=1,padx=7,pady=6)

    #On place les widgets label_frame_photo
    label_frame_photo.grid(row=1 , column=1)
    bouton_img.pack()


    #Configuration de scrollbar
    scrollbar_list_products.config(command=listbox_produits.yview)

    #Les bind
    listbox_produits.bind("<ButtonRelease-1>", afficher_selection)
    entry_search_products.bind("<KeyRelease>", search_in_listbox)




    #Boucle principale
    modify_products.mainloop()
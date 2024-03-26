#Fonction pour avoir la date et l'heure actuelle selon la pile de l'ordinateur ( By ralph)
def hora():
    import datetime
    maintenant = datetime.datetime.now()
    format_personnalise = "%Y-%m-%d %H:%M:%S"
    date_formatee = maintenant.strftime(format_personnalise)
    return date_formatee


# Fonction pour capturer une photo (By Ralph)
def capture_photo(get_nom):
    import cv2
    # Capture vidéo à partir de la caméra (index 0 pour la première caméra)
    capture = cv2.VideoCapture(0)
    
    while True:
        # Lecture d'une image de la capture vidéo
        ret, frame = capture.read()

        # Afficher l'image en continu
        cv2.imshow('Appuyez sur la touche Entrée pour prendre la photo', frame)

        # Attendre que l'utilisateur appuie sur la touche Entrée
        if cv2.waitKey(1) == 13:  # 13 correspond à la touche Entrée
            # Enregistrer l'image capturée au format JPG
            cv2.imwrite(f"visages\{get_nom}.jpg", frame)
            break  # Sortir de la boucle une fois la photo prise

    # Libérer la capture vidéo
    capture.release()
    # Fermer toutes les fenêtres d'affichage
    cv2.destroyAllWindows()
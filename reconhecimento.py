import face_recognition
import cv2

# Carregar uma imagem de exemplo e aprender a reconhecer
imagem_conhecida = face_recognition.load_image_file("gustavao.jpg")
imagem_conhecida2 = face_recognition.load_image_file("henrique_baitola.jpg")
imagem_conhecida3 = face_recognition.load_image_file("pimenis.jpg")
encodings_conhecidos = [face_recognition.face_encodings(imagem_conhecida)[0],face_recognition.face_encodings(imagem_conhecida2)[0],face_recognition.face_encodings(imagem_conhecida3)[0]]
nomes = ["Gustavo", "Priquitin","Pimenis"]
# Inicializar a webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capturar um único frame de vídeo
    ret, frame = video_capture.read()

    # Encontrar todas as faces e encodings de face no frame atual do vídeo
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop através de cada face encontrada no frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Ver se a face é uma correspondência para a face conhecida
        matches = face_recognition.compare_faces(encodings_conhecidos, face_encoding)

        nome = "Desconhecido"
        color = (0, 0, 255)
        if True in matches:
            indice_match = matches.index(True)
            nome = nomes[indice_match]
            color = (34, 139, 34)
        # Desenhar um retângulo ao redor do rosto e escrever o nome
        cv2.rectangle(frame, (left, top), (right, bottom), color , 2)
        cv2.putText(frame, nome, (left, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    # Mostrar o resultado
    cv2.imshow('Video', frame)

    # Sair do loop com 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
import face_recognition
import cv2

# Carregar uma imagem de exemplo e aprender a reconhecer
imagem_conhecida = face_recognition.load_image_file("img1.jpg")
imagem_conhecida2 = face_recognition.load_image_file("img2.jpg")
imagem_conhecida3 = face_recognition.load_image_file("img3.jpg")
encodings_conhecidos = [face_recognition.face_encodings(imagem_conhecida)[0],face_recognition.face_encodings(imagem_conhecida2)[0],face_recognition.face_encodings(imagem_conhecida3)[0]]
nomes = ["Gustavo", "Henrique","Andre"]
# Inicializar a webcam
imagemAAnalizar = cv2.imread("teste do baguio.jpg");


    

    # Encontrar todas as faces e encodings de face no frame atual do vídeo
face_locations = face_recognition.face_locations(imagemAAnalizar)
face_encodings = face_recognition.face_encodings(imagemAAnalizar, face_locations)

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
    cv2.rectangle(imagemAAnalizar, (left, top), (right, bottom), color , 2)
    cv2.putText(imagemAAnalizar, nome, (left, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    # Mostrar o resultado
cv2.imshow('Imagem', imagemAAnalizar)

    # Sair do loop com 'q'
cv2.waitKey(0)

cv2.destroyAllWindows()
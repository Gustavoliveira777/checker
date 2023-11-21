import face_recognition
import cv2
import numpy as np
import base64

def roomValidate(imageRoomPIL, beneficiariesFaceImgPathArray=[]):

    # Carrega as imagens 
    imagem_conhecida = face_recognition.load_image_file("C:\\Users\\olive\\OneDrive\\Documentos\\Projetos\\checker\\images\\peoples\\gustavao.jpg")
    imagem_conhecida2 = face_recognition.load_image_file("C:\\Users\\olive\\OneDrive\\Documentos\\Projetos\\checker\\images\\peoples\\henrique_baitola.jpg")
    imagem_conhecida3 = face_recognition.load_image_file("C:\\Users\\olive\\OneDrive\\Documentos\\Projetos\\checker\\images\\peoples\\pimenis.jpg")
    encodings_conhecidos = [face_recognition.face_encodings(imagem_conhecida)[0],face_recognition.face_encodings(imagem_conhecida2)[0],face_recognition.face_encodings(imagem_conhecida3)[0]]
    nomes = ["Gustavo", "Henrique","Andre"]
    
    # Transforma a imagem da sala recebida da API e transformada em PIL para o formato NumPY para compreensão do OpenCV
    np_imageRoom = np.array(imageRoomPIL)
    imagemAAnalizar = cv2.cvtColor(np_imageRoom, cv2.COLOR_RGB2BGR)

    # Encontrar todas as faces na imagem
    face_locations = face_recognition.face_locations(imagemAAnalizar)
    face_encodings = face_recognition.face_encodings(imagemAAnalizar, face_locations)
    
    # Array das faces encontrdas para devolver resultado
    founds = []

    # Percorre a imagem pra identificar 
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Verifica se a face é uma correspondência para a face conhecida
        matches = face_recognition.compare_faces(encodings_conhecidos, face_encoding)

        nome = "Desconhecido"
        color = (0, 0, 255) #Pinta o quadrado de vermelho para Desconhecido
        #Guarda as pessoas encontradas
        if True in matches:
            indice_match = matches.index(True)
            nome = nomes[indice_match]
            color = (34, 139, 34) #Pinta o quadrado de verde pra Identificados
            founds.append(nome)

        # Desenha um retângulo ao redor do rosto e escrever o nome
        cv2.rectangle(imagemAAnalizar, (left, top), (right, bottom), color , 2)
        cv2.putText(imagemAAnalizar, nome, (left, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    # Converte a imagem resultado em array NumPY
    _, npyarrImgResult = cv2.imencode('.jpg', imagemAAnalizar)
    # Converte o array para bytes
    imgResultBytes = npyarrImgResult.tobytes()
    # Converte os Bytes para base64
    imgResultBase64 = base64.b64encode(imgResultBytes)
    # Constroi dicionário de body de response
    response = {'peoplesMatches':founds,'conferenceImage':imgResultBase64.decode('utf-8')}
    print(f'Resposta do processamento: {response}')
    return response
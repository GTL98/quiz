# 1. Importar as bibliotecas
import cv2
import csv
import time
import cvzone
from cvzone.HandTrackingModule import HandDetector
from questao_multipla_escolha import QuestaoMultiplaEscolha

# 2. Carregar o módulo de detecção
detector = HandDetector(maxHands=1, detectionCon=0.8, minTrackCon=0.8)

# 3. Importar o arquivo .cvs
caminho_csv = 'perguntas_quiz.cvs'
with open(caminho_csv, newline='\n', encoding='utf-8') as doc:
    leitor = csv.reader(doc)
    questoes = list(leitor)[1:]
num_questao = 0
quantidade_questao = len(questoes)

# 4. Passar cada pergunta para o módulo QuestaoMultiplaEscolha
lista_questao_multipla_escolha = []
for questao in questoes:
    lista_questao_multipla_escolha.append(QuestaoMultiplaEscolha(questao))

# 5. Definir o tamanho da tela
largura_tela = 1280
altura_tela = 720

# 6. Captura de vídeo
cap = cv2.VideoCapture(0)
cap.set(3, largura_tela)
cap.set(4, altura_tela)

while True:
    # Detectar as mãos
    _, imagem = cap.read()
    imagem = cv2.flip(imagem, 1)
    maos, imagem = detector.findHands(imagem, flipType=False)
    
    if num_questao < quantidade_questao:
        # Mostrar a pergunta na tela
        pergunta = lista_questao_multipla_escolha[num_questao]

        # Mostrar as respostas na tela
        imagem, caixa_delimitadora = cvzone.putTextRect(imagem, pergunta.questao, [100, 100], 2, 2, offset=50, border=5)
        imagem, caixa_delimitadora_1 = cvzone.putTextRect(imagem, pergunta.alternativa_1,
                                                          [100, 250], 2, 2, offset=50, border=5)
        imagem, caixa_delimitadora_2 = cvzone.putTextRect(imagem, pergunta.alternativa_2,
                                                          [400, 250], 2, 2, offset=50, border=5)
        imagem, caixa_delimitadora_3 = cvzone.putTextRect(imagem, pergunta.alternativa_3,
                                                         [100, 400], 2, 2, offset=50, border=5)
        imagem, caixa_delimitadora_4 = cvzone.putTextRect(imagem, pergunta.alternativa_4,
                                                         [400, 400], 2, 2, offset=50, border=5)

        # Extrair as informações das mãos
        if maos:
            lista_landmark = maos[0]['lmList']
            cursor = lista_landmark[8]  # ponta do dedo indicador
            # Descobrir a distância entre a ponta do dedo indicador com a ponta do dedo médio
            comprimento, info = detector.findDistance(lista_landmark[8], lista_landmark[12])
            if comprimento < 35:
                pergunta.atualizar(cursor, [caixa_delimitadora_1, caixa_delimitadora_2,
                                            caixa_delimitadora_3, caixa_delimitadora_4], imagem)
                if pergunta.resposta_usuario is not None:
                    num_questao += 1
                    time.sleep(0.3)
                    
    else:
        pontuacao = 0
        for pergunta in lista_questao_multipla_escolha:
            if pergunta.resposta == pergunta.resposta_usuario:
                pontuacao += 1
        pontuacao = round((pontuacao / quantidade_questao) * 100, 2)
        imagem, _ = cvzone.putTextRect(imagem, 'Quiz Completo', [250, 300], 2, 2, offset=50, border=5)
        imagem, _ = cvzone.putTextRect(imagem, f'Acerto: {pontuacao}%', [700, 300], 2, 2, offset=50, border=5)
        
    # Desenhar a barra de progresso
    barra_valor = 150 + (950 // quantidade_questao) * num_questao
    cv2.rectangle(imagem, (150, 600), (barra_valor, 650), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(imagem, (150, 600), (1100, 650), (255, 0, 255), 5)
    
    # Escrever a porcentagem da barra
    imagem, _ = cvzone.putTextRect(imagem, f'{round((num_questao/quantidade_questao)*100)}%', [1130, 635], 2, 2, offset=16)
    
    # Mostrar imagem na tela
    cv2.imshow('Quiz', imagem)
    
    # Terminar o loop
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
        
# 7. Fechar a tela de captura
cap.release()
cv2.destroyAllWindows()
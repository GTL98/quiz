import cv2


class QuestaoMultiplaEscolha:
    def __init__(self, dados):
        self.questao = dados[0]
        self.alternativa_1 = dados[1]
        self.alternativa_2 = dados[2]
        self.alternativa_3 = dados[3]
        self.alternativa_4 = dados[4]
        self.resposta = int(dados[5])
        self.resposta_usuario = None
        
    def atualizar(self, cursor, caixas_delimitadoras, imagem):
        for x, caixa_delimitadora in enumerate(caixas_delimitadoras):
            x1, y1, x2, y2 = caixa_delimitadora
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.resposta_usuario = x+1
                cv2.rectangle(imagem, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)
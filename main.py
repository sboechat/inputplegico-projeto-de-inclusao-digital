import cv2
import mediapipe as mp
import speech_recognition as sr
import pyautogui
from threading import Thread

pyautogui.FAILSAFE = False
class Actions(Thread):
    def __init__ (self):
        Thread.__init__(self)
        self.bocaSup = 0
        self.bocaInf = 10
        self.pos_y_sobrancelha = 0
        self.pos_y_olho = 0
        self.tela_x = screen_w
        self.tela_y = screen_h
        self.last_screen_x = screen_w / 2
        self.last_screen_y = screen_h / 2
        self.screen_x = screen_w / 2
        self.screen_y = screen_h / 2
        self.frame_pos_x = self.screen_x
        self.frame_pos_y = self.screen_y
        self.ativar_mic = 45

    def conf(self):
        repeticoes = 200
        print("ATENÇÃO: RECONFIGURAR AO MUDAR O USUÁRIO OU A DISTÂNCIA ENTRE O USUÁRIO E O APARELHO")
        print("Levante a sobrancelha e abra a boca")
        for i in range(repeticoes):
            main(self)
            self.ativar_mic = self.pos_y_olho - self.pos_y_sobrancelha
            self.click_value = self.bocaSup - self.bocaInf
        print("p2 " + str(self.ativar_mic) + " ; "+str(self.click_value))
        print("OK!")
        print("Olhe para cima /\\")
        cima = 0
        for i in range(repeticoes):
            main(self)
            cima =  self.frame_pos_y
        
        print("Olhe para baixo \\/")
        baixo = 0
        for i in range(repeticoes):
            main(self)
            baixo =  self.frame_pos_y

        print("Olhe para direita >")
        direita = 0
        for i in range(repeticoes):
            main(self)
            direita = self.frame_pos_x

        print("Olhe para esquerda <")
        esquerda = 0
        for i in range(repeticoes):
            main(self)
            esquerda = self.frame_pos_x

        self.tela_x = direita - esquerda
        self.tela_y = baixo - cima
        print(baixo, cima, direita, esquerda, self.tela_x, self.tela_y, cam.frame_w, cam.frame_h)
    def run(self):
        self.conf()
        while(True):
            try:
                # if self.screen_x <= 0:
                #     self.screen_x = 0.5
                # elif self.screen_x >= screen_w:
                #     self.screen_x = screen_w-0.5

                # if self.screen_y <= 0:
                #     self.screen_y = 0.5
                # elif self.screen_y >= screen_h:
                #     self.screen_y = screen_h -0.5

                if abs(self.last_screen_x - self.screen_x) > screen_w*0.005:
                    pyautogui.moveTo(self.screen_x, self.last_screen_y)
                    self.last_screen_x = self.screen_x
                if abs(self.last_screen_y - self.screen_y) > screen_h*0.005:
                    pyautogui.moveTo(self.last_screen_x, self.screen_y)
                    self.last_screen_y = self.screen_y
            except:
                print("except pyautogui")

            if (self.bocaSup - self.bocaInf) > self.click_value:
                pyautogui.click()
                print('CLICK')
                pyautogui.sleep(0.5)
                print(self.bocaSup,self.bocaInf, self.bocaSup - self.bocaInf)    

            if (self.pos_y_olho - self.pos_y_sobrancelha) > self.ativar_mic:
                print(self.pos_y_olho - self.pos_y_sobrancelha)
                try:
                    with sr.Microphone() as mic:
                        rec = sr.Recognizer()
                        rec.adjust_for_ambient_noise(mic)
                        print("Fala aí patrão")
                        audio = rec.listen(mic)
                        texto = rec.recognize_google(audio, language="pt-BR")
                        print(texto)
                        if texto == "apagar":
                            pyautogui.press('backspace')
                        elif texto == "apagar tudo":
                            pyautogui.press('backspace', presses=150)
                        elif texto == "confirmar":
                            pyautogui.press('enter')
                        else:
                            pyautogui.write(texto) 
                except Exception as e:
                    print("except mic", e)


# LEFT_IRIS = [474, 475, 476, 477]
# RIGHT_IRIS = [469,470,471,472]

webcam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
pos_x = 0
pos_y = 0
screen_w, screen_h = pyautogui.size()

class Cam(Thread):
    def __init__ (self):
        Thread.__init__(self)
        self.ret, self.frame = webcam.read()
        self.frame = cv2.flip(self.frame, 1)
        self.rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.face_mesh = face_mesh.process(self.rgb_frame)
        self.landmark_points = self.face_mesh.multi_face_landmarks
        self.frame_h, self.frame_w, _ = self.frame.shape
        self.ativado = True

    def run(self):
        while(self.ativado):
            _, frameInvertido = webcam.read()
            self.frame = cv2.flip(frameInvertido, 1)
            self.rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.face_mesh = face_mesh.process(self.rgb_frame)
            self.landmark_points = self.face_mesh.multi_face_landmarks
            self.frame_h, self.frame_w, _ = self.frame.shape

    def stop(self):
        self.run = False
cam = Cam()
cam.start()

def main(act):
    
    if cam.landmark_points:
        landmarks = cam.landmark_points[0].landmark
        nariz = cam.landmark_points[0].landmark[1]
        sobrancelha = cam.landmark_points[0].landmark[295]
        olho = cam.landmark_points[0].landmark[253]

        pos_x_sobrancelha = int(sobrancelha.x * cam.frame_w)
        pos_y_sobrancelha = int(sobrancelha.y * cam.frame_h)
        cv2.circle(cam.frame, (pos_x_sobrancelha, pos_y_sobrancelha), 3, (0, 0, 0))
        act.pos_y_sobrancelha = pos_y_sobrancelha

        pos_x_olho = int(olho.x * cam.frame_w)
        pos_y_olho = int(olho.y * cam.frame_h)
        cv2.circle(cam.frame, (pos_x_olho, pos_y_olho), 3, (0, 0, 0))
        act.pos_y_olho = pos_y_olho

        pos_x = int(nariz.x * cam.frame_w)
        pos_y = int(nariz.y * cam.frame_h)
        cv2.circle(cam.frame, (pos_x, pos_y), 3, (0, 255, 0))

        act.frame_pos_x = pos_x
        act.frame_pos_y = pos_y

        act.screen_x = ((screen_w / act.tela_x) * (pos_x - ((cam.frame_w - act.tela_x) / 2)))
        act.screen_y = ((screen_h / act.tela_y) * (pos_y - ((cam.frame_h - act.tela_y) / 2)))

        # aux = screen_w / cam.frame_w * pos_x
        # act.screen_x = aux - (screen_w*0.3)

        # act.screen_y = screen_h / cam.frame_h * pos_y
        # aux = screen_h / cam.frame_h * pos_y
        # act.screen_y = aux - (screen_h*0.3)

        boca = [landmarks[14], landmarks[13]]
        for landmark in boca:
            x = int(landmark.x * cam.frame_w)
            y = int(landmark.y * cam.frame_h)
            cv2.circle(cam.frame, (x, y), 3, (255, 0, 0))
        
        act.bocaSup = boca[0].y
        act.bocaInf = boca[1].y

    cv2.imshow("Mouseplegico", cam.frame)
    cv2.waitKey(1)

actions = Actions()
actions.start()

while True:
    main(actions)
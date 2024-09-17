#https://medium.com/@hektorprofe/primeros-pasos-en-pyqt-5-y-qt-designer-programas-gr%C3%A1ficos-con-python-6161fba46060
#PyQt5

import uvicorn.config
from plantilla_ui import *
from python_event_bus import EventBus
import mainWS
import uvicorn
from threading import Thread
import signal
from python_event_bus import EventBus

signal.signal(signal.SIGINT, signal.SIG_DFL)  ## Cancela la ejecucion con Ctrl C

window = None

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self) 
        self.label.setText("Haz clic en el botón")
        self.pushButton.setText("Presióname")
        #Conectamos los eventos con sus acciones:
        self.pushButton.clicked.connect(self.actualizar)    
        
    def actualizar(self):
        self.label.setText("¡Acabas de hacer clic en el botón!")
        EventBus.call("QT5_say", "Precionaste el boton en QT5")

@EventBus.on("websocket_say")  ##Un decorador nunca va dentro de la funcion, va en la cabecera de esta
def WSConnect(message): ##Funcion que recibe el evento
    global window
    window.label.setText(message)

def run_api():
    config = uvicorn.Config(mainWS.app, host="127.0.0.1", port=8000)
    server = uvicorn.Server(config)
    server.run()
    
def run_QT5():
    global window
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    apiThread = Thread(target = run_api)
 #   QT5Thread = Thread(target = run_QT5)
    apiThread.start()
    run_QT5()
  #  QT5Thread.start()
    apiThread.join()
   # QT5Thread.join()
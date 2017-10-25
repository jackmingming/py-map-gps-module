from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
import functools
from threading import Thread
import json
import sys
import server

class fox(QtGui.QWidget):
    def __init__(self):
        super(fox, self).__init__()
        self.init_server()
        self.setupUI()
        self.show()
        self.raise_()

    def init_server(self):
        server_thread = Thread(target=server.run_server)
        server_thread.daemon = True
        server_thread.start()

    def setupUI(self):
        # self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setFixedSize(800, 500)
        self._set_appIcon()
        self.setWindowTitle('Fox')

        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

        view = self.view = QtWebKit.QWebView()
        cache = QtNetwork.QNetworkDiskCache()
        cache.setCacheDirectory("cache")
        view.page().networkAccessManager().setCache(cache)
        view.page().networkAccessManager()
        view.page().mainFrame().addToJavaScriptWindowObject("MainWindow", self)
        view.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        view.load(QtCore.QUrl('http://localhost:3000'))
        view.loadFinished.connect(self._onLoadFinished)
        view.linkClicked.connect(QtGui.QDesktopServices.openUrl)
        
        self.vbox.addWidget(view)
        self.vbox.setContentsMargins(0,0,0,0)

    def _onLoadFinished(self):
        print 'loaded!'

    @QtCore.pyqtSlot(float, float)
    def onMapMove(self, lat, lng):
        # self.label.setText('Lng: {:.5f}, Lat: {:.5f}'.format(lng, lat))  
        self.position_lat = lat
        self.position_lon = lng     

    def _set_appIcon(self):
        app_icon = QtGui.QIcon()
        app_icon.addFile('assets/icons/app_icons/fox_16.png', QtCore.QSize(16,16))
        app_icon.addFile('assets/icons/app_icons/fox_24.png', QtCore.QSize(24,24))
        app_icon.addFile('assets/icons/app_icons/fox_32.png', QtCore.QSize(32,32))
        app_icon.addFile('assets/icons/app_icons/fox_64.png', QtCore.QSize(64,64))
        app_icon.addFile('assets/icons/app_icons/fox_128.png', QtCore.QSize(128,128))
        app_icon.addFile('assets/icons/app_icons/fox_256.png', QtCore.QSize(256,256))
        app_icon.addFile('assets/icons/app_icons/fox_512.png', QtCore.QSize(521,512))
        app.setWindowIcon(app_icon)
              
    def close_app(self):
        sys.exit()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    w = fox()
    app.exec_()
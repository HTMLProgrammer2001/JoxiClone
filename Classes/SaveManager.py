from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication
from PyQt5.QtGui import QClipboard
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl

from json import loads
import requests


class SaveManager:
	manager = QNetworkAccessManager()

	def __init__(self, app):
		self.app = app
		self.manager.finished.connect(self.saveServerFinished)

	def save(self, image):
        # save file on disk
		path = QFileDialog().getSaveFileName(self.app, 'Save image', '', '*.jpg')
		image.save(path[0])

	def saveBuffer(self, image):
		cb: QClipboard = QApplication.clipboard()
		cb.setImage(image, mode=cb.Clipboard)

		QMessageBox.information(self.app, 'Copy', 'Image copied to buffer')

	def saveServer(self, image):
		name = 'tmp.png'
		url = 'https://joxi-server.herokuapp.com/save'

        # save file on disk
		image.save(f"./{name}")

		with open(f"./{name}", 'rb') as img:
			files = {'image': (name, img, 'multipart/form-data', {'Expires': '0'})}

			with requests.Session() as s:
				# create pyqt QNetworkRequest from requests module
				r = s.post(url, files=files)
				request = r.request
				request.prepare(method="POST", url=url)

				request_qt = QNetworkRequest(QUrl(url))

				for header, value in request.headers.items():
					request_qt.setRawHeader(bytes(header, encoding="utf-8"),
											bytes(value, encoding="utf-8"))

				# set handlers
				self.manager = QNetworkAccessManager()
				self.manager.finished.connect(self.saveServerFinished)
				self.manager.post(request_qt, request.body)

	def saveServerFinished(self, reply: QNetworkReply):
		# if error on server occured
		if reply.error():
			QMessageBox.critical(self.app, 'Query error', reply.errorString())
			return

		try:
			data = loads(bytes(reply.readAll()))
			QMessageBox.information(self.app, 'Success query', data['message'])
		except Exception as e:
			QMessageBox.critical(self.app, 'Query error', 'Error in parsing')
			print(e)
			return

		# save path to clipboard
		cb: QClipboard = QApplication.clipboard()
		cb.setText(data['path'], mode=cb.Clipboard)

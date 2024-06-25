import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QInputDialog, QLineEdit
from encryption_utils import generate_key, encrypt_file, decrypt_file

class FileTransferApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.key = None

    def initUI(self):
        self.setWindowTitle('Secure File Transfer')
        layout = QVBoxLayout()

        self.label = QLabel('No file selected.')
        layout.addWidget(self.label)

        select_file_button = QPushButton('Select File')
        select_file_button.clicked.connect(self.select_file)
        layout.addWidget(select_file_button)

        encrypt_button = QPushButton('Transfer File Securely')
        encrypt_button.clicked.connect(self.encrypt_file)
        layout.addWidget(encrypt_button)

        decrypt_button = QPushButton('Decrypt File')
        decrypt_button.clicked.connect(self.decrypt_file)
        layout.addWidget(decrypt_button)

        self.setLayout(layout)
        self.show()

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.file_path = file_path
            self.label.setText(f'Selected file: {file_path}')

    def encrypt_file(self):
        if not hasattr(self, 'file_path'):
            self.label.setText('Please select a file first.')
            return
        
        if not self.key:
            password, ok = QInputDialog.getText(self, 'Password', 'Enter your password:', QLineEdit.Password)
            if ok and password:
                self.key = generate_key(password.encode())
            else:
                self.label.setText('Password not entered.')
                return
        
        try:
            encrypt_file(self.file_path, self.key)
            print(f'File {self.file_path} securely encrypted.')
            
        except Exception as e:
            print(f'Error: {str(e)}')

    def decrypt_file(self):
        if not hasattr(self, 'file_path'):
            self.label.setText('Please select a file first.')
            return
        
        if not self.key:
            password, ok = QInputDialog.getText(self, 'Password', 'Enter your password:', QLineEdit.Password)
            if ok and password:
                self.key = generate_key(password.encode())
            else:
                self.label.setText('Password not entered.')
                return
        
        try:
            decrypt_file(self.file_path, self.key)  # Pass the original file path without .enc
            print(f'File {self.file_path} securely decrypted.')
            
        except Exception as e:
            print(f'Error: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileTransferApp()
    sys.exit(app.exec_())

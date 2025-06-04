"""
Utilitaires pour la communication série dans l'application Moniteur CAN
"""
import serial
import serial.tools.list_ports
from PyQt6.QtCore import QThread, pyqtSignal

class SerialReaderThread(QThread):
    """Thread pour lire les données du port série sans bloquer l'interface utilisateur."""
    data_received = pyqtSignal(str)
    
    def __init__(self, serial_port=None):
        super().__init__()
        self.serial_port = serial_port
        self.running = False
        
    def set_serial_port(self, serial_port):
        self.serial_port = serial_port
        
    def run(self):
        self.running = True
        while self.running and self.serial_port:
            try:
                if self.serial_port.in_waiting:
                    data = self.serial_port.readline().decode('utf-8', errors='replace')
                    self.data_received.emit(data)
            except Exception as e:
                self.data_received.emit(f"Erreur de lecture: {str(e)}\n")
                self.running = False
            self.msleep(10)  # Petit délai pour éviter de surcharger le CPU
                
    def stop(self):
        self.running = False
        self.wait()


def get_available_ports():
    """Retourne la liste des ports série disponibles.
    
    Returns:
        list: Liste des ports série disponibles
    """
    return [port.device for port in serial.tools.list_ports.comports()]


def open_serial_port(port_name, baud_rate):
    """Ouvre un port série avec les paramètres spécifiés.
    
    Args:
        port_name (str): Nom du port série
        baud_rate (int): Vitesse de communication
        
    Returns:
        tuple: (port série, message) ou (None, message d'erreur)
    """
    try:
        port = serial.Serial(port_name, int(baud_rate), timeout=0.1)
        return port, f"Connecté au port {port_name}"
    except Exception as e:
        return None, f"Erreur de connexion: {str(e)}"


def parse_can_frame(frame_text):
    """Parse une trame CAN depuis le texte reçu.
    
    Args:
        frame_text (str): Texte de la trame CAN
        
    Returns:
        dict: Informations de la trame CAN (id, data, timestamp)
            ou None si le format n'est pas valide
    """
    try:
        # Format typique: "123#DEADBEEF" ou "ID:123 DATA:DEADBEEF"
        if '#' in frame_text:
            parts = frame_text.strip().split('#')
            if len(parts) == 2:
                return {
                    'id': parts[0].strip(),
                    'data': parts[1].strip(),
                    'timestamp': '',  # À remplir par l'appelant
                }
        elif 'ID:' in frame_text and 'DATA:' in frame_text:
            id_part = frame_text.split('ID:')[1].split()[0].strip()
            data_part = frame_text.split('DATA:')[1].strip()
            return {
                'id': id_part,
                'data': data_part,
                'timestamp': '',  # À remplir par l'appelant
            }
    except Exception:
        pass
    
    return None

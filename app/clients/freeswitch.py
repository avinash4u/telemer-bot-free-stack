import socket
import threading
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class FreeSWITCHClient:
    def __init__(self):
        self.host = settings.fs_esl_host
        self.port = settings.fs_esl_port
        self.password = settings.fs_esl_password
        self.socket = None
        self.connected = False
        
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            
            # Authenticate
            auth_msg = f"auth {self.password}\n\n"
            self.socket.send(auth_msg.encode())
            
            # Subscribe to events
            sub_msg = "event plain ALL\n\n"
            self.socket.send(sub_msg.encode())
            
            self.connected = True
            logger.info(f"Connected to FreeSWITCH ESL at {self.host}:{self.port}")
            
            # Start event listener thread
            threading.Thread(target=self._listen_for_events, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Failed to connect to FreeSWITCH: {e}")
            
    def _listen_for_events(self):
        buffer = ""
        while self.connected:
            try:
                data = self.socket.recv(4096).decode()
                if not data:
                    break
                    
                buffer += data
                while '\n\n' in buffer:
                    event_data, buffer = buffer.split('\n\n', 1)
                    self._handle_event(event_data)
                    
            except Exception as e:
                logger.error(f"Error receiving FreeSWITCH events: {e}")
                break
                
    def _handle_event(self, event_data):
        try:
            # Parse FreeSWITCH event
            event = {}
            for line in event_data.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    event[key.strip()] = value.strip()
            
            # Handle specific events
            if event.get('Event-Name') == 'CHANNEL_ANSWER':
                self._handle_call_answered(event)
            elif event.get('Event-Name') == 'PLAYBACK_STOP':
                self._handle_playback_complete(event)
            elif event.get('Event-Name') == 'DTMF':
                self._handle_dtmf(event)
                
        except Exception as e:
            logger.error(f"Error parsing FreeSWITCH event: {e}")
            
    def _handle_call_answered(self, event):
        logger.info(f"Call answered: {event.get('Caller-Caller-ID-Number')} -> {event.get('Caller-Destination-Number')}")
        # Trigger orchestrator call flow
        
    def _handle_playback_complete(self, event):
        logger.info("Playback completed")
        # Continue with next step in call flow
        
    def _handle_dtmf(self, event):
        digit = event.get('DTMF-Digit')
        logger.info(f"DTMF received: {digit}")
        # Process user input
        
    def execute(self, command):
        """Execute FreeSWITCH command via ESL"""
        if self.connected:
            try:
                cmd = f"api {command}\n\n"
                self.socket.send(cmd.encode())
                logger.info(f"Executed FreeSWITCH command: {command}")
            except Exception as e:
                logger.error(f"Failed to execute FreeSWITCH command: {e}")
                
    def disconnect(self):
        self.connected = False
        if self.socket:
            self.socket.close()

# Global FreeSWITCH client instance
fs_client = FreeSWITCHClient()

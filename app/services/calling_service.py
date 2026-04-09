import httpx
import asyncio
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class CallingService:
    def __init__(self):
        self.freeswitch_host = settings.fs_esl_host
        self.freeswitch_port = 8021
        self.freeswitch_password = settings.fs_esl_password

    async def make_outbound_call(self, phone_number: str, caller_id: str = "TeleMER") -> bool:
        """Make outbound call to phone number"""
        try:
            # Format phone number (remove +, add 00 if needed)
            formatted_number = self._format_phone_number(phone_number)
            
            # Create call via FreeSWITCH external SIP gateway
            command = f"originate {{origination_caller_id_name={caller_id},origination_caller_id_number={caller_id}}}sofia/gateway/freevoipdeal_trunk/{formatted_number} &transfer(9001)"
            
            result = await self._execute_freeswitch_command(command)
            
            if result and "+OK" in result:
                logger.info(f"Outbound call initiated to {phone_number}")
                return True
            else:
                logger.error(f"Failed to initiate call to {phone_number}: {result}")
                return False
                
        except Exception as e:
            logger.error(f"Error making outbound call to {phone_number}: {e}")
            return False

    def _format_phone_number(self, phone_number: str) -> str:
        """Format phone number for SIP dialing"""
        # Remove + and spaces
        formatted = phone_number.replace("+", "").replace(" ", "").replace("-", "")
        
        # Add 00 if no country code
        if len(formatted) == 10 and not formatted.startswith("00"):
            formatted = "00" + formatted
        elif len(formatted) == 11 and formatted.startswith("1"):
            formatted = "00" + formatted
            
        return formatted

    async def _execute_freeswitch_command(self, command: str) -> Optional[str]:
        """Execute FreeSWITCH command via ESL"""
        try:
            import socket
            
            # Connect to FreeSWITCH ESL
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.freeswitch_host, self.freeswitch_port))
            
            # Authenticate
            sock.send(f"auth {self.freeswitch_password}\n\n".encode())
            auth_response = sock.recv(1024).decode()
            
            if "+OK" not in auth_response:
                sock.close()
                return None
            
            # Execute command
            sock.send(f"api {command}\n\n".encode())
            response = sock.recv(1024).decode()
            
            sock.close()
            return response
            
        except Exception as e:
            logger.error(f"Error executing FreeSWITCH command: {e}")
            return None

    async def hangup_call(self, call_uuid: str) -> bool:
        """Hangup active call"""
        try:
            command = f"uuid_kill {call_uuid}"
            result = await self._execute_freeswitch_command(command)
            return result and "+OK" in result
        except Exception as e:
            logger.error(f"Error hanging up call {call_uuid}: {e}")
            return False

    async def get_call_status(self, call_uuid: str) -> Optional[str]:
        """Get call status"""
        try:
            command = f"uuid_dump {call_uuid}"
            result = await self._execute_freeswitch_command(command)
            return result
        except Exception as e:
            logger.error(f"Error getting call status {call_uuid}: {e}")
            return None

# Global calling service instance
calling_service = CallingService()

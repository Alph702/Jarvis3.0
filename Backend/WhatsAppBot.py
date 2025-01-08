import pywhatkit as pwk
import json
import time as t
from pathlib import Path
from pyautogui import press, hotkey, keyDown, keyUp


class WhatsAppBot:
    def __init__(self, contacts_file: str = "Data/Contact.json"):
        """
        Initialize the WhatsAppBot with contacts file.
        Args:
            contacts_file (str): Path to the contacts JSON file.
        """
        self.contacts_file = contacts_file
        self.contacts = self._load_contacts()

    def _load_contacts(self):
        """Load contacts from the JSON file."""
        try:
            with open(self.contacts_file, 'r') as f:
                data = json.load(f)
                return data.get('people', {})
        except FileNotFoundError:
            print(f"Contacts file not found at {self.contacts_file}")
            return {}
        except json.JSONDecodeError:
            print(f"Invalid JSON in contacts file: {self.contacts_file}")
            return {}

    def send_message(self, name: str, message: str, time: str = "now"):
        """
        Send a WhatsApp message to the specified contact.
        Args:
            name (str): Name of the contact (as saved in contacts file).
            message (str): The message to send.
            time (str): Time to send message ("now" or "HH:MM AM/PM" format)
        """
        name = name.lower()
        # Convert contact names to lowercase for case-insensitive comparison
        contact_found = None
        for contact_name in self.contacts:
            if contact_name.lower() == name:
                contact_found = contact_name
                break
                
        if not contact_found:
            print(f"Contact {name} not found in contacts file")
            return False

        phone_number = f"+{self.contacts[contact_found]}"
        
        try:
            if time.lower() == "now":
                # Send message immediately
                pwk.sendwhatmsg_instantly(
                    phone_no=phone_number,
                    message=message,
                    wait_time=15
                )
                t.sleep(2)
                press('enter')
                press('enter')
                t.sleep(5)
                hotkey('ctrl', 'w')
            else:
                # Parse time in 12-hour format (HH:MM AM/PM)
                try:
                    # Split time and AM/PM
                    time_parts = time.upper()
                    time_parts = time_parts.replace('.','')
                    time_parts = time_parts.split()
                    if len(time_parts) != 2 or time_parts[1] not in ['AM', 'PM']:
                        raise ValueError("Time must be in 'HH:MM AM/PM' format")
                    
                    time_str, period = time_parts
                    hour, minute = map(int, time_str.split(':'))
                    
                    # Convert to 24-hour format
                    if period == 'PM' and hour != 12:
                        hour += 12
                    elif period == 'AM' and hour == 12:
                        hour = 0
                        
                    if not (0 <= hour <= 23 and 0 <= minute <= 59):
                        raise ValueError("Invalid hour or minute")
                    
                    pwk.sendwhatmsg(
                        phone_no=phone_number,
                        message=message,
                        time_hour=hour,
                        time_min=minute,
                        wait_time=15
                    )
                    press('enter')
                    press('enter')
                    t.sleep(1)
                    hotkey('ctrl', 'w')
                except ValueError as ve:
                    print(f"Invalid time format: {str(ve)}. Use 'HH:MM AM/PM' format (e.g., '02:30 PM')")
                    return False
            
            return True
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return False

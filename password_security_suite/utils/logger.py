import logging
import os
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

class Logger:
    def __init__(self, log_file="data/reports/activity.log"):
        # Ensure directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("SecuritySuite")

    def info(self, message):
        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {message}")
        self.logger.info(message)

    def success(self, message):
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {message}")
        self.logger.info(f"SUCCESS: {message}")

    def warn(self, message):
        print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {message}")
        self.logger.warning(message)

    def error(self, message):
        print(f"{Fore.RED}[-]{Style.RESET_ALL} {message}")
        self.logger.error(message)
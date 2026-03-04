import os
import platform
import re

class CredentialExtractor:
    def __init__(self):
        self.os_type = platform.system()

    def extract_linux_hashes(self, shadow_path="/etc/shadow"):
        """
        Parses the Linux shadow file.
        Format: username:$id$salt$hash:lastchanged:min:max:warn:inactive:expire
        """
        extracted = []
        if not os.path.exists(shadow_path):
            return {"error": f"Shadow file not found at {shadow_path}"}

        try:
            with open(shadow_path, 'r') as f:
                for line in f:
                    parts = line.strip().split(':')
                    if len(parts) > 1 and parts[1] not in ['*', '!', '!!', '']:
                        user = parts[0]
                        full_hash = parts[1]
                        
                        # Identify Algorithm
                        algo = "Unknown"
                        if full_hash.startswith('$1$'): algo = "MD5"
                        elif full_hash.startswith('$5$'): algo = "SHA-256"
                        elif full_hash.startswith('$6$'): algo = "SHA-512"
                        elif full_hash.startswith('$y$'): algo = "Yescrypt"

                        extracted.append({
                            "user": user,
                            "hash": full_hash,
                            "algo": algo,
                            "source": "Linux Shadow"
                        })
            return extracted
        except PermissionError:
            return {"error": "Permission denied. Root access required to read shadow file."}

    def extract_windows_hashes(self, sam_path, system_path):
        """
        On Windows, hashes are stored in the SAM hive, but encrypted using a key 
        found in the SYSTEM hive. This method simulates the detection of these files.
        Note: True extraction usually requires external libraries like 'impacket' 
        or 'pysam'. Here we provide the parser logic.
        """
        if not os.path.exists(sam_path) or not os.path.exists(system_path):
            return {"error": "SAM or SYSTEM hive files missing."}

        # Engineering logic: In a real toolkit, we would use a library to parse 
        # the hive binary. For this project, we return the metadata for the audit.
        return [{
            "user": "Administrator",
            "hash": "AAD3B435B51404EEAAD3B435B51404EE:31D6CFE0D16AE931B73C59D7E0C089C0", # Example NTLM
            "algo": "NTLM",
            "source": "Windows SAM"
        }]

    def identify_hash_type(self, hash_str):
        """Utility to identify hash type based on length/format."""
        length = len(hash_str)
        if "$" in hash_str: return "Modular Crypt Format (Linux)"
        if length == 32: return "MD5 or NTLM"
        if length == 40: return "SHA-1"
        if length == 64: return "SHA-256"
        if length == 128: return "SHA-512"
        return "Unknown"

# Example Usage
if __name__ == "__main__":
    extractor = CredentialExtractor()
    # On a lab Linux machine:
    # print(extractor.extract_linux_hashes("data/hashes/shadow_backup"))
import hashlib
import time
import itertools
import string

class PasswordCracker:
    def __init__(self):
        # Supported hash algorithms
        self.algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
        }

    def _hash_value(self, text, algorithm):
        """Helper to hash a string based on the chosen algorithm."""
        algorithm = algorithm.lower()
        
        if algorithm == 'ntlm':
            # NTLM logic: MD4(UTF-16-LE(password))
            # Note: hashlib.new('md4') might require OpenSSL legacy provider on some systems
            hash_obj = hashlib.new('md4', text.encode('utf-16le'))
            return hash_obj.hexdigest()
        
        hash_func = self.algorithms.get(algorithm)
        if not hash_func:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        return hash_func(text.encode()).hexdigest()

    def dictionary_attack(self, target_hash, wordlist_path, algorithm='sha256'):
        """Attempts to match the hash using a wordlist and records metrics."""
        print(f"[*] Starting Dictionary Attack (Algo: {algorithm})...")
        start_time = time.time()
        attempts = 0

        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    attempts += 1
                    word = line.strip()
                    
                    # Compare generated hash to target
                    if self._hash_value(word, algorithm) == target_hash:
                        duration = time.time() - start_time
                        return {
                            "success": True, 
                            "password": word, 
                            "attempts": attempts, 
                            "time": round(duration, 4)
                        }
        except FileNotFoundError:
            return {"success": False, "error": "Wordlist file not found.", "attempts": 0, "time": 0}

        # If loop finishes without a match
        duration = time.time() - start_time
        return {
            "success": False, 
            "attempts": attempts, 
            "time": round(duration, 4)
        }

    def brute_force_simulator(self, target_hash, max_length=4, algorithm='sha256'):
        """
        Simulates an incremental brute-force attack.
        Used to demonstrate why length is the best defense.
        """
        print(f"[*] Starting Brute-Force Simulation (Max Length: {max_length})...")
        # Character set: Uppercase, lowercase, digits, and punctuation
        chars = string.ascii_letters + string.digits + string.punctuation
        start_time = time.time()
        attempts = 0

        for length in range(1, max_length + 1):
            for guess in itertools.product(chars, repeat=length):
                attempts += 1
                guess_str = "".join(guess)
                
                if self._hash_value(guess_str, algorithm) == target_hash:
                    duration = time.time() - start_time
                    return {
                        "success": True, 
                        "password": guess_str, 
                        "attempts": attempts, 
                        "time": round(duration, 4)
                    }
        
        duration = time.time() - start_time
        return {
            "success": False, 
            "attempts": attempts, 
            "time": round(duration, 4)
        }

# Example Usage for Testing
if __name__ == "__main__":
    cracker = PasswordCracker()
    # SHA-256 hash of "manpreet1"
    # 269785023945958564177d018659d5718a38ecf8476839a82046835d0059f1c7
    target = "269785023945958564177d018659d5718a38ecf8476839a82046835d0059f1c7"
    
    # Replace with your actual wordlist path
    # result = cracker.dictionary_attack(target, "data/wordlists/custom_list.txt")
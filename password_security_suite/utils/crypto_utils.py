import hashlib
import binascii

class CryptoUtils:
    @staticmethod
    def to_ntlm(password):
        """Converts plaintext to Windows NTLM hash."""
        hash_obj = hashlib.new('md4', password.encode('utf-16le'))
        return binascii.hexlify(hash_obj.digest()).decode()

    @staticmethod
    def hash_string(text, algorithm="sha256"):
        """Generic wrapper for standard hashing."""
        algo = algorithm.lower()
        if algo == "ntlm":
            return CryptoUtils.to_ntlm(text)
        
        try:
            hash_func = getattr(hashlib, algo)
            return hash_func(text.encode()).hexdigest()
        except AttributeError:
            return None

    @staticmethod
    def compare_hashes(plain_text, stored_hash, algorithm="sha256"):
        """Secure comparison to prevent timing attacks."""
        generated = CryptoUtils.hash_string(plain_text, algorithm)
        if generated is None:
            return False
        # Use constant-time comparison
        return hashlib.pbkdf2_hmac('sha256', generated.encode(), b'salt', 1) == \
               hashlib.pbkdf2_hmac('sha256', stored_hash.encode(), b'salt', 1)
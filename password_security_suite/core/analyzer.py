import math
import re

class PasswordAnalyzer:
    def __init__(self):
        # List of common weak patterns to flag
        self.common_patterns = [
            r"123", r"abc", r"qwerty", r"password", r"admin"
        ]

    def calculate_entropy(self, password):
        """
        Calculates the Shannon Entropy of a password.
        Formula: H = L * log2(R)
        """
        if not password:
            return 0
        
        character_pool = 0
        if re.search(r'[a-z]', password): character_pool += 26
        if re.search(r'[A-Z]', password): character_pool += 26
        if re.search(r'[0-9]', password): character_pool += 10
        if re.search(r'[^a-zA-Z0-9]', password): character_pool += 32
        
        if character_pool == 0: return 0
        
        # Entropy Calculation
        entropy = len(password) * math.log2(character_pool)
        return round(entropy, 2)

    def evaluate_complexity(self, password):
        """Checks against corporate security policy (Length 12+, Mixed Case, Numbers, Symbols)."""
        checks = {
            "length": len(password) >= 12,
            "uppercase": bool(re.search(r'[A-Z]', password)),
            "lowercase": bool(re.search(r'[a-z]', password)),
            "digit": bool(re.search(r'[0-9]', password)),
            "special": bool(re.search(r'[^a-zA-Z0-9]', password))
        }
        return checks

    def suggest_stronger_version(self, password):
        """
        Remediation Logic: This is the 'Stronger Version' generator.
        It analyzes what's missing and injects it.
        """
        if not password:
            return "P@ssw0rd2026!"

        stronger = password
        
        # 1. Add Uppercase if missing
        if not re.search(r'[A-Z]', stronger):
            stronger = stronger.capitalize()
            
        # 2. Add Numbers if missing
        if not re.search(r'[0-9]', stronger):
            stronger += "2026"
            
        # 3. Add Special Characters if missing
        if not re.search(r'[^a-zA-Z0-9]', stronger):
            stronger += "!"
            
        # 4. Ensure it hits the 14-character security sweet spot
        while len(stronger) < 14:
            stronger += "x"
            
        return stronger

    def check_predictability(self, password):
        """Flags common easy-to-guess patterns."""
        findings = []
        for pattern in self.common_patterns:
            if re.search(pattern, password.lower()):
                findings.append(f"Common pattern detected: '{pattern}'")
        return findings

    def get_strength_rating(self, entropy):
        """Converts raw bits into a human-readable score."""
        if entropy < 28: return "Very Weak"
        if entropy < 36: return "Weak"
        if entropy < 60: return "Reasonable"
        if entropy < 128: return "Strong"
        return "Very Strong"

    def analyze(self, password):
        """Main method that runs the full checkup."""
        entropy = self.calculate_entropy(password)
        complexity = self.evaluate_complexity(password)
        patterns = self.check_predictability(password)
        rating = self.get_strength_rating(entropy)
        
        # If common patterns like '123' are found, the rating drops
        if patterns and entropy < 60:
            rating = "Weak (Predictable)"

        # Only generate a suggestion if the password isn't already 'Perfect'
        passed_all = all(complexity.values())
        recommendation = self.suggest_stronger_version(password) if not passed_all else "Already Secure"

        return {
            "password": password,
            "entropy_bits": entropy,
            "rating": rating,
            "passed_complexity": passed_all,
            "details": complexity,
            "warnings": patterns,
            "suggested_password": recommendation
        }

# Example Usage
if __name__ == "__main__":
    analyzer = PasswordAnalyzer()
    results = analyzer.analyze("manpreet1")
    
    print(f"--- Analysis Results ---")
    print(f"Password: {results['password']}")
    print(f"Rating:   {results['rating']}")
    print(f"Status:   {'PASS' if results['passed_complexity'] else 'FAIL'}")
    print(f"Suggested Stronger Version: {results['suggested_password']}")
import itertools
import re
import os

class DictionaryGenerator:
    def __init__(self):
        # Professional Leet-speak mapping
        self.leet_map = {
            'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'],
            'o': ['0'], 's': ['5', '$'], 't': ['7']
        }
        # Absolute Path Setup
        self.base_dir = r"C:\Users\manpr\OneDrive\Desktop\password_security_suite"
        self.default_path = os.path.join(self.base_dir, "data", "wordlists", "custom_list.txt")

    def generate_base_list(self, user_data):
        """Creates a base wordlist from user-provided info."""
        base_list = set(user_data)
        variations = set()
        for word in base_list:
            variations.update([word.lower(), word.upper(), word.capitalize()])
        return list(variations)

    def apply_mutations(self, base_list, include_numbers=True, include_special=True):
        """Applies mutation rules to the base list."""
        mutated_list = set(base_list)
        
        # Adding 2026 as it's the current simulation year
        years = ['2023', '2024', '2025', '2026', '123', '1']
        specials = ['!', '@', '#', '$', '%', '&']

        for word in base_list:
            if include_numbers:
                for year in years:
                    mutated_list.add(f"{word}{year}")
            
            if include_special:
                for char in specials:
                    mutated_list.add(f"{word}{char}")
                    
        return list(mutated_list)

    def apply_leet_speak(self, word):
        """Creates all possible leet-speak combinations for a word."""
        chars = []
        for char in word.lower():
            if char in self.leet_map:
                chars.append([char, *self.leet_map[char]])
            else:
                chars.append([char])
        
        return ["".join(combination) for combination in itertools.product(*chars)]

    def save_to_file(self, wordlist, filename=None):
        """
        Exports the generated list to the absolute path.
        If filename is provided, it saves within the absolute wordlists folder.
        """
        # If no filename is passed, use the default absolute path
        if filename is None:
            target_path = self.default_path
        else:
            # If a filename like "test.txt" is passed, put it in the correct folder
            target_path = os.path.join(self.base_dir, "data", "wordlists", filename)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        try:
            with open(target_path, "w", encoding='utf-8') as f:
                for word in sorted(wordlist):
                    f.write(f"{word}\n")
            print(f"[+] Successfully generated {len(wordlist)} passwords to: {target_path}")
        except IOError as e:
            print(f"[-] Error saving wordlist: {e}")

# Example Usage
if __name__ == "__main__":
    gen = DictionaryGenerator()
    target_info = ["Admin", "Security", "2026"]
    
    base = gen.generate_base_list(target_info)
    mutated = gen.apply_mutations(base)
    
    leet_variants = gen.apply_leet_speak("Security")
    final_list = set(mutated).union(set(leet_variants))
    
    # This will now save to your specific Desktop path automatically
    gen.save_to_file(final_list)
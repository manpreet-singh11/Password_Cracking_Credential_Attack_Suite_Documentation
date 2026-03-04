import os
import sys
import hashlib
from core.analyzer import PasswordAnalyzer
from core.dictionary_gen import DictionaryGenerator
from core.cracker import PasswordCracker
from utils.logger import Logger
from utils.report_gen import ReportGenerator

def main():
    # 1. Initialize all modules
    logger = Logger()
    analyzer = PasswordAnalyzer()
    dict_gen = DictionaryGenerator()
    cracker = PasswordCracker()
    reporter = ReportGenerator()

    # Session Memory - Holds data until the app is closed
    analysis_results = []
    crack_results = None 

    logger.info("Security Suite Initialized and Ready.")

    while True:
        print("\n" + "="*40)
        print(f"{'PASSWORD SECURITY SUITE':^40}")
        print("="*40)
        print("1. Generate Custom Dictionary")
        print("2. Analyze Password Strength")
        print("3. Crack Password Hashes")
        print("4. (Optional) Extract Hashes")
        print("5. GENERATE FINAL AUDIT REPORT")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ")

        if choice == '1':
            logger.info("Starting Targeted Dictionary Generation...")
            raw_input = input("Enter seed keywords (comma separated): ")
            if not raw_input.strip():
                logger.error("No keywords provided.")
                continue
                
            user_input = raw_input.split(',')
            base = dict_gen.generate_base_list([i.strip() for i in user_input])
            final_list = dict_gen.apply_mutations(base)
            
            dict_gen.save_to_file(final_list)
            logger.success(f"Custom wordlist built with {len(final_list)} variations.")

        elif choice == '2':
            pwd = input("Enter password for policy analysis: ")
            if not pwd:
                continue
                
            result = analyzer.analyze(pwd)
            analysis_results.append(result) 
            
            # Professional Touch: Show the hash immediately for testing Option 3
            current_hash = hashlib.sha256(pwd.encode()).hexdigest()
            
            print(f"\n[Analysis Results]")
            print(f"Rating:   {result['rating']}")
            print(f"Entropy:  {result['entropy_bits']} bits")
            print(f"SHA-256:  {current_hash}") # Copy this for Option 3!
            if result.get('suggested_password'):
                print(f"Fix:      {result['suggested_password']}")

        elif choice == '3':
            logger.info("Initiating Dictionary Attack Simulation...")
            target_hash = input("Enter the target hash: ").strip()
            algo = input("Enter algorithm (md5, sha1, sha256) [default: sha256]: ").lower() or 'sha256'
            
            if not target_hash:
                logger.error("Hash input required.")
                continue

            wordlist_path = r"C:\Users\manpr\OneDrive\Desktop\password_security_suite\data\wordlists\custom_list.txt"
            
            # Perform the attack
            crack_results = cracker.dictionary_attack(target_hash, wordlist_path, algorithm=algo)
            
            if crack_results.get("success"):
                logger.success(f"Hash cracked successfully!")
                print(f"Plaintext: {crack_results['password']}")
                print(f"Performance: {crack_results['time']:.4f}s | {crack_results['attempts']} attempts")
            else:
                logger.error("Attack finished: No match found.")
                print(f"Stats: {crack_results.get('attempts', 0)} attempts in {crack_results.get('time', 0):.4f}s")

        elif choice == '5':
            if not analysis_results:
                logger.error("Report Generation Denied: No analysis data found. Run Option 2 first.")
            else:
                logger.info("Compiling all session data into Audit Report...")
                
                # Pass both lists to the generator
                report_content = reporter.generate_summary(analysis_results, crack_results)
                
                # Export to TXT
                final_path = reporter.export_report(report_content)
                logger.success(f"Audit Complete. File saved to reports folder.")

        elif choice == '6':
            logger.info("Security session terminated.")
            print("Goodbye.")
            sys.exit()
            
        else:
            print("Invalid selection. Please choose between 1 and 6.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Emergency Shutdown initiated.")
        sys.exit()
Project Objectives

Understand how password hashes are stored (Linux & Windows)

Simulate dictionary and brute-force attack techniques

Analyze password strength and entropy

Identify weak credentials

Generate security audit reports with mitigation recommendations

🧠 Why This Project Matters

Passwords remain one of the most targeted attack vectors in cybersecurity.

Weak password policies can lead to:

Account takeovers

Privilege escalation

Data breaches

Credential stuffing attacks

This project helps bridge both Red Team (offensive simulation) and Blue Team (defensive auditing) perspectives.

🛠️ Features
✅ Dictionary Generator

Custom wordlist creation

Pattern-based generation (name + DOB, keyboard patterns, common passwords)

Mutation rules (leet substitutions, uppercase variations, appended numbers)

✅ Hash Extraction Module (Lab Demonstration)

Linux /etc/shadow hash extraction (controlled VM only)

Windows SAM & SYSTEM hive export (offline method)

Hash type identification (MD5, SHA-512, NTLM, etc.)

✅ Brute-Force Simulation Engine

Incremental character testing (a–z, A–Z, 0–9, symbols)

Dictionary attack simulation

Estimated time-to-crack calculation

Ethical cracking demonstration only

✅ Password Strength Analyzer

Complexity validation

Entropy estimation

Dictionary-based weakness detection

Risk classification (Low / Medium / High)

Security improvement recommendations

✅ Report Generation

Weak password summary

Cracking simulation results

Risk analysis

Mitigation suggestions

⚙️ Technologies Used

Programming Language:

Python 3.x

Python Modules:

hashlib

passlib / crypt

argparse

random

string

Optional Tools (Reference Only):

John the Ripper

Hashcat

📁 Project Structure
password_attack_suite/
│
├── dictionary/
├── hash_extraction/
├── brute_force/
├── strength_analysis/
├── reports/
├── main.py
└── requirements.txt
🚀 Installation
git clone https://github.com/yourusername/password-attack-suite.git
cd password-attack-suite
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux
pip install -r requirements.txt
▶️ Usage Examples

Generate dictionary:

python main.py --generate-dictionary

Analyze password strength:

python main.py --analyze-password "Password123"

Simulate attack on hash file:

python main.py --simulate-attack hashes.txt
🔬 Workflow

User provides input (passwords or hash file)

Generate custom dictionary

Identify hash algorithm

Simulate dictionary or brute-force attack

Analyze password strength

Generate final security audit report

📊 Sample Output

Generated wordlist file

Identified hash types

Estimated time-to-crack

Weak password severity rating

Security recommendations

🧪 Testing & Validation

The project includes:

Unit testing of individual modules

Weak vs strong password classification testing

Dictionary attack simulation validation

Entropy and complexity verification

Performance testing with large wordlists

🎓 Learning Outcomes

Through this project, I gained hands-on understanding of:

Password hashing mechanisms

Ethical attack simulation methodologies

Authentication security auditing

Password entropy calculation

Defensive security improvements

⚠️ Disclaimer

This project is strictly for:

Cybersecurity students

Security researchers

Ethical hacking labs

Defensive security auditing practice

Unauthorized password cracking is illegal and unethical.

📌 Future Improvements

Multi-threaded brute-force simulation

GUI interface

Advanced entropy modeling

Account lockout simulation

Integration with SIEM-style logging

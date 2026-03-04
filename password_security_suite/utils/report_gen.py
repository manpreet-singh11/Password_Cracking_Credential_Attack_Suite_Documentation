import json
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        # Absolute path to your project folder
        self.base_dir = r"C:\Users\manpr\OneDrive\Desktop\password_security_suite"
        self.output_dir = os.path.join(self.base_dir, "data", "reports")
        
        # Ensure the directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_summary(self, analysis_results, crack_results=None):
        """
        Compiles all module outputs into a structured dictionary.
        """
        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "assessment_summary": {
                "total_passwords_analyzed": len(analysis_results),
                "vulnerabilities_detected": 0,
                "risk_level": "Low"
            },
            "detailed_findings": [],
            "recommendations": []
        }

        # Identify if a specific password was cracked
        cracked_password = None
        if crack_results and crack_results.get("success"):
            cracked_password = crack_results.get("password")

        # Process Analysis Data
        vulnerability_count = 0
        for res in analysis_results:
            is_cracked = (res['password'] == cracked_password)
            failed_complexity = not res['passed_complexity']
            
            # Determine status label
            if is_cracked:
                status_label = "COMPROMISED"
            elif failed_complexity:
                status_label = "FAIL (Policy)"
            else:
                status_label = "PASS"

            finding = {
                "target": res['password'],
                "strength": res['rating'],
                "entropy": f"{res['entropy_bits']} bits",
                "status": status_label,
                "remediation": res.get('suggested_password', "Secure - No changes needed.")
            }

            # Count as vulnerability if it fails policy, is weak, or was cracked
            if res['rating'] in ["Very Weak", "Weak"] or failed_complexity or is_cracked:
                vulnerability_count += 1
                
            report["detailed_findings"].append(finding)

        # --- CRACKING DATA INCLUSION ---
        # Maps the 'time' and 'attempts' from core/cracker.py
        if crack_results:
            report["cracking_simulation"] = {
                "success": crack_results.get("success", False),
                "time_taken": crack_results.get('time', 0.0), 
                "attempts_made": crack_results.get("attempts", 0)
            }

        # Global Risk Level Logic
        if vulnerability_count > 0:
            if vulnerability_count > (len(analysis_results) / 2):
                report["assessment_summary"]["risk_level"] = "High"
            else:
                report["assessment_summary"]["risk_level"] = "Medium"
        
        report["assessment_summary"]["vulnerabilities_detected"] = vulnerability_count
        report["recommendations"] = self._get_recommendations(report["assessment_summary"]["risk_level"])
        
        return report

    def _get_recommendations(self, risk_level):
        recs = ["Implement multi-factor authentication (MFA).", "Use 14+ character passphrases."]
        if risk_level in ["High", "Medium"]:
            recs.append("Rotate compromised credentials immediately.")
            recs.append("Enforce account lockout policies.")
        return recs

    def export_report(self, report_data, format="txt"):
        """Saves the final report to the local file system."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"audit_{timestamp}.{format}"
        full_path = os.path.join(self.output_dir, filename)
        
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                if format == "json":
                    json.dump(report_data, f, indent=4)
                else:
                    self._write_text_report(f, report_data)
            print(f"[+] Audit report generated successfully at: {full_path}")
        except IOError as e:
            print(f"[-] Failed to write report: {e}")

    def _write_text_report(self, file_handle, data):
        """Generates the visual text layout with specific cracking metrics."""
        file_handle.write("="*70 + "\n")
        file_handle.write(f"{'PASSWORD SECURITY AUDIT REPORT':^70}\n")
        file_handle.write(f"{'Date: ' + data['timestamp']:^70}\n")
        file_handle.write("="*70 + "\n\n")
        
        summary = data['assessment_summary']
        file_handle.write(f"OVERALL RISK LEVEL: {summary['risk_level']}\n")
        file_handle.write(f"Vulnerabilities Found: {summary['vulnerabilities_detected']}\n")
        file_handle.write(f"Total Analyzed: {summary['total_passwords_analyzed']}\n\n")
        
        # --- CRACKING PERFORMANCE SECTION ---
        file_handle.write("-" * 25 + " CRACKING STATS " + "-" * 29 + "\n")
        if 'cracking_simulation' in data:
            sim = data['cracking_simulation']
            status = "SUCCESS" if sim['success'] else "FAILED"
            time_val = sim['time_taken']
            attempts = sim['attempts_made']
            
            file_handle.write(f"  Result:         {status}\n")
            file_handle.write(f"  Time Taken:     {time_val:.4f} seconds\n")
            file_handle.write(f"  Attempts Made:  {attempts}\n")
            
            if time_val > 0:
                speed = int(attempts / time_val)
                file_handle.write(f"  Cracking Speed: {speed:,} attempts/second\n")
        else:
            file_handle.write(f"  STATUS: No cracking simulation conducted in this session.\n")
        
        file_handle.write("-" * 70 + "\n\n")
        
        # --- DETAILED FINDINGS TABLE ---
        file_handle.write(f"{'PASSWORD':<20} | {'STATUS':<16} | {'SUGGESTED FIX'}\n")
        file_handle.write("-" * 70 + "\n")
        for finding in data['detailed_findings']:
            file_handle.write(f"{finding['target']:<20} | {finding['status']:<16} | {finding['remediation']}\n")
            
        file_handle.write("\n" + "="*70 + "\n")
        file_handle.write("SECURITY RECOMMENDATIONS:\n")
        for rec in data['recommendations']:
            file_handle.write(f"[*] {rec}\n")
        file_handle.write("="*70 + "\n")
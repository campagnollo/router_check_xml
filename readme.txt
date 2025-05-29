Automated SSH-based configuration check tool for network devices using Paramiko and XML parsing.

This Python script connects to one or more network devices (e.g., Cisco routers or switches) via SSH, executes
 commands, and parses the resulting XML output to validate configuration elements. It’s ideal for compliance checks,
 configuration audits, or daily health monitoring in a network automation workflow.

🔧 Features
🔐 SSH-based connection using paramiko

⚙️ Command execution on remote devices

🧾 Structured XML response parsing

🛠️ Useful for:

Configuration validation

Compliance audits

Nightly health checks

Integration with CI/CD pipelines

📁 File Structure
bash
Copy
Edit
router_check_xml/
├── router_check_xml.py   # Main script
├── devices.txt           # List of target devices (IP addresses or hostnames)
└── requirements.txt      # Required Python packages

🚀 Getting Started
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/campagnollo/router_check_xml.git
cd router_check_xml
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Configure Your Devices List
Create a file named devices.txt with one IP address or hostname per line:

Copy
Edit
192.0.2.1
router1.localdomain
4. Run the Script
bash
Copy
Edit
python router_check_xml.py
🔐 Authentication
Currently, the script uses username/password authentication hardcoded or prompted interactively.
 Consider enhancing it with:

SSH key support

Secure vault integration (e.g., HashiCorp Vault, AWS Secrets Manager)

Environment variables or encrypted credentials

📘 Sample Use Case
Imagine you need to ensure all your Cisco routers have ip ssh version 2 configured:

The script logs in to each router.

It runs a command like show running-config | include ip ssh.

The result is parsed (especially if output is in XML format).

The script reports whether each device is compliant.

💡 Potential Enhancements
CLI support (argparse)

JSON/YAML config file for commands

Logging and error handling improvements

Output to CSV/JSON for reporting

Integration with CI tools like Jenkins or GitHub Actions

📎 Related Technologies
Python 2.x

Paramiko – SSH library for Python

Cisco IOS/NX-OS – Devices tested against (can be extended)

🧑‍💻 Author
Eric L. Moore
DevOps & Cloud Infrastructure Engineer
GitHub

📜 License
This project is licensed under the MIT License.

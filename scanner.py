import json
import yaml
import os
import shutil
import subprocess

xygeni_dir = "/home/daniel/Desktop/xygeni_scanner/"

scan_options = [
    "Full Scan",
    "Inventory Scan",
    "Secrets Scan",
    "CodeTamper Scan",
    "Dependency Scan",
    "Suspicious Dependency Scan",
    "Misconfiguration Scan",
    "Compliance Scan",
    "IAC Scan",
]

ct_data = {}
comp_data = {}
inventory_data = {}
deps_data = {}
suspectdeps_data = {}
iac_data = {}
secrets_data = {}
misconf_data = {}

scanerino = {}


def scanner_dir_configured():
    return os.path.isdir(xygeni_dir)


bash_command = ""


def start_scan(selected_scan, source_code_directory):
    if selected_scan == "Misconfiguration Scan":
        selected_scan = "misconf"
    elif selected_scan == "Secrets Scan":
        selected_scan = "secrets"
    elif selected_scan == "CodeTamper Scan":
        selected_scan = "codetamper"
    elif selected_scan == "IAC Scan":
        selected_scan = "iac"
    elif selected_scan == "Inventory Scan":
        selected_scan = "inventory"
    elif selected_scan == "Compliance Scan":
        selected_scan = "compliance"
    elif selected_scan == "Dependency Scan":
        selected_scan = "deps"
    elif selected_scan == "Suspicious Dependency Scan":
        selected_scan = "suspectdeps"
    else:
        selected_scan = "scan"

    command = [xygeni_dir + 'xygeni', selected_scan, '-d', source_code_directory, '-n', 'default',
               '-o', 'results/' + selected_scan + '.json', '-f', 'json']
    delete_results()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('======================= Scan Started: ', process.pid, process, process.args)
    while process.returncode is None:
        stdout_output = process.stdout.readline()
        stderr_output = process.stderr.readline()
        if stdout_output == b'' and stderr_output == b'' and process.poll() is not None:
            break
        if stdout_output:
            print(stdout_output.decode('utf-8').strip())
        if stderr_output:
            print(stderr_output.decode('utf-8').strip())

    process.terminate()
    process.kill()
    print('======================= Scan Ended: ', process.pid, process, process.args)


def parse_results():
    directory_path = os.getcwd() + '/results'
    try:
        if not os.path.exists(directory_path):
            print(f"The directory '{directory_path}' does not exist.")
            return

        data_store = ScanDetails()

        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if "codetamper" in file.lower() and file.endswith(".json"):
                    with open(file_path, 'r') as json_file:
                        ct_data[file] = json.load(json_file)
                        data_store.ct_data = ct_data[file]
                elif "compliance" in file.lower() and file.endswith(".json"):
                    with open(file_path, 'r') as json_file:
                        comp_data[file] = json.load(json_file)
                        data_store.comp_data = comp_data[file]
                elif "inventory" in file.lower() and file.endswith(".json"):
                    with open(file_path, 'r') as json_file:
                        inventory_data[file] = json.load(json_file)
                        data_store.inventory_data = inventory_data[file]
                elif "suspectdeps" in file.lower() and file.endswith(".json"):
                    with open(file_path, 'r') as json_file:
                        suspectdeps_data[file] = json.load(json_file)
                        data_store.suspectdeps_data = suspectdeps_data[file]
                elif "deps" in file.lower() and file.endswith(".json"):
                    with open(file_path, 'r') as json_file:
                        deps_data[file] = json.load(json_file)
                        data_store.deps_data = deps_data[file]
                elif "iac" in file.lower() and file.endswith(".json"):
                    with open(file_path, 'r') as json_file:
                        iac_data[file] = json.load(json_file)
                        data_store.iac_data = iac_data[file]
                elif "secrets" in file.lower() and file.endswith(".json"):
                    with open(file_path, 'r') as json_file:
                        secrets_data[file] = json.load(json_file)
                        data_store.secrets_data = secrets_data[file]
                elif "misconf" in file.lower() and file.endswith(".json"):
                    with open(file_path, 'r') as json_file:
                        misconf_data[file] = json.load(json_file)
                        data_store.misconf_data = misconf_data[file]

        return data_store

    except Exception as e:
        print(f"An error occurred parsing results: {str(e)}")


def delete_results():
    try:
        full_path = os.getcwd() + '/results'

        if not os.path.exists(full_path):
            print(f"The directory '{full_path}' does not exist.")
            return

        for root, dirs, files in os.walk(full_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                shutil.rmtree(dir_path)

        print(f"Deleted results in '{full_path}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def set_config(env):
    config_path = xygeni_dir + 'conf/xygeni.yml'
    yaml.explicit_start = True
    yaml.preserve_quotes = True  # not necessary for your current input
    with open(config_path, 'r') as file:
        data = yaml.safe_load(file)

        url_mapping = {
            'pro': 'https://in.xygeni.io/deps-doctor-service',
            'dev': 'https://apidev.xygeni.io/deps-doctor-service',
            'demo': 'https://apidemo.xygeni.io/deps-doctor-service',
            'local': 'http://localhost:8080/deps-doctor-service',
        }
        fe_url_mapping = {
            'pro': 'https://in.xygeni.io/dashboard',
            'dev': 'https://in.labdev.xygeni.io/dashboard',
            'demo': 'https://apidemo.xygeni.io/deps-doctor-service',
            'local': 'http://localhost:8080/deps-doctor-service',
        }

        # Update the specific values in the loaded data
        if 'api' in data:
            data['api']['url'] = url_mapping.get(env.lower())

        if 'dashboard' in data:
            data['dashboard']['url'] = fe_url_mapping.get(env.lower())

    with open(config_path, "w") as f:
        yaml.dump(data, f, sort_keys=False)


def get_config():
    config_path = xygeni_dir + 'conf/xygeni.yml'
    yaml.explicit_start = True
    yaml.preserve_quotes = True
    with open(config_path, 'r') as file:
        data = yaml.safe_load(file)
        return data


class ScanDetails:
    def __init__(self):
        self.ct_data = {}
        self.comp_data = {}
        self.inventory_data = {}
        self.deps_data = {}
        self.suspectdeps_data = {}
        self.iac_data = {}
        self.secrets_data = {}
        self.misconf_data = {}

import paramiko

class QUAFEL_API:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        # self.ssh = connect_ssh(host, port, username, password)
        

    def setup_quafel(self, ssh):
        self.command(ssh,"sudo apt-get update && sudo apt-get upgrade")
        self.command(ssh,"sudo apt install python3.10")
        self.command(ssh,"sudo apt install pipx")
        self.command(ssh,"pipx install poetry")
        self.command(ssh,"pipx ensurepath")
        self.command(ssh,"exec bash")
        self.command(ssh,"cd ~")
        self.command(ssh,"mkdir git")
        self.command(ssh,"cd git/")
        self.command(ssh,"git clone https://github.com/cirKITers/Quafel.git")
        self.command(ssh,"cd Quafel/")
        self.command(ssh,"poetry lock --no-update")
        self.command(ssh,"poetry install --without dev")
        self.close_ssh(ssh)
        
    def submit_simulation(self, 
            min_qubits: int, max_qubits: int, qubits_increment: int, qubits_type: str, 
            min_depth: int, max_depth: int, depth_increment: int, depth_type: str, 
            min_shots: int, max_shots: int, shots_increment: int, shots_type: str,
            quantum_framework: list[str], evaluations: int):
        ssh = self.connect_ssh()
        # self.command(ssh,"cd ~/git/Quafel/")
        
        list_frameworks: str = '["' + '","'.join(quantum_framework) + '"]'

        output, error = self.command(ssh,"cd ~/git/Quafel/ && grep -n 'frameworks' conf/base/parameters/data_generation.yml | cut -d ':' -f1")
        line: int = output.split('\n')[0]
        self.command(ssh,f"cd ~/git/Quafel/ && sed -i '{line}s/.*/  frameworks: {list_frameworks}/' conf/base/parameters/data_generation.yml")

        prepare_command: str = (f"cd ~/git/Quafel/ && /home/ubuntu/.local/bin/poetry run kedro run --pipeline prepare --params=data_generation.min_qubits={min_qubits},data_generation.max_qubits={max_qubits},data_generation.qubits_increment={qubits_increment},data_generation.qubits_type={qubits_type},"
            f"data_generation.min_depth={min_depth},data_generation.max_depth={max_depth},data_generation.depth_increment={depth_increment},data_generation.depth_type={depth_type},"
            f"data_generation.min_shots={min_shots},data_generation.max_shots={max_shots},data_generation.shots_increment={shots_increment},data_generation.shots_type={shots_type},"
            f"data_science.evaluations={evaluations}")

        output, error = self.command(ssh,prepare_command)
        if error: print("QUAFEL error"); return
        output, error = self.command(ssh,"cd ~/git/Quafel/ && /home/ubuntu/.local/bin/poetry run kedro run --pipeline measure --runner quafel.runner.MyParallelRunner")
        if error: print("QUAFEL error"); return
        output, error = self.command(ssh,"cd ~/git/Quafel/ && /home/ubuntu/.local/bin/poetry run kedro run --pipeline combine")
        if error: print("QUAFEL error"); return
        output, error = self.command(ssh,"cd ~/git/Quafel/ && /home/ubuntu/.local/bin/poetry run kedro run --pipeline visualize")
        if error: print("QUAFEL error"); return

        self.close_ssh(ssh)

    def submit_simulation_point(self, qubits: int, depth: int, shots: int, quantum_framework: list[str], evaluations: int):
        self.submit_simulation(qubits, qubits, 1, "linear", depth, depth, 1, "exp2", shots, shots+1, 1, "exp2", quantum_framework, evaluations)


    def connect_ssh(self):
        # Create an SSH client
        ssh = paramiko.SSHClient()
        # Automatically add the server's SSH key to known hosts
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            # Connect to the server
            ssh.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)
            print(f"Connected to {self.host}")
            return ssh
            
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")
        except paramiko.SSHException as sshException:
            print(f"Unable to establish SSH connection: {sshException}")
        except Exception as e:
            print(f"Exception in connecting to SSH server: {e}")

    def close_ssh(self, ssh):
        ssh.close()

    def command(self, ssh, command):
        # Execute the command
        print(f">> {command}")
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Read the command's output
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')


        #if output:
        print("<<\n", output)
        if error:
                print("Error<<\n", error)

        return output, error

if __name__ == "__main__":
    # SSH server details
    host = "193.196.39.170"
    port = 22
    username = "ubuntu"
    password = "123"
    
    # Execute the command on the remote server
    quafel = QUAFEL_API(host, port, username, password)

    quafel.submit_simulation_point(2, 4, 6, ["qiskit_fw"], 3)
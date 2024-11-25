#! /usr/bin/env python3
import subprocess
import tempfile
from netfilterqueue import NetfilterQueue
from scapy.all import *
import cryptography
import json


### Config ###
#Editor to use (must be in path)
editor= "vim"

# Create a temporary file with the content and open the editor
def input_via_editor(editor, content=""):
	with tempfile.NamedTemporaryFile(mode='w') as temp_file:
		if content:
			temp_file.write(content)
			temp_file.flush()
		try:
			subprocess.check_call([editor, temp_file.name])
		except subprocess.CalledProcessError as e:
			raise IOError("{} exited with code {}.".format(editor, e.returncode))
		with open(temp_file.name) as temp_file_2:
			return temp_file_2.read()

# Proccess intercepted packets
def interrupt_and_edit(pkt):
	'''
	global editor
	load_layer('tls')
	packet = TLS(pkt.get_payload())
	print(packet.load)
	#packet = IP(pkt.get_payload()) #if want to edit the payload only
	#b'E\x00\x00T\xc8\x1c@\x00@\x01\xc8\x83\xc0\xa8\xb2\xa8]\xb8\xd8\xff\x08\x00\xf0t\x00\x04\x00\x01\xb7\xa17f\x00\x00\x00\x00Y\xab\x00\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'
	#compute the equivalent scapy command
	#TLSEncryptedContent(load=b'E\x00\x00T\xca\xc0@\x00@\x01\xc5\xdf\xc0\xa8\xb2\xa8]\xb8\xd8\xff\x08\x00\x9f<\x00\t\x00\x01\xdd\xe67f\x00\x00\x00\x00\x81\x99\x03\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567')
	scapy_command = packet.command()
	
	#let the user edit the scapy command
	user_defined_command = input_via_editor(editor, scapy_command)
	#convert to packet
	user_defined_packet = eval(user_defined_command)
        
	#force update of the checksum
	del user_defined_packet[TLS].chksum
	#update the payload
	pkt.set_payload( raw(user_defined_packet) )
	
	#forward the packet
	pkt.accept()
	'''
	print("Accepted a new packet...")
	ip = IP(pkt.get_payload())
	if not ip.haslayer("Raw"):
		print("fi1")
		pkt.accept()
	else:
		tcpPayload = ip["Raw"].load
		print("2")
		if tcpPayload[0] == 0x16 and tcpPayload[1] == 0x03 and tcpPayload[2] == 0x03:
			print("real")
			# we located the Handshake
			msgBytes = pkt.get_payload()       # msgBytes is read-only, copy it
			msgBytes2 = [b for b in msgBytes]
			msgBytes2[54] = 0x01
			pkt.set_payload(bytes(msgBytes2))
			pkt.accept()                                       # drop TLS_RSA_WITH_AES_256_CBC_SHA
			print("4")
		else:
			pkt.accept()
			print("5")
	print("finish")


if __name__=="__main__":

	nfqueue = NetfilterQueue()

	#Bind to the same queue number (here 2)
	nfqueue.bind(2, interrupt_and_edit)
	
	#run (indefinetely)
	try:
		nfqueue.run()
	except KeyboardInterrupt:
		print('Quiting...')
	nfqueue.unbind()
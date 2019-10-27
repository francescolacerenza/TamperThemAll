import argparse
from itertools import combinations, permutations
import json
from ast import literal_eval
from os import getcwd
from glob import glob
from re import findall

# importing all the tampering scripts (credits to WhatWaf )
from tampers import *

# given a tampering chain it applies the requested tampers in the list order
def tamperIt(chain):
	payload=Payload
	for tamper_script in chain:
		try:
			# limiting randomcomments usage on large payloads because it's useless and it causes Recursion limits exception
			if tamper_script=="randomcomments" and len(payload) >=40: pass
			else:
				payload=globals()[tamper_script](payload)
		except Exception as e:
			print("[X] There was an error with the tampering script "+tamper_script+":\n"+str(e))
	tampered.append(payload)
	outjson[payload]=chain

# given a basePayload and a max_tampers_chaining_len this function operates the combination and permutation phase to create all the possible 
# tampering chains and then uses the function tamperIt() in order to tamper the base payload with the created chains 
def tampersMixer(basePayload,chainLen):
	chains=[]
	# doing combinations and internal permutations for each chain len till the max chain len specified by the user
	for n in range(1,chainLen+1):
		for combination in combinations(scripts,n):
			for permutation in permutations(combination):
				chains.append(list(permutation))
	print("[*] Number of total payloads (duplicates included): "+str(len(chains)))
	print("[*] Tampering Chains Phase")
	while len(chains)>0:
		tamperIt(chains.pop())

if __name__ == "__main__":
	global Payload,outName,tampered,outjson,scripts
	outjson={}
	tampered=[]

	banner="""

                                                             %&%#%&%.                                                           
                                                        /################                                                    
                                                      ########%&&&%%#######                                                    
                                                    ,#%%%%&@@@@&&@@@@@&%#%%#/                                                    
                                                   /%(((#%&&%&&&&&&&&&&%%###%/                                               
                                                   #/////#&@@@@@@@@@@@@#(////#                                                   
                                                  .#/////#&@@@@@@@@@@@@%(////%,                                                  
    PAYLOADS TAMPERER                              ,%/////#&&&&&@@@&&&&(////%,                                                
    FOR WAF BYPASSING                              #/////(%&&&&&&&&&&&%#(////#                                                 
                                                   (#///((%%&&&&&&&&&&%#((//##                                                   
    Author: Francesco Lacerenza                    ,%///((#%&&&&&&&&&%%#((//%,                                                  
                                                    #///((#%%&&&&&&&%%%#((//#                                                  
                                                    (#//((#%%%%&&%&%%%##((/%#                                                    
                                                     %//((#%%%%%%%%%%%##((/%                                                     
                                                     #//((#%%%%%%%%%%%##(((#                                                 
                                                     ,#(((#%%%%%%%%%%%##((%*                                                     
                                                      #/((##%%%%%%%%%%##((#                                                       
                                                      #(((##%%&&&&&&%%##((#                                                         
                                                       ,#//(#&&&&@&&&(((#,                                                       
                                                      ,#///(@@@@@@@@@#(//#,                                                     
                                                      #(//(#%%%&&&&&&%((/(#                                                     
                                                     #%%%%###%%%&&%%###%%%%#                                                 
                                                   (#####%%&&@@@@@@@&&%%#%###(                                              
                                                 ,%/((((#%&&&&@@@@@@@&&(((((%(                                          
                                                       ###%%%%%%%%%%%%%%##                                                   
                                                       /((##%%%%%%%%%%##((                                            
                                               ....(%%%//(##%%%&&&%%%%#((/#####,,                                           
                                           ...       ,,** _______________ **,,       ...                                         
                                             *.........**|TAMPER THEM ALL|**.........*                                            
                                              *,,,,,,,,** _______________ **,,,,,,,,*
                                               **//(#%%#(/////*****///////(#%%%#(//*

______________________________________________________________T.T.A._____________________
"""
	#print(banner)

	# loading in a list all the tampering scripts names located in the /tampers dir, names needed for the function call with globals()
	scripts = list([str(findall("[ \w-]+?(?=\.)",script)[0]) for script in glob(getcwd()+"/tampers/*.py")])
	scripts.remove("__init__")


	parser = argparse.ArgumentParser()
	parser.add_argument("-p","--payload",type=str,help="""Base payload between single or double quotes (depends on which kind of quotes the payload contains)""")
	parser.add_argument("-l","--chainLen",type=int,help="""max number of tampering methods chained in a single tampering chain.\n""")
	parser.add_argument("-c","--chain",type=str,help="""comma separated tampering chain, order matters (left to right)\n""")
	parser.add_argument("-f","--tampersList",type=str,help="""define your own tamper list to reduce the N """)
	parser.add_argument("-o","--outFile",type=str,help="""output payloads list name""")
	parser.add_argument("-s","--search",type=str,help="""search in a .association file what chain produced a certain payload, also print(the 'payload evolution' for further investigation. ex. -s bypassing/payloadsFile,file.associations """)
	parser.add_argument("-a","--allTampers",action='store_true',help="""print(available tamper scripts list""")

	# parsing user input and handling each input combination 
	args = parser.parse_args()

	# printing out all the available tampering scripts
	if args.allTampers:
		for el in scripts: print(el)
		exit(0)
	
	# setting global Payload
	if args.payload: Payload=args.payload

	# handling tampers selection through input file
	if args.tampersList:
		print("[*] Loading Tampering Scripts Pool from file")
		with open(args.tampersList,"r") as f:
			scripts=f.read().splitlines()

	# handling payload list generation usage option given the payload, max chaining len and output file
	if args.payload and args.chainLen and args.outFile:
		outName=args.outFile
		print("[*] Combination and Permutation Phase")
		# Calling main tampering function that saves the created payloadlist in tampered
		tampersMixer(Payload,args.chainLen)
		# removing duplicates
		tampered=list(set(tampered))

		print("[*] Writing "+str(len(tampered))+" generated payloads in "+args.outFile+".payloadlist (duplicates removed)")
		with open(outName+".payloadlist","w") as f:
			for payload in tampered:
				f.write(payload+"\n")
		print("[*] Writing associations payload:chain in "+args.outFile+".associations "+" for further checks")
		with open(outName+".associations","w") as f:
			# writing base payload as first element in the association file in order to get it and print the payload evolution in search mode
			f.write(Payload+"\n")
			# writing couples : tamperedPayload-usedTamperingChain
			for el in outjson:
				f.write(el+" , "+str(outjson[el])+"\n")
		print("[*] Done.")
		exit(0)

	# handling single tamper option
	if args.payload and args.chain:
		chain=[]
		chain.append(args.chain.split(","))
		while len(chain)>0:
			tamperIt(chain.pop())
		print(tampered[0])
		exit(0)

	# handling search mode in which is possible to match the bypassing payloads with their relative tampering chains, also prints each bypassing payload evolution	
	if args.search:
		arguments=args.search.split(",")
		with open(getcwd()+"/"+arguments[1],"r") as f:
			associations=f.read().splitlines()
		Payload=associations[0]
		del associations[0]
		with open(arguments[0],"r") as f:
			bypassed_payloads=f.read().splitlines()
		print("[*] Original Payload referred in the provided associations file : "+Payload)
		print("______________________________________________________________________________________________________________________________________________________")
		print
		for el in associations:
			for bypassed_payload in bypassed_payloads:
				if bypassed_payload in el:
					chain=str(el.split(" , ")[1])
					print("[*] Association Found-> chain :"+chain+" bypassing payload :"+str(el.split(" , ")[0]))
					print("[-] Printing Payload Evolution:")
					
					chain=literal_eval(chain)
					payloadBackup=Payload
					for tamper in chain:
						print("------------------------------------------------------------------------------------------------------------------------------------------------")
						step=[]
						step.append(tamper)
						tamperIt(step)
						Payload= tampered.pop()
						print(Payload)
					Payload=payloadBackup
					print("______________________________________________________________________________________________________________________________________________________")
		exit(0)
	else:
		print("[X] Insufficient params")
		print
		parser.print_help()
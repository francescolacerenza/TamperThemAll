# TamperThemAll
A tampered payload generator to Fuzz Web Application Firewalls for Testing Fun and, why not, Bypassing.

### [*] Know 'How and Why'
TTA takes in input a string representing your payload, it doen't matter what kind of vulnerability it exploits (SQLi, XSS, CMD Injection etc.), and gives back a payloads set with the input string chain-tampered in all the possible combinations and permutations.
It's also created an associations file used to find out what chain produced a certain payload, useful function for the post exploitation phase in which you have a set of bypassing payloads and no idea of where they come from.
Detailed Concept explained in the Medium article:
URL

### [*] CMD Options
```
  -h, --help            show this help message and exit
  -p PAYLOAD, --payload PAYLOAD
                        Base payload between single or double quotes (depends
                        on which kind of quotes the payload contains)
  -l CHAINLEN, --chainLen CHAINLEN
                        max number of tampering methods to chaining.
  -c CHAIN, --chain CHAIN
                        comma separated tampering chain, order matters (left
                        to right)
  -f TAMPERSLIST, --tampersList TAMPERSLIST
                        define your own tamper list to reduce the N
  -o OUTFILE, --outFile OUTFILE
                        output payloads list name
  -s SEARCH, --search SEARCH
                        search in a .association file what chain produced a
                        certain payload, also print(the 'payload evolution'
                        for further investigation. ex. -s
                        bypassing/payloadsFile,file.associations
  -a, --allTampers      print(available tamper scripts list
```
### [*] Usage Examples
##### Creating a Tampered payloads list using : basePayload,max_tamperingChain_len,outputFileName
![unsageNormal](https://user-images.githubusercontent.com/25546186/67636036-964a9d80-f8cc-11e9-80f9-364f619d862e.png)

##### Creating a Tampered payloads list with a restricted tampers list using : tampersListFile,basePayload,max_tamperingChain_len,outputFileName

##### Single tamperChain using : basePayload,custom_tamperChain

##### Search mode of what chains produced the bypassing payloads
This mode is used when you have bypassed the WAF using the produced payloadList and want to find out which chains produced the bypassing payloads. Useful to produce a better PoC or for reasearch purposes about the WAF Normalization Function.
![searchMode](https://user-images.githubusercontent.com/25546186/67636050-b8442000-f8cc-11e9-98d6-e451acd4dc06.png)


### [*] Call for Contributors
Everyone interested in the development of this tool, please contact me on twitter or linkedin.

**TODO LIST**:

**-** Add new Tampering Scripts. To add them you simply have to create a file containing the function (named as the file) and add it in the tampers folder. You also have to add the following line in the __init__.py under tampers/ dir:
```from tampers.yourTamperFileName import *```

**-** Add an option to specify which kind of vulnerability you want to exploit with the basePayload in order to create separate tampers lists for each vulnerability (this will reduce the number of payloads and requests sent to the WAF, the less you send the less you annoy)

## A special thanks to WhatWaf
It is a tool by EkultekThe used to detect a firewall on a web application, and attempting to detect a bypass.
The Available tampering scripts used in this tool are taken from his tool.
Check it out here: https://github.com/Ekultek/WhatWaf
### [*] Author
Lacerenza Francesco - Systems and Networks Security Student.
twitter: [@lacerenza_fra](https://twitter.com/lacerenza_fra)
linkedin: [lacerenzafrancesco](https://www.linkedin.com/in/francesco-lacerenza/)

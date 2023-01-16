# joinstr

 ### coinjoin implementation using nostr
 
 ![image](https://user-images.githubusercontent.com/94559964/185734286-bc5f06ff-6a46-4669-93bb-5d6ef92631fb.png)


 **Requirements:**

 - [python-nostr](https://github.com/jeffthibault/python-nostr)
 - Bitcoin Core

 **Usage:**
 
 **CLI**

 1. Run `python joinstr-cli.py` and enter descriptor for one of the inputs.
 2. Script will check inputs for this round in every 30 seconds and register a new adddress for output once 5 inputs are registered.
 3. Similar check happens every 30 seconds for outputs. Last peer should create a PSBT.
 4. Unsigned PSBT will be printed and signed by wallet with `walletprocesspsbt` RPC.
 5. Script will check signed PSBTs and last peer should finalize coinjoin transaction once 5 signed PSBTs are received.
 6. Coinjoin transaction will be broadcasted and txid will be printed.
 
 **GUI**
 
 1. Clone repo so that templates are available for using `joinstr-web`
 2. Run `joinstr-web.py` and open http://127.0.0.1:5000/ in browser.
 3. Select one of the inputs from wallet and submit for input registration.
 4. A new address will be registered for output once 5 inputs are registered for this round.
 5. PSBT will be created and shared.
 
 _GUI is a work in progress and other phases (signing PSBT and broadcasting) are left._

**Examples:**

CLI

```
List of utxos in wallet:

wpkh([53830dca/84'/1'/0'/0/0]02449be5fb74725255eeeb50eba930fa87705f21e99d13cd710cf2c1f21153c808)#x2hyyeg5

Enter descriptor for the input registration: wpkh([53830dca/84'/1'/0'/0/0]02449be5fb74725255eeeb50eba930fa87705f21e99d13cd710cf2c1f21153c808)#x2hyyeg5

event id:  bcbbe62d75d99fed73f1e50ac58a38d1840b658951893e63c0322b378d7d56f0

```
```
tb1qhxrp4zl54ul0twtyz0gury5399q7z0kvqqrl6m registered for output

event id: 9449c9065bef356d21507a98f88b028b17fc1c49eb195c8d4420604fcaaef041
```
```
Unsigned PSBT: cHNidP8BAP1yAQIAAAAFtMaoJYcXvOG5L3Yaz3YyS7gIt4h5/zzOrRRS3hrVvwoAAAAAAP////+o83geaSm4L76KToIUl5MiZqLAUbIDJLq6DWrjP/3b8AEAAAAA/////zEF3CXIvVHpIa7No1s1yg+KtyOfXTRSyWnOdXMfzcDwAQAAAAD/////wMa4XAgnU+39Ien+KG9rYtv8bLMNYakmZyY/QFfwLRcAAAAAAP/////5M42ID6uLmQTb2tnFHnN7UMpnDD25uN8ZX7A+GNSM3QEAAAAA/////wV4xwEAAAAAABYAFLmGGov0rz71uWQT0cGSkSlB4T7MeMcBAAAAAAAWABSc0/FM6Hdbdxh10IJkYOklVFWqjnjHAQAAAAAAFgAUPSZKe/w6PT6qIF+WhL4wHaFymjd4xwEAAAAAABYAFMx0rxYlpPWB3NFry4Ctk2eVi/UNeMcBAAAAAAAWABSzc4xK0VTfvjK0MHXrAUFLYgYnOgAAAAAAAAAAAAAAAAAAAA==

```
```
Signed PSBT: cHNidP8BAP1yAQIAAAAFtMaoJYcXvOG5L3Yaz3YyS7gIt4h5/zzOrRRS3hrVvwoAAAAAAP////+o83geaSm4L76KToIUl5MiZqLAUbIDJLq6DWrjP/3b8AEAAAAA/////zEF3CXIvVHpIa7No1s1yg+KtyOfXTRSyWnOdXMfzcDwAQAAAAD/////wMa4XAgnU+39Ien+KG9rYtv8bLMNYakmZyY/QFfwLRcAAAAAAP/////5M42ID6uLmQTb2tnFHnN7UMpnDD25uN8ZX7A+GNSM3QEAAAAA/////wV4xwEAAAAAABYAFLmGGov0rz71uWQT0cGSkSlB4T7MeMcBAAAAAAAWABSc0/FM6Hdbdxh10IJkYOklVFWqjnjHAQAAAAAAFgAUPSZKe/w6PT6qIF+WhL4wHaFymjd4xwEAAAAAABYAFMx0rxYlpPWB3NFry4Ctk2eVi/UNeMcBAAAAAAAWABSzc4xK0VTfvjK0MHXrAUFLYgYnOgAAAAAAAQBxAgAAAAG+qpMXZCy6tBuUlgo8JD0GVXKp60FkhwDeg2sF1fkFkwMAAAAA/f///wLo9wEAAAAAABYAFFfLA5xarC/w/SxeMDQ5tuXrYJLUWwMAAAAAAAAWABRfPf//hwMjHB4OKj87cU19XOSh7yOWAQABAR/o9wEAAAAAABYAFFfLA5xarC/w/SxeMDQ5tuXrYJLUAQhrAkcwRAIgOIhLoC5348U8YkEr4GU1K4yWskIOEXgW4Wsk/W2cR7ICIEJXqtOuDJ5CkwrSuwJLWtzab4dslbN3KuL/pyooMnOCASECRJvl+3RyUlXu61DrqTD6h3BfIemdE81xDPLB8hFTyAgAAAAAACICA77Cnd6o3kr0yc+91eabpOn5igs/MUMbudNYSS6oyMWMGFODDcpUAACAAQAAgAAAAIAAAAAAFAAAAAAAAAAA

event id: 5846b6e6902f3c5a43496d7d9785ed62444aa74963f03c33d637d8b09ee7a139
```
```
Coinjoin tx: 75e490b10b15a6a0422f25ff66ad98ef70390c8fecaac02712705dce8cc3564b

event id: 9b5d4bf279b59e2b6e539e683fba83da72dce2b640360aa95db1b1400be93190
```


GUI

![image](https://user-images.githubusercontent.com/94559964/212611546-3151648b-9171-4237-8443-1cd5d74451ff.png)

![image](https://user-images.githubusercontent.com/94559964/212611743-27a07966-de0e-4761-b062-817be13bf138.png)

**TO DO:**

1. Send each request using new tor circuit.
2. Use NIP 38/48 (encrypted channels) to improve privacy and security.
3. Break UTXOs in pool denominations before coinjoin.
5. Do not allow registering different types of inputs for a round.
6. Use NIP 9 to delete events after round is completed
7. Create an Android app.

:green_circle: Matrix room: #joinstr:matrix.org  
:green_circle: Nostr: 1440000bytes[at]nostr.boats | npub1v6qjdzkwgaydgxjvlnq7vsqxlwf4h0p4j7pt8ktprajd28r82tvs54nzyr

---

Do not use this script for mainnet as there are several bugs in the code and lot of scope for improvement.

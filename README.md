# joinstr

 ### coinjoin implementation using nostr (proof of concept)
 
 ![image](https://user-images.githubusercontent.com/94559964/185734286-bc5f06ff-6a46-4669-93bb-5d6ef92631fb.png)


 **Requirements:**

 - [python-nostr](https://github.com/jeffthibault/python-nostr)
 - Bitcoin Core

 **Usage:**

 1. Run `python coinjoin.py` and enter descriptor for one of the inputs.
 2. Script will check inputs for this round in every 30 seconds and register a new adddress for output once 5 inputs are registered.
 3. Unsigned PSBT will be printed and signed by wallet with `walletprocesspsbt` RPC.
 4. Script will check signed PSBTs and finalize coinjoin transaction once 5 signed PSBTs are received.
 5. Coinjoin transaction will be broadcasted and txid will printed.

 Note: Every step is followed by an eventid which represents the id for event published using python-nostr and could be checkedusing [nostr gateway](https://nostr.com/).

**Example:**

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

event id: 976744b38fa9343fb79e1b5215512ead6ee08e5890d79a201fc5b872f6de4eba
```
```
Signed PSBT: cHNidP8BAP1yAQIAAAAFtMaoJYcXvOG5L3Yaz3YyS7gIt4h5/zzOrRRS3hrVvwoAAAAAAP////+o83geaSm4L76KToIUl5MiZqLAUbIDJLq6DWrjP/3b8AEAAAAA/////zEF3CXIvVHpIa7No1s1yg+KtyOfXTRSyWnOdXMfzcDwAQAAAAD/////wMa4XAgnU+39Ien+KG9rYtv8bLMNYakmZyY/QFfwLRcAAAAAAP/////5M42ID6uLmQTb2tnFHnN7UMpnDD25uN8ZX7A+GNSM3QEAAAAA/////wV4xwEAAAAAABYAFLmGGov0rz71uWQT0cGSkSlB4T7MeMcBAAAAAAAWABSc0/FM6Hdbdxh10IJkYOklVFWqjnjHAQAAAAAAFgAUPSZKe/w6PT6qIF+WhL4wHaFymjd4xwEAAAAAABYAFMx0rxYlpPWB3NFry4Ctk2eVi/UNeMcBAAAAAAAWABSzc4xK0VTfvjK0MHXrAUFLYgYnOgAAAAAAAQBxAgAAAAG+qpMXZCy6tBuUlgo8JD0GVXKp60FkhwDeg2sF1fkFkwMAAAAA/f///wLo9wEAAAAAABYAFFfLA5xarC/w/SxeMDQ5tuXrYJLUWwMAAAAAAAAWABRfPf//hwMjHB4OKj87cU19XOSh7yOWAQABAR/o9wEAAAAAABYAFFfLA5xarC/w/SxeMDQ5tuXrYJLUAQhrAkcwRAIgOIhLoC5348U8YkEr4GU1K4yWskIOEXgW4Wsk/W2cR7ICIEJXqtOuDJ5CkwrSuwJLWtzab4dslbN3KuL/pyooMnOCASECRJvl+3RyUlXu61DrqTD6h3BfIemdE81xDPLB8hFTyAgAAAAAACICA77Cnd6o3kr0yc+91eabpOn5igs/MUMbudNYSS6oyMWMGFODDcpUAACAAQAAgAAAAIAAAAAAFAAAAAAAAAAA

event id: 5846b6e6902f3c5a43496d7d9785ed62444aa74963f03c33d637d8b09ee7a139
```
```
Coinjoin tx: 75e490b10b15a6a0422f25ff66ad98ef70390c8fecaac02712705dce8cc3564b

event id: 9b5d4bf279b59e2b6e539e683fba83da72dce2b640360aa95db1b1400be93190
```

**TO DO:**

1. Send each request using new tor circuit.
2. Create a NIP to support sharing a random secret betwen clients and relay for a round.
3. Break UTXOs in pool denominations before coinjoin if amount exceeds pool denomination by more than 50000 sats.
5. Do not allow registering different types of inputs for a round.
6. Create an Android app.

Do not use this script for mainnet as there are several bugs in the code and lot of scope for improvement.

:information_source: Feel free to create issues, pull request and contact me by email at alicexbt[at]protonmail[dot]com

import requests
import time
import json
import string
import random
from nostr.event import Event
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.filter import Filter, Filters
from nostr.key import PrivateKey

url = "http://127.0.0.1:<PORT>/wallet/<WALLET_NAME>"

'''
Change RPC credentials
'''

headers = {
    'Authorization': 'Basic dXNlcjpwYXNz',
    'Content-Type': 'text/plain'
}

def getkey():

    private_key = PrivateKey()
    public_key = private_key.public_key

    return public_key,private_key

def get_random_string(length):

    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters) for i in range(length))

    return random_str

def publish():

    relay_manager = RelayManager()
    relay_manager.add_relay("wss://relay.nostr.info")
    relay_manager.open_connections()
    time.sleep(2)

    public_key, private_key = getkey()

    event = Event(public_key.hex(), json.dumps(data), kind=892)
    event.sign(private_key.hex())
    eventid = event.id

    message = json.dumps([ClientMessageType.EVENT, event.to_json_object()])
    relay_manager.publish_message(message)
    time.sleep(1)
    relay_manager.close_connections()

    return eventid


def getevents():

    random_id = get_random_string(10)

    filters = Filters([Filter(kinds=[892])])
    subscription_id = random_id
    request = [ClientMessageType.REQUEST, subscription_id]
    request.extend(filters.to_json_array())

    relay_manager = RelayManager()
    relay_manager.add_relay("wss://relay.nostr.info")
    relay_manager.add_subscription(subscription_id, filters)
    relay_manager.open_connections()
    time.sleep(1.25)

    message = json.dumps(request)
    relay_manager.publish_message(message)
    time.sleep(1)

    desc_list = []
    output_list =[]
    event = {}
    upsbt = []
    spsbt = []

    i = 0

    while relay_manager.message_pool.has_events():
        event_msg = relay_manager.message_pool.get_event()
        event = json.loads(event_msg.event.content)
        if event_type == "input":
            try:
                desc_list.append(event['descriptor'])
            except:
                continue
        elif event_type == "output":
            try:
                output_list.append(event['address'])
            except:
                continue
        elif event_type == "unsigned":
            try:
                upsbt.append(event['unsigned_psbt'])
            except:
                    continue
        elif event_type == "signed":
            try:
                spsbt.append(event['signed_psbt'])
            except:
                continue

        i = i + 1

    relay_manager.close_connections()

    return event,output_list,desc_list,upsbt,spsbt,i

def listunspent():

    payload = "{\"jsonrpc\": \"1.0\", \"id\": \"joinstr\", \"method\": \"listunspent\"}"
    response = requests.request("POST", url, headers=headers, data=payload)

    i =0
    for i in range(0,len(response.json()['result'])):
        desc = response.json()['result'][i]['desc']
        print(desc)
        i = i + 1

def getaddress():
    payload = "{\"jsonrpc\": \"1.0\", \"id\": \"joinstr\", \"method\": \"getnewaddress\"}"
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()['result']

def createtx():

    payload = "{\"jsonrpc\": \"1.0\",\r\n \"id\": \"joinstr\",\r\n  \"method\": \"createpsbt\",\r\n  \"params\": [[{\"txid\":\"" + str(round_tx_list[0]) + "\",\"vout\":" + str(round_vout_list[0]) + "},{\"txid\":\"" + str(round_tx_list[1]) + "\",\"vout\":" + str(round_vout_list[1]) + "}, {\"txid\":\"" + str(round_tx_list[2]) + "\",\"vout\":" + str(round_vout_list[2]) + "},{\"txid\":\"" + str(round_tx_list[3]) + "\",\"vout\":" + str(round_vout_list[3]) + "},{\"txid\":\"" + str(round_tx_list[4]) + "\",\"vout\":" + str(round_vout_list[4]) + "}],\r\n    [{\"" + str(round_output_list[0]) +"\":" + str(postmix_ov) + "},\r\n    {\"" + str(round_output_list[1]) + "\":" + str(postmix_ov) + "},\r\n    {\"" + str(round_output_list[2]) + "\":" + str(postmix_ov) + "},\r\n    {\"" + str(round_output_list[3]) + "\":" + str(postmix_ov) + "},\r\n    {\"" + str(round_output_list[4]) + "\":" + str(postmix_ov) + "}]]\r\n}"
    response = requests.request("POST", url, headers=headers, data=payload)

    upsbt = response.json()['result']

    return upsbt

def getutxoinfo():

    payload = "{\"jsonrpc\": \"1.0\",\r\n \"id\": \"joinstr\",\r\n  \"method\": \"scantxoutset\",\r\n  \"params\": [\"start\", [\"" + str(round_desc_list[j]) + "\"]]\r\n}"
    response = requests.request("POST", url, headers=headers, data=payload)

    txid = response.json()['result']['unspents'][0]['txid']
    vout = response.json()['result']['unspents'][0]['vout']
    amount = response.json()['result']['total_amount']

    return txid,vout,amount

def signtx():

    payload = "{\"jsonrpc\": \"1.0\",\r\n \"id\": \"joinstr\",\r\n  \"method\": \"walletprocesspsbt\",\r\n  \"params\": [\"" + str(round_upsbt) + "\"]\r\n}"
    response = requests.request("POST", url, headers=headers, data=payload)

    signed_psbt = response.json()['result']['psbt']

    return signed_psbt


def checkinputs():

    desc_list = []
    round_desc_list = []

    time.sleep(30)

    event_type = "input"
    event,output_list,desc_list,upsbt,spsbt,num_i = getevents()

    if num_i % 5 !=0 or num_i == 0:
        checkinputs()
    else:
        for k in range(0,5):
            if desc_list[k] not in round_desc_list:
                round_desc_list.append(desc_list[k])

        return round_desc_list,num_i

def checkoutputs():

    output_list = []
    round_output_list = []

    time.sleep(30)

    event_type = "output"
    event,output_list,desc_list,upsbt,spsbt,num_o = getevents()

    if num_o % 5 !=0 or num_o == 0:
        checkoutputs()
    else:
        for k in range(0,5):
            round_output_list.append(output_list[k])

        return round_output_list,num_o

def checkupsbt():

    upsbt = []
    round_upsbt =[]

    time.sleep(30)

    event_type = "unsigned"
    event,output_list,desc_list,upsbt,spsbt,num_utx = getevents()

    if num_utx == 0:
        checkupsbt()
    else:
        round_upsbt = upsbt[0]

        return round_upsbt,num_utx

def combinetx():

    payload = "{\"jsonrpc\": \"1.0\",\r\n \"id\": \"joinstr\",\r\n  \"method\": \"combinepsbt\",\r\n  \"params\": [[\"" + str(round_spsbt_list[0]) + "\",\"" + str(round_spsbt_list[1]) + "\",\"" + str(round_spsbt_list[2]) + "\",\"" + str(round_spsbt_list[3]) + "\",\"" + str(round_spsbt_list[4]) + "\"]]\r\n}"
    response = requests.request("POST", url, headers=headers, data=payload)

    combined_psbt = response.json()['result']

    return combined_psbt


def checkspsbt():

    spsbt_list = []
    round_spsbt_list =[]

    time.sleep(30)

    event_type = "signed"
    event,output_list,desc_list,upsbt,spsbt_list,num_stx = getevents()

    if num_stx % 5 !=0 or num_stx == 0:
        checkspsbt()
    else:
        for k in range(0,5):
            round_spsbt_list.append(spsbt_list[k])

        return round_spsbt_list,num_stx


def finalizetx():

    payload = "{\"jsonrpc\": \"1.0\",\r\n \"id\": \"joinstr\",\r\n  \"method\": \"finalizepsbt\",\r\n  \"params\": [\"" + str(combinedtx) + "\"]\r\n}"
    response = requests.request("POST", url, headers=headers, data=payload)

    final_tx = response.json()['result']['hex']

    return final_tx


def broadcast():

    payload = "{\"jsonrpc\": \"1.0\",\r\n \"id\": \"joinstr\",\r\n  \"method\": \"sendrawtransaction\",\r\n  \"params\": [\"" + str(finaltx) + "\"]\r\n}"
    response = requests.request("POST", url, headers=headers, data=payload)

    release_txid = response.json()['result']

    return release_txid



if __name__=="__main__":


    # Input registration

    print("List of utxos in wallet:\n")
    utxo_list = listunspent()
    descriptor = input('\nEnter descriptor for the input registration: ')

    data = {}
    data["descriptor"] = descriptor
    data["type"] = "input"

    eventid = publish()
    print("\nevent id: ", eventid)

    # Output registration


    while True:
        event_type = "input"
        try:
            round_desc_list,num_i = checkinputs()
        except:
            continue
        break

    event_type = "output"
    event,output_list,desc_list,upsbt,spsbt,num_o = getevents()

    if num_o == 4 or (num_o - 4) % 5 == 0 :
        last_bool = True
    else:
        last_bool = False

    address = getaddress()

    data = {}
    data["address"] = address
    data["type"] = "output"
    data["last"] = last_bool

    eventid = publish()
    print("\n" + address + " registered for output")
    print("\nevent id:", eventid)

    '''
    TODO: Check outputs for `last_bool` before proceeding with next step
    '''

    while True:
        event_type = "output"
        try:
            round_output_list,num_o = checkoutputs()
        except:
            continue
        break

    # Create and publish tx

    if last_bool == True:

        j=0
        input_sum = 0
        round_tx_list =[]
        round_vout_list =[]

        while j<5:
            round_tx,round_vout,amt = getutxoinfo()

            if amt > 0.001 and amt < 0.0015:
                input_sum = input_sum + amt
                round_tx_list.append(round_tx)
                round_vout_list.append(round_vout)

                j=j+1
            else:
                print("Error: invalid input amount")
                break

        postmix_ov = (input_sum - 0.00001)/5


        data = {}
        data["unsigned_psbt"] = createtx()

        eventid = publish()

        upsbt = str(data["unsigned_psbt"])

        print("\nUnsigned PSBT: " + upsbt)
        print("\nevent id:", eventid)

    #Sign and publish tx

    while True:
        event_type = "unsigned"
        try:
            round_upsbt,num_utx = checkupsbt()
        except:
            continue
        break

    event_type = "signed"
    event,output_list,desc_list,upsbt,spsbt,num_stx = getevents()

    if num_stx == 4 or (num_stx - 4) % 5 == 0 :
        last_bool = True
    else:
        last_bool = False

    data = {}
    data["signed_psbt"] = signtx()
    data['last'] = last_bool

    spsbt = str(data["signed_psbt"])

    eventid = publish()

    print("\nSigned PSBT: " + str(spsbt))
    print("\nevent id:", eventid)

    # Combine, finalize and broadcast transaction

    '''
    TODO: Only do this step if we signed the PSBT last
    '''

    while True:
        event_type = "signed"
        try:
            round_spsbt_list,num_stx = checkspsbt()
        except:
            continue
        break

    combinedtx = combinetx()
    finaltx = finalizetx()

    data = broadcast()
    eventid = publish()

    print("\nCoinjoin tx: " + str(data))
    print("\nevent id:", eventid)

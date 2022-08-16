from basic import *
from wToken import wToken
from decouple import config
        

def main():

    (_wallet, _wallet_address) = wallet_import_mnemonic(1)
    connector  = connect(1)
    wDHN = wToken(connector, "build_static\DHN.json", "build\contracts\wDHN.json")
    wDHN.set_wToken_address()
    return connector, _wallet, _wallet_address, wDHN

def unwrap(connector,
           _wallet, _wallet_address,
           wDHN):

    wDHN.unwrap_Token(
                _wallet, _wallet_address
                )

def wrap(connector,
           _wallet, _wallet_address,
           wDHN):

    wDHN.wrap_Token(
                _wallet, _wallet_address
                )

def deploy_contract(connector,
                    _wallet, _wallet_address,
                    wDHN):

    wDHN.deploy_wToken(_wallet)



(connector, _wallet, _wallet_address, wDHN) = main()
wDHN.get_wallet_balance(_wallet_address)
unwrap(connector,
           _wallet, _wallet_address,
           wDHN)
wDHN.get_wallet_balance(_wallet_address)

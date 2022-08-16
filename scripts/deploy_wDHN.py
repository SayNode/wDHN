from basic import *
from wToken import wToken
from decouple import config


def main():

    (_wallet, _wallet_address) = wallet_import_mnemonic(1)
    connector  = connect(1)
    wDHN = wToken(connector, "build_static\DHN.json", "build\contracts\wDHN.json")
    return connector, _wallet, _wallet_address, wDHN

#
#Script
#
(connector, _wallet, _wallet_address, wDHN) = main()

#wDHN.deploy_wToken(_wallet)
wDHN.set_wToken_address()
wDHN.get_wallet_balance(_wallet_address)

wDHN.wrap_Token(
                _wallet, _wallet_address
                )

wDHN.get_wallet_balance(_wallet_address)

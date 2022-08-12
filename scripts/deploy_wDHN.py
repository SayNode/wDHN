from basic import *
import wToken

def main():

    (_wallet, _wallet_address) = wallet_import_mnemonic(2)
    connector  = connect(1)
    wDHN = wToken(connector, "build_static\DHN.json", "build\contracts\wDHN.json")
    wDHN.deploy_wToken(_wallet)
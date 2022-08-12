from basic import *
import wToken

def main():

    (_wallet, _wallet_address) = wallet_import_mnemonic(2)
    connector  = connect(1)
    wDHN = wToken(connector, Token_build_dir, wToken_build_dir)
    wDHN.deploy_wToken(_wallet)
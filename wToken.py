from traceback import print_tb
from thor_requests.contract import Contract
from decouple import config
import time

class wToken:

    def __init__(self, connector, Token_build_dir, wToken_build_dir):

        self.connector =connector
        self._contract_Token = Contract.fromFile(Token_build_dir)
        self.Token_contract_address=config('Token_contract_address')
        self._contract_wToken = Contract.fromFile(wToken_build_dir)

    def set_wToken_address(self):
        self.wToken_contract_address=config('wToken_contract_address')
    # 
    # Deploy wToken contract 
    #

    def deploy_wToken(self, testwallet):

        res = self.connector.deploy(testwallet, self._contract_wToken, ['address'],[self.Token_contract_address])
        time.sleep(15)
        
        wToken_contract_address = self.connector.get_tx_receipt(res['id'])['outputs'][0]['contractAddress']

        print("Wrapped Token contract was deployed at:" + str(wToken_contract_address))

        return self._contract_wToken, wToken_contract_address

    #   
    # Get wallet balances, we use "call" in order to not waste any gas 
    #
    def wallet_balance(self, _contract_Token, Token_contract_address, _wallet_address):

        balance_one = self.connector.call(
            caller=_wallet_address, # fill in your caller address or all zero address
            contract=_contract_Token,
            func_name="balanceOf",
            func_params=[_wallet_address],
            to=Token_contract_address,
        )
        #print("Wallet ("+str(_wallet_address)+") balance: " + str(balance_one["decoded"]["0"]))
        return int(balance_one["decoded"]["0"])

    #
    #Wrap Token into wToken
    #
    def wrap_Token(self,_wallet, _wallet_address):
        balance = self.wallet_balance(self._contract_Token, self.Token_contract_address, _wallet_address)

        #Approves the wToken contract to use the _wallet Tokens
        approve_wToken = self.connector.transact(
            _wallet,
            contract=self._contract_Token,
            func_name="approve",
            func_params=[self.wToken_contract_address,balance],
            to=self.Token_contract_address,
        )
        time.sleep(15)

        #Exchanges x amount of Tokens for x amount of wToken
        wrap_Token = self.connector.transact(
            _wallet,
            contract=self._contract_wToken,
            func_name="depositFor",
            func_params=[_wallet_address, balance],
            to=self.wToken_contract_address,
        )
        time.sleep(15)

    #
    #Unwrap wToken into Token
    #
    def unwrap_Token(self,
                _wallet, _wallet_address
                ):
        balance = self.wallet_balance(self.connector,self._contract_wToken, self.wToken_contract_address, _wallet_address)

        #Approves the wToken contract to use the _wallet Tokens
        approve_wToken = self.connector.transact(
            _wallet,
            contract=self._contract_Token,
            func_name="approve",
            func_params=[self.wToken_contract_address,balance],
            to=self.Token_contract_address,
        )
        time.sleep(10)

        #Exchanges x amount of Tokens for x amount of wToken
        unwrap_Token = self.connector.transact(
            _wallet,
            contract=self._contract_wToken,
            func_name="withdrawTo",
            func_params=[_wallet_address, balance],
            to=self.wToken_contract_address,
        )
        time.sleep(10)

    #
    # Delegate
    #
    def delegate(self,
                 _wallet,
                 delegate_to_address
                ):
        # Delegate the amount of Token tokens to himself to be able to vote
        delegate_token = self.connector.transact(
            _wallet, 
            contract=self._contract_wToken,
            func_name="delegate",
            func_params=[delegate_to_address],
            to=self.wToken_contract_address,
        )
        time.sleep(15)



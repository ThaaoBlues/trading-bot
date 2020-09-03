import os
import subprocess
from multiprocessing import Process, freeze_support
class manager():

    def __init__(self):
        os.chdir(os.getcwd())
        self.currency_value = ''
        self.currency = ''
        self.trigger_value = ''
        self.wallet = ''
        self.max_stock = ""
        self.check_files()
        
        with open('trading_botFiles\\settings\\trade_settings.txt','w') as f:
            f.write("0.1\n1000")
            f.close()

        self.main()






    def main(self):

        while True:
            cmd = input("manage trading bot (type help to display use tips): ")
            if cmd == "help":
                print("""
                - "set trigger <number>" : set the difference between buy price and sell price to trigger an action.
                - "set wallet <number>" : set the wallet content to the specified number.
                - "pause" : pause the bot.
                - "start" : start the bot.
                - "set cryptoc <name of the cryptocurrency>" : place the bot on the specified cryptocurrency stock.
                - "set cryptoc convert <abreviation of a currency (ex : eur,btc,usd...)>" : set the unity of the value of the cryptocurrency.
                - "set max tock <value>" : set the amount of cryptocurrency traded at each decision by the bot. 
                - "get cryptoc" : display current trading cryptocurrency.
                - "get cryptoc convert" : display current trading cryptocurrency converting value.
                - "get wallet" : display wallet content.
                - "get trigger" : display action triggering value difference.
                - "get max stock" : get the amount of cryptocurrency traded at each decision by the bot.
                - "resume" : wake up the bot when it is paused.
                - "reset price history" : reset the price history to have a brand new graph.
                """)

            elif cmd == "start":

                    
                self.check_files()

                if self.max_stock == "":
                    print("max stock value is not set, use \"set mex stock <value>\".")

                elif self.currency == "":
                    print("currency type is not set, use \"set cryptoc <cryptocurrency name>\". ")

                elif self.currency_value == "":
                    print("currency convert unity is not set, use \"set cryptoc convert <currency name>\". ")
                    
                elif self.trigger_value == "":
                    print("trigger value is not set, use \"set trigger <range to trigger an action>\".")

                elif self.wallet == "":                        
                    print("wallet content is not set, use \"set wallet <value>\".")

                else:
                    with  open("trading_botFiles\\bot_state.txt",'w') as f:
                        print("running")
                        f.write("running")
                        f.close()

                    bot = Process(target = self.start_bot)
                    bot.start()
                    print("bot started.")

            elif cmd == "pause":
                with  open("trading_botFiles\\bot_state.txt",'w') as f:
                    f.write("pause")
                    f.close()
                print("bot is now paused.")
            
            elif cmd == "resume":
                with  open("trading_botFiles\\bot_state.txt",'w') as f:
                    f.write("running")
                    f.close()
                print("bot is now running.")


            
                    

            elif cmd.startswith("set cryptoc"):
                if cmd.startswith("set cryptoc convert"):
                    self.currency_value = cmd.split()[3]               
                    with open("trading_botFiles\\cryptoc_value.txt",'w') as f:
                        f.write(self.currency_value)
                        f.close()
                    print(f"crypto currency convert unity is now : {self.currency_value}")
                else:
                    self.currency = cmd.split()[2]
                    with open("trading_botFiles\\cryptoc.txt",'w') as f:
                        f.write(self.currency)
                        f.close()
                    print(f"crypto currency is now : {self.currency}")


            elif cmd.startswith("set trigger"):
                self.trigger_value = cmd.split()[2].replace(",",".")
                with open('trading_botFiles\\settings\\trade_settings.txt','r') as f:
                    tt = f.read().split("\n")
                    f.close()
                    with open('trading_botFiles\\settings\\trade_settings.txt','w') as f:
                        tt[0] = self.trigger_value
                        for ele in tt:
                            f.write(ele + "\n")
                        f.close()
                    print(f"trigger fork is now {self.trigger_value}")

            elif cmd.startswith("set wallet"):
                self.wallet = cmd.split()[2].replace(",",".")
                with open('trading_botFiles\\settings\\trade_settings.txt','r') as f:
                    tt = f.read().split("\n")
                    f.close()
                    with open('trading_botFiles\\settings\\trade_settings.txt','w') as f:
                        tt[1] = self.wallet
                        for ele in tt:
                            f.write(ele + "\n")
                        f.close()
                print(f"wallet is now : {self.wallet}")

            elif cmd == "get wallet":
                with open('trading_botFiles\\settings\\trade_settings.txt','r') as f:
                    f.readline()
                    val = f.readline().strip("\n")
                    print(f"wallet content : {val} USD")
                    f.close()

            elif cmd == "get trigger":
                with open('trading_botFiles\\settings\\trade_settings.txt','r') as f:
                    val = f.readline().strip("\n")
                    print(f"trigger value : {val}")
                    f.close()

            elif cmd == "get cryptoc":
                with open("trading_botFiles\\cryptoc.txt",'r') as f:
                    print(f"cryptoc : {f.read()}")
                    f.close()

            elif cmd == "get cryptoc convert":
                with open("trading_botFiles\\cryptoc_value.txt",'r') as f:
                    print(f"cryptoc convert : {f.readline()}")
                    f.close()
                    
            elif cmd == "get bot state":
                with  open("trading_botFiles\\bot_state.txt",'r') as f:
                    print(f"bot state : {f.read()}")
                    f.close()

            elif cmd == "get max stock":
                 with  open("trading_botFiles\\max_stock.txt",'r') as f:
                    self.max_stock = f.read()
                    print(f"max stock : {self.max_stock}")
                    f.close()

            elif cmd.startswith("set max stock"):
                 with  open("trading_botFiles\\max_stock.txt",'w') as f:
                    self.max_stock = cmd.split()[3]
                    f.write(self.max_stock)
                    print(f"max stock is now : {self.max_stock}")
                    f.close()

            elif cmd == "reset price history":
                with open("trading_botFiles\\price_history.txt","w"):
                    f.close()
                print("price history has been reset.")
            else:
                print("Unknown command, type help to get a command list.")


    def check_files(self):
            os.chdir(os.getcwd())
            print("[+]files init...")

            try:
                open('trading_botFiles\\settings\\trade_settings.txt')
                open("trading_botFiles\\price_history.txt")
                open('trading_botFiles\\last_action.txt')
                open('trading_botFiles\\stock.txt')
                open("trading_botFiles\\last_price.txt")
                open("trading_botFiles\\bot_state.txt")
                open("trading_botFiles\\cryptoc.txt")
                open("trading_botFiles\\cryptoc_value.txt")
                open('trading_botFiles\\buy_price.txt')
                open('trading_botFiles\\max_stock.txt')

            except:
                try:
                    os.mkdir("trading_botFiles")
                    os.mkdir("trading_botFiles\\settings")
                    open('trading_botFiles\\settings\\trade_settings.txt','w')
                    open("trading_botFiles\\price_history.txt",'w')
                    open('trading_botFiles\\last_action.txt','w')
                    open('trading_botFiles\\stock.txt','w')
                    open('trading_botFiles\\buy_price.txt','w')
                    open("trading_botFiles\\last_price.txt",'w')
                    open("trading_botFiles\\bot_state.txt",'w')
                    open("trading_botFiles\\cryptoc.txt",'w')
                    open("trading_botFiles\\cryptoc_value.txt",'w')
                    open('trading_botFiles\\max_stock.txt','w')

                except:
                    pass

    def start_bot(self):
        subprocess.call("F:\Python\python trading_bot.py", creationflags=subprocess.CREATE_NEW_CONSOLE)
    

if __name__ == "__main__":
    freeze_support()
    manager1 = manager()











import string
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process, freeze_support
from threading import Thread
import os
import matplotlib.animation as animation
import platform
import requests

class real_time_follower():
    def __init__(self):
        os.chdir(os.getcwd())
        self.first_loop = True
        self.play = False
            
        self.currency = ""
        self.currency_value = ""
        self.max_stock = ""
            
        self.wait_message_process = Process(target = self.wait_message)
        self.wait_message_process.start()
        self.first_start = True
        
        self.main()
        self.price_f = ''
        self.price = ''
        self.h1 = ''
        

        
    def wait_message(self):
        pos = 1
        if platform.system() == 'Windows':
            command = "cls"   
        else :
            command = "clear"
        time.sleep(1)
        os.system(command)
        while True:
            if pos == 1:
                sys.stdout.write("\r Chargement des composants... |")
                time.sleep(0.25)
                pos = 2
            elif pos == 2:
                sys.stdout.write("\r Chargement des composants... /")
                time.sleep(0.25)
                pos = 3
            elif pos == 3:
                sys.stdout.write("\r Chargement des composants... -")
                time.sleep(0.25)
                pos = 4
            elif pos == 4:
                sys.stdout.write("\r Chargement des composants... \\")
                time.sleep(0.25)
                pos = 1
        
    def main(self):

        time.sleep(5)
        
        plot = Thread(target = self.make_graph)
        plot.start()

        self.wait_message_process.terminate()


        try :
            while True :
                with  open("trading_botFiles\\max_stock.txt",'r') as f:
                    self.max_stock = f.read()
                    f.close()
                with open("trading_botFiles\\bot_state.txt","r") as f:
                    if f.read() == "running":
                        self.play = True
                    else :
                        self.play = False

                if self.play:
                    with open("trading_botFiles\\cryptoc.txt","r",encoding = 'utf-8') as f:
                        self.currency = f.read()
                        f.close()

                    with open("trading_botFiles\\cryptoc_value.txt","r",encoding = 'utf-8') as f:
                        self.currency_value = f.read()
                        f.close()

                    text = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={self.currency}&vs_currencies={self.currency_value}").text
                    price = text.replace("{\""+self.currency+"\":{\""+self.currency_value+"\":","").strip("}}")

                    self.price = price
                    self.backup_data(self.price)
                    time.sleep(1)
                    self.first_loop = False

                
                
        except Exception as e:
            print(e)
            print("Bye !")
           
            exit(1)
    
    def backup_data(self,price):
        self.price_f = float(price.replace(',','.').strip('\n'))
        with open("trading_botFiles\\price_history.txt",'a',encoding = 'utf-8') as f:
            f.write("{}\n".format(str(self.price_f)))
            f.close()
        if self.first_loop == False:  
            try:
                with open("trading_botFiles\\last_price.txt",'r',encoding = 'utf-8') as f:
                    last_price = f.readline()
                    last_price = float(last_price.replace(',','.').strip('\n'))
                    diff = str(round(self.price_f - last_price,5))
                    action = self.calc_action(diff)
                    with open("trading_botFiles\\stock.txt",'r',encoding = 'utf-8') as f:
                        stock = f.readline()
                        f.close()
                    with open("trading_botFiles\\buy_price.txt",'r',encoding = 'utf-8') as f:
                        bp = f.readline()
                        f.close()

                    print("price : {} curve : {}, action : {}, stock : {}, bought at : {}".format(price,diff,action,stock,bp))
                    f.close()                        
                    with open("trading_botFiles\\last_price.txt",'w',encoding = 'utf-8') as f:
                        f.write("{}\n".format(str(self.price_f)))

                        f.close
            except Exception as e:
                print(e)
                with open("trading_botFiles\\last_price.txt",'w',encoding = 'utf-8') as f:
                    f.write("{}\n".format(self.price))
                    f.close()
        else:
            with open('trading_botFiles\\settings\\trade_settings.txt','r',encoding = 'utf-8') as f:
                action_range = float(f.readline().strip('\n'))
                wallet = float(f.readline().strip('\n'))
                f.close()
            with open('trading_botFiles\\last_action.txt','w',encoding = 'utf-8') as f:
                f.write('buy')
                f.close()
            with open('trading_botFiles\\stock.txt','w',encoding = 'utf-8') as f:
                f.write(self.max_stock)
                f.close()
            with open('trading_botFiles\\settings\\trade_settings.txt','w',encoding = 'utf-8') as f:
                f.write("{}\n".format(str(action_range)))
                f.write("{}".format(str(wallet - (self.price_f*int(self.max_stock)))))
                print("wallet :: {} ".format(str(wallet - (self.price_f*int(self.max_stock)))))
                f.close()
            with open("trading_botFiles\\buy_price.txt",'w',encoding = 'utf-8') as f:
                f.write(str(self.price))
                f.close()
            with open("trading_botFiles\\last_price.txt",'w',encoding = 'utf-8') as f:
                print(f"first loop, buying {self.max_stock} {self.currency} at {price}")
                f.write("{}\n".format(str(self.price_f)))
                f.close()



            
    def calc_action(self,diff):
            with open('trading_botFiles\\settings\\trade_settings.txt','r',encoding = 'utf-8') as f:
                action_range = float(f.readline().strip('\n'))
                wallet = float(f.readline().strip('\n'))
                f.close()


            with open('trading_botFiles\\last_action.txt','r',encoding = 'utf-8') as f:
                last_action = f.read()
                f.close()

                
            with open('trading_botFiles\\stock.txt','r',encoding = 'utf-8') as f:
                stock = f.read()
                f.close()

            with open("trading_botFiles\\buy_price.txt",'r',encoding = 'utf-8') as f:
                pre = f.read()
                if pre != '':
                    buy_price = float(pre)
                else:
                    buy_price = float(0)
                f.close()

            with open("trading_botFiles\\last_price.txt",'r',encoding = 'utf-8') as f:
                last_price = f.readline()
                last_price = float(last_price.replace(',','.').strip('\n'))
                f.close()

            with open("trading_botFiles\\buy_price.txt",'r',encoding = 'utf-8') as f:
                bp = f.readline()
                f.close()
                
            if last_action != 'buy' and stock != self.max_stock and self.price_f < float(bp):
                
                with open('trading_botFiles\\last_action.txt','w') as f:
                    f.write('buy')
                    f.close()
                with open('trading_botFiles\\stock.txt','w') as f:
                    f.write(self.max_stock)
                    f.close()
                with open('trading_botFiles\\settings\\trade_settings.txt','w') as f:
                    f.write("{}\n".format(str(action_range)))
                    f.write("{}".format(str(wallet - (self.price_f*int(self.max_stock)))))
                    print("wallet :: {} ".format(str(wallet - (self.price_f*int(self.max_stock)))))
                    f.close()
                with open("trading_botFiles\\buy_price.txt",'w',encoding = 'utf-8') as f:
                    f.write(str(self.price))
                    f.close()
                    
                return 'buy'

            
            elif last_action != 'sell' and stock != '0' and self.first_loop == False and self.price_f >= buy_price + action_range:
                
                with open('trading_botFiles\\last_action.txt','w') as f:
                    f.write('sell')
                    f.close()
                with open('trading_botFiles\\stock.txt','w') as f:
                    f.write('0')
                    f.close()
                with open('trading_botFiles\\settings\\trade_settings.txt','w') as f:
                    f.write("{}\n".format(str(action_range)))
                    f.write("{}".format(str(wallet + (self.price_f*int(self.max_stock)))))
                    print("\nwallet :: {} ".format(str(wallet + (self.price_f*int(self.max_stock)))))
                    f.close()
                
                    
                return 'sell'

        

            else:
                with open('trading_botFiles\\last_action.txt','w') as f:
                    f.write('None')
                    f.close()
                return 'None'
        

    def make_graph(self):
        
        all_prices = []
        f = open("trading_botFiles\\price_history.txt",'r')
        
        for ele in f.readlines():
            all_prices.append(float(ele.strip('\n')))

        f.close()
        fig = plt.figure() 
        self.h1 = fig.add_subplot(1,1,1)
        plt.legend('Ethereum price')
        ani = animation.FuncAnimation(fig, self.animate_graph, interval=1000)
        plt.show()
        
            

    def animate_graph(self,i):
        
            all_prices = []
            f = open("trading_botFiles\\price_history.txt",'r')
            
            for ele in f.readlines():
                all_prices.append(float(ele.strip('\n')))
                
            f.close()
            self.h1.clear()
            self.h1.plot(all_prices)
        


if __name__ == "__main__":
    freeze_support()
    real_time_follower1 = real_time_follower()
    

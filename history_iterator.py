from specs import id, hash, get_chat_ids_doller, get_chat_ids_silver
from telethon import TelegramClient
import pymongo
import re
import datetime 
from zoneinfo import ZoneInfo 




#introduce mongo db 
mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongoclient["telegram"]
doller_col = db["dollar"]  
silver_col = db['silver']
 

#build the class
class client(TelegramClient) :
    def __init__(self, name, api_id, api_hash, doller_col, silver_col) :
        super().__init__(name, api_id, api_hash)     
        
         
###main function

    async def main(self) : 

##doller part  
        for id in get_chat_ids_doller :
            messages = await self.get_messages(entity = -id, limit = None, offset_date = datetime.datetime.now())
            
            
#price part         
            for message in messages : 
                price = ''
                try :   
                    for letter in message.text :
                        if str.isdigit(letter) : 
                            num = letter
                            added_num = ''.join(num)
                            price += added_num
                            suspicious = False
                            reason = None
#if we have chat action messages in the channel,we will get this error.       
                except TypeError : 
                    None    
                    
                    
#suspesios finder and reason part
                if price == '' :
                    price = None
                    suspicious = True            
                    reason = ('There is not any number')
                elif len(re.split('', price)) != 7 :
                    price = None
                    suspicious = True 
                    reason = ('High or low number of numbers')
                elif message.media != None :
                    price = None
                    suspicious = True 
                    reason = ('There is media in the post') 
                elif re.findall('دلار', message.text) != ['دلار'] : 
                    price = None
                    suspicious = True 
                    reason = ('It is a wierd message')  
                    
                    
#source part
                if message.chat_id == -get_chat_ids_doller[0] :
                    source = 'arka'
                elif message.chat_id == -get_chat_ids_doller[1] :
                    source = 'tehran sabze'  
                   
                            
#Convert the price to number for beauty of database
                if price != None :          
                    price = int(price)     
                             
                                                     
#change zone(not work yet)                  
#                utc_dt = message.date.astimezone(ZoneInfo('UTC'))
#                message.date = utc_dt.astimezone(ZoneInfo('Asia/Tehran'))


    #inserting part 
                my_dict = {
                        'price' : price,
                        'time' : message.date,
                        'source' : source,
                        'message' : message.text,
                        'sospension' : suspicious,
                        'reason' : reason
                        }
                doller_col.insert_one(my_dict)
                


##silver part 
        for id in get_chat_ids_silver :      
            messages = await self.get_messages(entity = -id, limit = None, offset_date = datetime.datetime.now())
            
            
#price part         
            for message in messages : 
                numbers = ''
                try :   
                    for letter in message.text :
                        if str.isdigit(letter) : 
                            num = letter
                            added_num = ''.join(num)
                            numbers += added_num
                    price1 = int(numbers[0:6])
                    price2 = float(numbers[9:11] + '.' + numbers[11:13])
                    
#if we have chat action messages in the channel,we will get this error.       
                except TypeError : 
                    None    
                    
                                     
#source part
                if message.chat_id == -get_chat_ids_silver[0] :
                    source = 'Noghre Ati'

                            
#Convert the price to number for beauty of database
                if price != None :          
                    price = int(price)     
                             
                                                     
#change zone(not work yet)                  
#                utc_dt = message.date.astimezone(ZoneInfo('UTC'))
#                message.date = utc_dt.astimezone(ZoneInfo('Asia/Tehran'))


    #inserting part 
                my_dict = {
                        'sana price' : price1,
                        'jahani price' : price2,
                        'time' : message.date,
                        'source' : source,
                        'message' : message.text,
                        }
                silver_col.insert_one(my_dict)
                


                    
#turn on   
user = client('user', id, hash, doller_col, silver_col)
user.start()
user.loop.run_until_complete(user.main())        

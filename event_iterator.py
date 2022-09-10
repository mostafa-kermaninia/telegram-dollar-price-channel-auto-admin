from specs import id, hash, get_chat_ids_doller, send_chat_ids
from telethon import TelegramClient,events
import pymongo
import re


#introduce mongo db 
mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongoclient["telegram"]
col = db["dollar"]  
 
 
#build the class
class client(TelegramClient) :
    def __init__(self, name, api_id, api_hash, col):
        super().__init__(name, api_id, api_hash)
        
        self.add_event_handler(self.main, events.NewMessage(from_users = get_chat_ids_doller))
       
       
##main function  
    async def main(self, event) :
        
        
#price part 
        price = ''    
        for letter in event.text :
            if str.isdigit(letter) : 
                num = letter
                added_num = ''.join(num)
                price += added_num
                suspicious = False
                reason = None        
         
            
#suspesios finder and reason part
        if price == '' :
            price = None
            suspicious = True            
            reason = ('There is not any number')
        elif len(re.split('', price)) != 7 :
            price = None
            suspicious = True 
            reason = ('High or low number of numbers')
        elif event.media != None :
            price = None
            suspicious = True 
            reason = ('There is media in the post') 
        elif re.findall('دلار', event.text) != ['دلار'] : 
            price = None
            suspicious = True 
            reason = ('It is a wierd message')  
            
                
#source part
        if event.chat_id == -get_chat_ids_doller[0] :
            source = 'arka'
        elif event.chat_id == -get_chat_ids_doller[1] :
            source = 'tehran sabze'  
            
            
#sleep(optional)
#        await asyncio.sleep(10)
      
            
#post into the channal           
        if price != None :   
#tehran sabze handling
            for id in send_chat_ids :
                if re.findall('سبزه', event.text) == ['سبزه'] : 
                    
                    if re.findall('فـردایی', event.text) == ['فـردایی'] :
                        if re.findall('خــریـدار', event.text) == ['خــریـدار'] :
                            await self.send_message(id, f'دلار سبزه فردايي💸 {price} \n خريدار✅')                         
                        elif re.findall('فروشنده', event.text) == ['فروشنده'] :    
                            await self.send_message(id, f'دلار سبزه فردايي💸 {price} \n فروشنده❎') 
                        elif re.findall('معامله', event.text) == ['معامله']  :    
                            await self.send_message(id, f'دلار سبزه فردايي💸 {price} \n معامله شد❇️')   
                                                
                    elif re.findall('نـــقـدی', event.text) == ['نـــقـدی'] : 
                        if re.findall('خــریـدار', event.text) == ['خــریـدار'] :
                            await self.send_message(id, f'دلار سبزه نقدي💰 {price} \n خريدار✅')                         
                        elif re.findall('فروشنده', event.text) == ['فروشنده'] :    
                            await self.send_message(id, f'دلار سبزه نقدي💰 {price} \n فروشنده❎') 
                        elif re.findall('معامله', event.text) == ['معامله'] :    
                            await self.send_message(id, f'دلار سبزه نقدي💰 {price} \n معامله شد❇️')                           
#gheimat lahzeh handling 
                if re.findall('فردایی', event.text) == ['فردایی'] :  
                    await self.send_message(id, f'دلار  فردايي💸 {price} \n معامله شد❇️')   
                                                
                elif re.findall('تهران', event.text) == ['تهران'] :  
                    await self.send_message(id, f'دلار  تهران🏦 {price} \n معامله شد❇️')                         
                   
                            
#Convert the price to number for beauty of database
                price = int(price)  
                
                
#change zone(not work yet)          
#        utc_dt = event.date.astimezone(ZoneInfo('UTC'))
#        event.date =  utc_dt.astimezone(ZoneInfo('Asia/Tehran'))
                   
                   
#inserting part 
        my_dict = {
                'price' : price,
                'time' : event.date,
                'source' : source,
                'message' : event.text,
                'sospension' : suspicious,
                'reason' : reason
                }
        col.insert_one(my_dict)

    
    
    
#turn on   
user = client('user', id, hash, col)
user.start()
user.run_until_disconnected()        
#:)
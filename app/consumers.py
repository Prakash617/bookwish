from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
import json
# database
from app.models import Chat, Group

# class MySyncConsumer(SyncConsumer):

#     def websocket_connect(self, event):
#         print('websocket connect.. ',  event)
#         print('channel layer...', self.channel_layer) #get default channel layer
#         print('channel Name... ',self.channel_name) #get channel name
#         print('group_name...', self.scope['url_route']['kwargs']['group_name'])
#         self.group_name = self.scope['url_route']['kwargs']['group_name']
        
        
#         async_to_sync(self.channel_layer.group_add)(self.group_name, #group name
#                                                     self.channel_name)
#         self.send({
#             "type": "websocket.accept",
#         })

#     def websocket_receive(self, event):
#         print('websocket receive from client.. ',  event,)
#         data = json.loads(event['text'])
#         group = Group.objects.get(name = self.group_name)
#         print('group',group)
#         chat = Chat(content = data['msg'], group = group)
#         print('chat',chat)
#         chat.save()
        
#         async_to_sync(self.channel_layer.group_send)(self.group_name,{
#             'type':'chat.message',
#             'message':event['text']
#         })
            
            
#         # self.send({
#         #     'type': 'websocket.send',
#         #     'text': event['text'],
#         # })
        
#     def chat_message(self,event):
#         print('event',event)
#         print('actual data........', event['message'])
        
#         self.send({
#             'type': 'websocket.send',
#             'text': event['message'],
#         })
        
#     def websocket_disconnect(self, event):
#         print('websocket disconnect.. ',  event)
#         # self.send({
#         #     "type": "websocket.accept",
#         # })
        
#         async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)
#         raise StopConsumer
    
    
    

class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('websocket connect.. ',  event)
        print('channel layer...', self.channel_layer) #get default channel layer
        print('channel Name... ',self.channel_name) #get channel name
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        
        await self.channel_layer.group_add(self.group_name, #group name
                                                    self.channel_name)
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        print('websocket receive from client.. ',  event)
        print('event',event['text'])
        # data = json.loads(event['text'])
        data = json.loads(event['text'])
        print('data',data)
        print('data---',data['msg'],type(data['msg']))
        # find group obj
        # for orm filter use below
        group = await database_sync_to_async(Group.objects.get)(name = self.group_name)
        print('group',group)
        print('user',self.scope['user'])
        if self.scope['user'].is_authenticated:
            chat = Chat(content = data['msg'], group = group)
            print('chat',chat)
            await database_sync_to_async(chat.save)()
            data['user'] = self.scope['user'].username
            print('username', data['user'])
            await self.channel_layer.group_send(self.group_name,{
                'type':'chat.message',
                'message':json.dumps(data)
            })
        else:
            await self.send({
            'type': 'websocket.send',
            'text': json.dumps({'msg':'login Required','user':'guest'}),
            })
            
            
            
        
        
    async def chat_message(self,event):
        print('event',event)
        print('actual data........', event['message'])
        
        await self.send({
            'type': 'websocket.send',
            'text': event['message'],
        })
        
    async def websocket_disconnect(self, event):
        print('websocket disconnect.. ',  event)
        # self.send({
        #     "type": "websocket.accept",
        # })
        
        await self.channel_layer.group_discard(self.group_name,self.channel_name)
        raise StopConsumer
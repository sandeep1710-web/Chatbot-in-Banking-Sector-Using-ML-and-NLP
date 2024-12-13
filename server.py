"""from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from chatbot import get_response,get_response2


class ChatServer(WebSocket):

    def handleMessage(self):





        # echo message back to client
        message = self.data
        #message1=self.data

        response = get_response(message)
        a = get_response2(message)
        self.sendMessage(response)
        self.sendMessage(a)



        #self.sendMessage(a)



    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')



server = SimpleWebSocketServer('', 8000, ChatServer)
server.serveforever()"""

import asyncio
import websockets
from chatbot import get_response, get_response2
import mysql.connector

mydb =mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Sandeep1234#",
    database = "chatbot"
)
cur = mydb.cursor()

def addtodatabase(message,response):        
        query = "INSERT into history values(%s,%s);"
        cur.execute(query,(message,response,))
        mydb.commit()
        new = cur.fetchall()
        print(new)

async def on_message(websocket, path):
    while True:
        message = await websocket.recv()
        response = get_response(message)
        a = get_response2(message)
        await websocket.send(response)
        await websocket.send(a)
        addtodatabase(message,response)


start_server = websockets.serve(on_message, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
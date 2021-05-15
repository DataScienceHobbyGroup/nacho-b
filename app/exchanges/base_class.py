class exchange_base_class():
    
    # Access the command queue
    q = []

    async def buy(self,qty,value):
        pass

    async def sell(self,qty,value):
        pass

    async def run(self):
        while True:
            item = await self.q.get()
            if item.isBuyTransaction:
                await self.buy(item.amount, item.desired_value)
            else:
                await self.sell(item.amount, item.desired_value)
            #print ('Got: ' + str(item))
            await self.q.task_done()

    def __init__(self,queue,initial_investment=0):  
        self.q = queue
        self.current_balance = initial_investment            
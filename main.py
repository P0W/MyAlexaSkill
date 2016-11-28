## Author : Prashant
## Learning Amazon Web Services( AWS) Lambda Functions with Amazon Echo


class AlexaResponseBuilder(object):
    def __init__(self, event, context ):
        self.event   = event
        self.context = context
        self.sessionAttributes = { }
        self.sendToAlexa = {
  "version": "1.0",
  "response": {
    "outputSpeech": {
      "text": "Welcome to the Alexa Skills by P0W",
      "type": "PlainText"
    },
    "shouldEndSession": False,
    "reprompt": {
      "outputSpeech": {
        "text": "Please say some stock to listen current values",
        "type": "PlainText"
      }
    },
    "card": {
      "content": "Stock Values",
      "type": "Simple",
      "title": "Stock Values from Bombay Stock Exchange"
    }
  },
  "sessionAttributes": {}
}

    def run( self ):
        dispatcher = {
            'LaunchRequest'      : self.onLaunchRequestReceived,
            'IntentRequest'      : self.onIntentRequestReceived,
            'SessionEndedRequest':self.onSessionEndedRequestReceived,
                      }.get( self.event['request']['type'], self.onInvalidRequestReceived )
        return dispatcher()
        
    def onInvalidRequestReceived( self ):
        raise ValueError("Invalid Request Received") 
        

    def onLaunchRequestReceived( self ):
        return self.sendToAlexa
        pass

    def onIntentRequestReceived( self ):
        dispatcher ={
            'AMAZON.HelpIntent'   :self.onHelpIntentReceived,
            'AMAZON.CancelIntent' :self.onCancelIntentReceived,
            'AMAZON.StopIntent'   :self.onStopIntentReceived,
            }.get( self.event['request']['intent']['name'], self.onCustomIntentReceived )
        
        return dispatcher()
        
    def onSessionEndedRequestReceived( self ):       
        self.sendToAlexa['response']['shouldEndSession'] = True
        return self.sendToAlexa

    def onHelpIntentReceived( self ):        
        self.sendToAlexa['response']['shouldEndSession'] = True
        return self.sendToAlexa

    def onCancelIntentReceived( self ):
        self.sendToAlexa['response'][ 'outputSpeech' ][ 'text' ] = \
                    "Thank you for trying the P0W Alexa Skills Kit. " \
                    "Have a nice day! "         
        self.sendToAlexa['response']['shouldEndSession'] = True
        return self.sendToAlexa

    def onStopIntentReceived( self ):
        self.sendToAlexa['response'][ 'outputSpeech' ][ 'text' ] = \
                    "Thank you for trying the P0W Alexa Skills Kit. " \
                    "Have a nice day! "         
        self.sendToAlexa['response']['shouldEndSession'] = True
        return self.sendToAlexa

    def onCustomIntentReceived( self ):
        return self.sendToAlexa


#python 2.7.6
from urllib import *
import json
import time
import copy

class GoogleFinanceStockGrabber(object):
    def __init__(self):
        self.prefix = "http://finance.google.com/finance/info?client=ig&q="

    def get(self,symbol):
        url = self.prefix+"%s"%(symbol)
        u = urlopen(url)
        content = u.read().decode('utf-8')
        
        obj = json.loads(content[3:])
        return obj

    def stockPrinter( self, symb ):
        print ( '\n%10s | %-6s : %10s (%8s %% ) < %s >' % (symb['t'], symb['e'], symb['l'], symb['cp'], symb['lt'] ) )
          
class StockRunner(  GoogleFinanceStockGrabber ):
    def __init__(self, AllStocks):
        super(StockRunner, self).__init__()
        self.AllStocks = copy.deepcopy(AllStocks)
            
    def run(self):
        res = []
        quote = self.get(','.join( self.AllStocks.keys() ) )
        for symb in quote:
            stockKey = '%s:%s' % ( symb['e'], symb['t'] )
            res.append ( '%s is %s Rupees' % (self.AllStocks[stockKey], symb['l'] ) )
        return "\n ..".join(res)
               
        
    

AllStocks = { 
                   ## 'Exchange:Symbol' : Actual Name
                  'BOM:509480'      : 'Berger Paints'             ,
                  'BOM:500233'      : 'Kajaria Ceramics'          ,
                  'BOM:532540'      : 'Tata Consultancy Services Limited' ,
                  'BOM:532500'      : 'Maruti Suzuki India Limited',
                  'BOM:500096'      : 'Dabur India Limited'       ,
                  'BOM:500112'      : 'State Bank of India'       ,
                  'BOM:500209'      : 'Infosys Limited',
                  'BOM:532483'      : 'Canara Bank Limited',
                  'BOM:533344'      : 'PTC India Financial Services Limited',
                  'BOM:500570'      : 'Tata Motors Limited',
                  'BOM:502137'      : 'Deccan Cements',
                }
                
class GreetFromAlexa( AlexaResponseBuilder ):
    def __init__(self, event, context ):
        super( GreetFromAlexa, self ).__init__( event, context )
        self.sockrunner = StockRunner(AllStocks)

    def onLaunchRequestReceived( self ):
        print ('LAUCH REQUEST')
        self.sendToAlexa['response'][ 'outputSpeech' ][ 'text' ] = \
                    "Welcome to the P0W Alexa Skills Kit Test. " \
                    "This is developed by Prashant"
        self.sendToAlexa['response']['shouldEndSession'] = False
        return  self.sendToAlexa
        
    def onCustomIntentReceived( self ):
        print ('INTENT REQUEST' )
        self.sendToAlexa['response'][ 'outputSpeech' ][ 'text' ] = \
                    "Your share values from Bombay Stock Exchage as follows :\n %s " % self.sockrunner.run()
        self.sendToAlexa['response']['shouldEndSession'] = True
        self.sendToAlexa['response'][ 'card' ][ 'content' ] = self.sendToAlexa['response'][ 'outputSpeech' ][ 'text' ] 
        return  self.sendToAlexa

def lambda_handler( event, context ):
    '''
     This function should be called from AWS lambda
    '''    
    alexaObj = GreetFromAlexa(  event, context )
    return alexaObj.run( )

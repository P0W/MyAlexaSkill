
## Author : Prashant
## Learning Amazon Web Services( AWS) Lambda Functions with Amazon Echo

class AlexaResponseBuilder:
    def __init__(self, event, context ):
        self.event   = event
        self.context = context
        self.sessionAttributes = { }
        self.sendToAlexa = {  
   "version" : "1.0",
   "sessionAttributes" :self.sessionAttributes,
   "response":{  
      "outputSpeech":{  
         "type":"PlainText",
         "text":" AlexaResponseBuilder - None",         
      },
      "card":{  
         "type":"Simple",
         "title":"AlexaResponseBuilder - Title",
         "content":"AlexaResponseBuilder - Content",
         "text":"AlexaResponseBuilder - Text",
      },
      "reprompt":{  
         "outputSpeech":{  
            "type":"Simple",
            "text":"AlexaResponseBuilder - Text",
      },
      "shouldEndSession": False
   }
      }
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
        self.sendToAlexa['shouldEndSession'] = True
        return self.sendToAlexa

    def onHelpIntentReceived( self ):        
        self.sendToAlexa['shouldEndSession'] = True
        return self.sendToAlexa

    def onCancelIntentReceived( self ):
        self.sendToAlexa['response'][ 'outputSpeech' ][ 'text' ] = \
                    "Thank you for trying the P0W Alexa Skills Kit. " \
                    "Have a nice day! "         
        self.sendToAlexa['shouldEndSession'] = True
        return self.sendToAlexa

    def onStopIntentReceived( self ):
        self.sendToAlexa['response'][ 'outputSpeech' ][ 'text' ] = \
                    "Thank you for trying the P0W Alexa Skills Kit. " \
                    "Have a nice day! "         
        self.sendToAlexa['shouldEndSession'] = True
        return self.sendToAlexa

    def onCustomIntentReceived( self ):
        return self.sendToAlexa



class GreetFromAlexa( AlexaResponseBuilder ):
    def __init__(self, event, context ):
        super( GreetFromAlexa, self ).__init__( event, context )

    def onLaunchRequestReceived( self ):
        self.sendToAlexa['response'][ 'outputSpeech' ][ 'text' ] = \
                    "Welcome to the P0W Alexa Skills Kit Test. " \
                    "This is developed by Prashant"
        return  self.sendToAlexa


def lambda_handler( event, context ):
    '''
     This function should be called from AWS lambda
    '''    
    alexaObj = GreetFromAlexa(  event, context )
    return alexaObj.run( )


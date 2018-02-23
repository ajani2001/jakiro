from RetransLayer                    import RetransLayer
from yowsup.layers                   import YowParallelLayer, YowLayerEvent
from yowsup.layers.protocol_receipts import YowReceiptProtocolLayer
from yowsup.layers.auth              import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers.protocol_acks     import YowAckProtocolLayer
from yowsup.layers.axolotl           import AxolotlSendLayer, AxolotlControlLayer, AxolotlReceivelayer
from yowsup.layers.network           import YowNetworkLayer
from yowsup.stacks                   import YowStack, YOWSUP_CORE_LAYERS

vk_credentials = ( 6376055, input('enter you vk login\n'), input('enter you vk password\n') )
whatsapp_credentials = ( input('enter you phone number for whatsapp\n'), input('enter the code you\'ve received via yowsup cli\n') )

AXOLOTL_LAYERS = ( YowParallelLayer([AxolotlSendLayer, AxolotlReceivelayer]), AxolotlControlLayer )
layers = ( RetransLayer, YowParallelLayer([YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowAckProtocolLayer, YowReceiptProtocolLayer]) ) + AXOLOTL_LAYERS + YOWSUP_CORE_LAYERS

stack = YowStack(layers)
stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, whatsapp_credentials)
stack.setProp('vk_credentials', vk_credentials)
stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
stack.loop()

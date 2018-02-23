import vk
from yowsup.layers                                    import EventCallback
from yowsup.layers.interface                          import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.network                            import YowNetworkLayer
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities     import OutgoingAckProtocolEntity

class RetransLayer(YowInterfaceLayer):

  vkApi = None
  userId = None

  @ProtocolEntityCallback("message")
  def onMessage(self, entity):
    self.toLower( OutgoingReceiptProtocolEntity( entity.getId(), entity.getFrom(), 'read', entity.getParticipant() ) )
    self.vkApi.messages.send( user_id=self.userId, message = 'from: {getFrom}\n{getBody}'.format( getFrom = entity.getFrom(), getBody = entity.getBody() ) )

  ''' #for further versions
  @ProtocolEntityCallback("receipt")
  def onReceipt(self, entity):
    self.toLower( OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom()) )
  '''

  @EventCallback(YowNetworkLayer.EVENT_STATE_CONNECT)
  def connectVk(self, event):
    credentials = self.getProp('vk_credentials')
    self.vkApi = vk.API( vk.AuthSession(app_id=credentials[0], user_login=credentials[1], user_password=credentials[2], scope='messages') )
    self.userId = self.vkApi.users.get()[0]['uid']

  def __str__(self):
    return 'Retranlation Layer'

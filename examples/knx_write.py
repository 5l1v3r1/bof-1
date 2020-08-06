from sys import path, argv
path.append('../')

from bof import knx, BOFNetworkError

def update_source(knxnet, field):
    field.ip_address.value = knxnet.source_address
    field.port.value = knxnet.source_port

def tunnel_connect(knxnet):
    tunnel_connect_request = knx.KnxFrame(type="CONNECT_REQUEST",
                                          connection="TUNNELING CONNECTION")
    update_source(knxnet, tunnel_connect_request.body.control_endpoint)
    update_source(knxnet, tunnel_connect_request.body.data_endpoint)
    tunnel_connect_response = knxnet.send_receive(tunnel_connect_request)
    return tunnel_connect_response.body.communication_channel_id.value

def tunnel_disconnect(knxnet, channel):
    tunnel_disconnect_request = knx.KnxFrame(type="DISCONNECT_REQUEST")
    tunnel_disconnect_request.body.communication_channel_id.value = channel
    update_source(knxnet, tunnel_disconnect_request.body.control_endpoint)
    tunnel_disconnect_response = knxnet.send_receive(tunnel_disconnect_request)

def group_write(knxnet, kga, value):
    """Write ``value`` to knx group address ``kga`` on ``knxnet``"""
    request = knx.KnxFrame(type="CONFIGURATION REQUEST", cemi="L_Data.req")
    print(request)
    #TODO

if len(argv) < 2:
    print("Usage: {0} IP".format(argv[0]))
    exit(-1)

try:
    knxnet = knx.KnxNet()
    knxnet.connect(argv[1])
    channel = tunnel_connect(knxnet)
    group_write(knxnet, "1/1/1", 1)
    tunnel_disconnect(knxnet, channel)
except BOFNetworkError as bne:
    print(bne)
finally:
    knxnet.disconnect()
# In consumers.py
from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from channels.sessions import enforce_ordering


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    message.channel_session['room'] = message.user.id
    Group("user-%s" % message.user.id).add(message.reply_channel)


@enforce_ordering
@channel_session_user
def ws_message(message):
    Group("user-%s" % message.channel_session['room']).send({
        "text": message['text'],
    })


@channel_session_user
def ws_disconnect(message):
    Group("user-%s" % message.channel_session['room']).discard(message.reply_channel)

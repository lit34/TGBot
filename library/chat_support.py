import asyncio
from library.sql import *
from presets import Presets
from pyrogram.errors import FloodWait


# Function to find last message id of supported types
async def find_msg_id(client, id, chat_id):
    id_last_msg = int()
    try:
        async for user_message in client.USER.iter_history(chat_id):
            messages = await client.USER.get_messages(chat_id, user_message.message_id, replies=0)
            for file_type in file_types:
                media = getattr(messages, file_type, None)
                if media is not None:
                    id_last_msg = str(messages.message_id).split(" ")[0]
                    await msg_id_limit(id, id_last_msg)
                    await to_msg_id_cnf_db(id, id_last_msg)
                    file_types.clear()
                    file_types.extend(Presets.FILE_TYPES)
                    return
    except FloodWait as e:
        await asyncio.sleep(e.x)
    except Exception:
        pass


# Function to find percentage of the total process
async def calc_percentage(sp, ep, message_id):
    const = pct = int()
    const = (ep - sp) + 1
    pct = ((message_id + const) - ep) / const * 100  # Credits to ma wife to find a formula !
    return pct


# Function to show the process graph
async def calc_progress(pct):
    progress = int()
    progress = (int(pct)//10 * "β¬οΈ " + (10-int(pct)//10) * "β»οΈ ")
    return progress


# Function to find DC Id:
async def find_dc(chat_status):
    dc = chat_status.dc_id
    dc_id = {dc == 1: "πΌππππ π΅π», πππ° [ππ π]", dc == 2: "π°ππππππππ, π½π» [ππ π]", dc == 3: "πΌππππ π΅π», πππ° [ππ π]",
             dc == 4: "π°ππππππππ, π½π» [ππ π]", dc == 5: "ππ’π§π ππ©π¨π«π, ππ [ππ π]"}.get(True)
    return dc_id

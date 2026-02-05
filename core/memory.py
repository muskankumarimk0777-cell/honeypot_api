import time

conversation_memory = {}
conversation_start_time = {}

def init_conversation(cid):
    if cid not in conversation_memory:
        conversation_memory[cid] = []
        conversation_start_time[cid] = time.time()

def add_message(cid, role, content):
    conversation_memory[cid].append({
        "role": role,
        "content": content
    })

def get_history(cid):
    return conversation_memory.get(cid, [])

def get_duration(cid):
    return int(time.time() - conversation_start_time.get(cid, time.time()))

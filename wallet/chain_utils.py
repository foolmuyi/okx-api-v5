import json
import os

def load_chain_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'chain_config.json')
    
    with open(json_path, 'r') as file:
        return json.load(file)

def get_chain_info(chain_id):
    config = load_chain_config()
    return config.get(str(chain_id))

def get_rpc_url(chain_id):
    chain_info = get_chain_info(chain_id)
    return chain_info['rpc_url'] if chain_info else None

def get_chain_name(chain_id):
    chain_info = get_chain_info(chain_id)
    return chain_info['name'] if chain_info else None

def get_supported_chain_ids():
    return list(load_chain_config().keys())

# 可选：添加一个函数来获取所有支持的链的信息
def get_all_chain_info():
    return load_chain_config()
import okex.Account_api as Account
import okex.Funding_api as Funding
import okex.Market_api as Market
import okex.Public_api as Public
import okex.Trade_api as Trade
import okex.subAccount_api as SubAccount
import okex.status_api as Status
import okex.Mktplace_api as Mktplace
from okex.utils import get_chain_id, get_chain_name
from wallet.Waas import Wallet
from dotenv import load_dotenv
import json
import os


debug_mode = True
if debug_mode == True:
    proxies = {
    'https://': 'http://127.0.0.1:7890/',
    'http://': 'http://127.0.0.1:7890/'
    }
else:
    proxies = None

if __name__ == '__main__':
    # load keys
    load_dotenv()
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('SECRET_KEY')
    passphrase = os.getenv('PASSPHRASE')

    # configs
    # collection example: https://www.okx.com/zh-hans/web3/marketplace/nft/collection/polygon/anichess-orbs-of-power
    chain = 'polygon'
    chainId = get_chain_id(chain)    # get chainId from chainName
    # chainId = 137
    # chain = get_chain_name(chainId)    # get chainName from chainId
    collectionAddress = '0x473989BF6409D21f8A7Fdd7133a40F9251cC1839'
    slug = 'anichess-orbs-of-power'
    tokenId = '3'
    walletAddress = '0x9e95a2ebb002e7eb6e0bea5fa4635feedd6f7f36'

    # create object
    MktplaceAPI = Mktplace.MktplaceAPI(api_key, secret_key, passphrase, proxies=proxies)

    # 说明：下列示例中均只使用了必需参数，具体的可选参数和相关说明见MktplaceAPI源代码
    # 获取单个NFT详情
    json_data = MktplaceAPI.get_nft_detail(chain, collectionAddress, tokenId)
    # 获取合集中的NFT列表
    # json_data = MktplaceAPI.get_nft_list(chain, collectionAddress)
    # 获取钱包中NFT资产列表
    # json_data = MktplaceAPI.get_asset_list(chain, walletAddress)
    # 获取单个合集详情
    # json_data = MktplaceAPI.get_collection_detail(slug)
    # 获取单链/全链合集列表
    # json_data = MktplaceAPI.get_collection_list()
    # 获取挂单信息
    # json_data = MktplaceAPI.get_listings(chain)
    # 获取出价订单
    # json_data = MktplaceAPI.get_offers(chain)
    # 购买NFT
    # json_data = MktplaceAPI.get_listings(chain, collectionAddress, tokenId)
    # orderId = json_data['data']['data'][0]['orderId']
    # tx_data = MktplaceAPI.buy_nft(chain, walletAddress, [{'orderId': orderId, 'takeCount': 1}])
    # wallet = Wallet(chainId)
    # json_data = wallet.call_contract(**tx_data)
    # 获取合集交易信息
    # json_data = MktplaceAPI.get_collection_trades(chain, collectionAddress)
    # 创建挂单
    # params = {'chain': chain, 'walletAddress': walletAddress, 'collectionAddress': collectionAddress, 
    #           'tokenId': tokenId, 'price': 99*(10**18), 'currencyAddress': '0x0000000000000000000000000000000000000000', 
    #           'count': 1, 'validTime': '2200000000', 'platform': 'okx'}
    # sign_data, order_data = MktplaceAPI.create_listing(**params)
    # wallet = Wallet(chainId)
    # signed_sign = wallet.get_signed_sign(sign_data)
    # json_data = MktplaceAPI.submit_listing(chain, walletAddress, signed_sign, order_data)

    # 格式化输出
    formatted_data = json.dumps(json_data, indent=4)
    print(formatted_data)
from .client import Client
from .consts import *


class MktplaceAPI(Client):

    def __init__(self, api_key, api_secret_key, passphrase, use_server_time=False, flag='0', proxies=None):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, proxies)

    def get_nft_detail(self, chain, contractAddress, tokenId):
        params = {'chain': chain, 'contractAddress': contractAddress, 'tokenId': tokenId}
        return self._request_with_params(GET, NFT_DETAIL, params)

    def get_nft_list(self, chain, contractAddress, cursor=None, limit=None):
        params = {'chain': chain, 'contractAddress': contractAddress, 'cursor': cursor, 'limit': limit}
        return self._request_with_params(GET, NFT_LIST, params)

    def get_asset_list(self, chain, ownerAddress, contractAddress=None, cursor=None, limit=None):
        params = {'chain': chain, 'ownerAddress': ownerAddress, 'contractAddress': contractAddress, 
                  'cursor': cursor, 'limit': limit}
        return self._request_with_params(GET, NFT_ASSET_LIST, params)

    def get_collection_detail(self, slug):
        params = {'slug': slug}
        return self._request_with_params(GET, NFT_COLLECTION_DETAIL, params)

    def get_collection_list(self, chain=None, cursor=None, limit=None):
        params = {}
        if chain:
            params['chain'] = chain
        if cursor:
            params['cursor'] = cursor
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, NFT_COLLECTION_LIST, params)

    def get_listings(self, chain, collectionAddress=None, tokenId=None, maker=None, createAfter=None, 
                     createBefore=None, updateAfter=None, updateBefore=None, status='active', platform=None,
                     sort='price_asc', limit=None, cursor=None):
        '''
        chain: 链名称
        collectionAddress: NFT 合约地址
        tokenId: NFT编号
        maker: 根据订单发起人钱包地址过滤
        createAfter: 只展示此时间戳之后的创建订单，单位为秒
        createBefore: 只展示此时间戳之前的创建订单，单位为秒
        updateAfter: 只展示此时间戳之后的更新订单，单位为秒
        updateBefore: 只展示此时间戳之前的更新订单，单位为秒
        status: 根据订单状态过滤，包括active、inactive、cancelled、sold
        platform: 目标挂单平台，详情见已经接入的市场，默认值为 okx
        sort: 订单排序规则，包括create_time_desc、update_time_desc、price_desc、price_asc。默认为根据时间正序排序
        limit: 单页条数限制，默认值为 50
        cursor: 查询指定订单页的游标参数
        '''
        params = {'chain': chain, 'collectionAddress': collectionAddress, 'tokenId': tokenId, 'maker': maker,
                  'createAfter': createAfter, 'createBefore': createBefore, 'updateAfter': updateAfter,
                  'updateBefore': updateBefore, 'status': status, 'platform': platform, 'sort': sort,
                  'limit': limit, 'cursor': cursor}
        return self._request_with_params(GET, NFT_LISTINGS, params)

    def get_offers(self, chain, collectionAddress=None, tokenId=None, maker=None, createAfter=None, createBefore=None,
                   updateAfter=None, updateBefore=None, status='active', sort='price_desc', limit=None, cursor=None):
        params = {'chain': chain, 'collectionAddress': collectionAddress, 'tokenId': tokenId, 'maker': maker,
                  'createAfter': createAfter, 'createBefore': createBefore, 'updateAfter': updateAfter,
                  'updateBefore': updateBefore, 'status': status, 'sort': sort, 'limit': limit, 'cursor': cursor}
        return self._request_with_params(GET, NFT_OFFERS, params)

    def buy_nft(self, chain, walletAddress, items):
        params = {'chain': chain, 'walletAddress': walletAddress, 'items': items}
        order_json = self._request_with_params(POST, NFT_BUY, params)
        errors = order_json['data']['errors']
        if errors == []:
            order_action = [step for step in order_json['data']['steps'] if step['action'] == 'TakeOrders'][0]
            tx_item = order_action['items'][0]
            order_tx = {}
            order_tx['chainId'] = tx_item['chain']
            order_tx['contractAddress'] = tx_item['contractAddress']
            order_tx['inputData'] = tx_item['input']
            order_tx['value'] = tx_item['value']
            return order_tx
        else:
            raise ValueError(errors)

    def get_collection_trades(self, chain, collectionAddress, tokenId=None, startTime=None, endTime=None, 
                              platform=None, limit=None, cursor=None):
        params = {'chain': chain, 'collectionAddress': collectionAddress, 'tokenId': tokenId, 'startTime': startTime,
                  'endTime': endTime, 'platform': platform, 'limit': limit, 'cursor': cursor}
        return self._request_with_params(GET, NFT_TRADES, params)

    def create_listing(self, chain, walletAddress, collectionAddress, tokenId, price, currencyAddress, 
                       count, validTime, platform):
        params = {'chain': chain, 'walletAddress': walletAddress, 'items': {'collectionAddress': collectionAddress, 
                  'tokenId': tokenId, 'price': price, 'currencyAddress': currencyAddress, 'count': count,
                  'validTime': validTime, 'platform': platform}}
        listing_json = self._request_with_params(POST, NFT_CREATE_LISTING, params)
        errors = listing_json['data']['errors']
        if errors == []:
            listing_action = [step for step in listing_json['data']['steps'] if step['action'] == 'SignOrders'][0]
            sign_item = listing_action['items'][0]
            sign_data = {}
            sign_data['domain'] = sign_item['domain']
            sign_data['types'] = sign_item['types']
            sign_data['primaryType'] = sign_item['primaryType']
            sign_data['message'] = sign_item['data']
            order_data = sign_item['data']
            return sign_data, order_data
        else:
            raise ValueError(errors)

    def submit_listing(self, chain, walletAddress, signature, order, platform='okx'):
        params = {'chain': chain, 'walletAddress': walletAddress, 'items': {'platform': platform, 
                  'signature': signature, 'order': order}}
        return self._request_with_params(POST, NFT_SUBMIT_LISTING, params)

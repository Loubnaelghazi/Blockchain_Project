import ipfshttpclient


class IPFSClient:
    def __init__(self, url="/ip4/127.0.0.1/tcp/5001"):
        self.client = ipfshttpclient.connect(url)

    def upload_file(self, file_path):
        res = self.client.add(file_path)
        return res["Hash"]

    def retrieve_file(self, ipfs_hash):
        return self.client.cat(ipfs_hash)

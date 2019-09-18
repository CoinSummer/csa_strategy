import time
import requests


current_milli_time = lambda: int(round(time.time() * 1000))

class WriteInfluxCli:
    def __init__(self, url):
        self.url = url
        self.data = []
        self.batch_size = 30
        self.session = requests.session()

    def stringify_tags(self, tags):
        tag_str = ''
        for kv in tags.items():
            tag_str += f",{kv[0]}={kv[1]}"
        return tag_str[1:]


    def write(self, name, tags, data, ts):
        try:
            tags_str = self.stringify_tags(tags)
            data_str = self.stringify_tags(data)
            data = f"{name},{tags_str} {data_str} {ts}000000"
            print(data)
            requests.post(url=self.url, data=data)
       
        except Exception as e:
            print(e)
    
    def add_point(self, name, tags, data, ts):
        try:
            tags_str = self.stringify_tags(tags)
            data_str = self.stringify_tags(data)
            line = f"{name},{tags_str} {data_str} {ts}000000"
            self.data.append(line)
            if len(self.data) >= self.batch_size:
                self.flush()
        except Exception as e:
            print(e)

    def len(self):
        return len(self.data)

    def flush(self):
        try:
            data = '\n'.join(self.data)
            print(data)
            requests.post(url=self.url, data=data)
            self.data = []
        except Exception as e:
            print(e)


if __name__ == "__main__":
    cli = WriteInfluxCli('http://localhost:8086/write?db=mydb')
    name = 'test_key'
    tags = { 'tag1': 'tag1', 'tag2': 'tag2' }
    data = { 'data1': 1, 'data2': 2 }
    cli.write(name, tags, data, current_milli_time())
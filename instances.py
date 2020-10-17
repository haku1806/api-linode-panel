import requests
import json as js
import time
import datetime
import random

class Instances:
    
    def __init__(self, api):
        self.api = api
        self.root_url = 'https://api.linode.com/v4/linode/instances/'
        self.list_linodes_id = {}
        self.list_linodes_full = {}
        
    def getListLinodes(self):
        self.url = self.root_url
        self.headers = {'Content-Type': 'application/json; charset=UTF-8',
               'Authorization': 'Bearer '+ self.api
               }
        self.r = requests.get(self.url, headers = self.headers)
        # return js.dumps(js.loads(r.text), indent=4)
        return js.loads(self.r.text)
    
    def printListLinodes(self):
        self.data = self.getListLinodes()
        self.list_linodes = self.data['data']
        self.count_linodes = self.data['results']
        
        # print(self.data)
        print("Tong VPS da tao la: ", self.count_linodes)
        
        print("+ {:-<4} + {:-^10} + {:->27} + {:->15} + {:->15} + {:->7} + {:->8} + {:->10} + {:->12} + {:->12} + {:->10} +".format('', '','','', '', '','', '', '','', ''))
        # print(region)
        print("| {:^4} | {:^10} | {:^27} | {:^15} | {:^15} | {:^7} | {:^8} | {:^10} | {:^12} | {:^10} | {:^12} |".format('STT','ID','LABEL','TAGS','IP','VCPUs','RAM(GB)','DISK(GB)','TRANSFER(TB)','Region','STATUS'))
        print("+ {:-<4} + {:-^10} + {:->27} + {:->15} + {:->15} + {:->7} + {:->8} + {:->10} + {:->12} + {:->12} + {:->10} +".format('', '','','', '', '','', '', '','', ''))
        for idx,i in enumerate(self.list_linodes):
            try:
                print("| {:^4} | {:^10} | {:^27} | {:^15} | {:^15} | {:^7} | {:^8} | {:^10} | {:^12} | {:^12} | {:^10} |".format(idx+1,i["id"],i["label"],i["tags"][0] if len(i["tags"])!=0 else 'None',i["ipv4"][0],i["specs"]["vcpus"],int(i["specs"]["memory"]/1024),int(i["specs"]["disk"]/1024),int(i["specs"]["transfer"]/1000),i["region"],i["status"]))
            except:
                print(i)
                
            self.list_linodes_id[idx+1] = i["id"]
            self.list_linodes_full[idx+1] = i
        print("+ {:-<4} + {:-^10} + {:->27} + {:->15} + {:->15} + {:->7} + {:->8} + {:->10} + {:->12} + {:->12} + {:->10} +".format('', '','','', '', '','', '', '','', ''))

        f = open('listIPVPS.txt','w')
        for idx, i in enumerate(self.list_linodes):
            f.write(i["ipv4"][0] + '\n')
        f.close()

    def selectTypeBoot(self, x):
        self.type = {1: 'khoi dong', 2: 'khoi dong lai', 3: 'tat', 4: 'xoa', 5: 'rescue'}
        
        self.printListLinodes()
        print() 
        try:
            print(f"Nhap 0 de {self.type[x]} tat ca VPS")
            self.service = int(input('Vui long nhap STT VPS yeu can ' + self.type[x] + ': '))

            if self.service == 0:
                # print(len(list_info_vps))
                for select in range(1,len(self.list_linodes_id)+1):
                    self.bootLinode(select,x)
            else:
                self.bootLinode(self.service,x)
        except:
            print("Ban chon sai.. Tro ve trang chinh")


    def bootLinode(self, linode_id, x):
            # type = ['boot', 'reboot', 'shutdown']
        self.type = {1: 'boot', 2: 'reboot', 3: 'shutdown', 4: 'delete', 5: 'rescue'}
        self._data = {}
        self._config = self.getListConfig(self.list_linodes_id[linode_id])
        # self._config.append()
        if x == 3:
            self.url = self.root_url + '{}/{}'.format(self.list_linodes_id[linode_id],self.type[x])
            self.headers = {'Content-Type': 'application/json; charset=UTF-8',
                'Authorization': 'Bearer '+ self.api
                }
        if x == 4:
            self.url = self.root_url + '{}'.format(self.list_linodes_id[linode_id])
        if x == 5:
            self.url = self.root_url + '{}/{}'.format(self.list_linodes_id[linode_id],self.type[x])
            self.disk = {"sda": {"disk_id": self.getListDisk(self.list_linodes_id[linode_id]), "volume_id": None}}
            # print(self.disk)
            self.headers = {'Content-Type': 'application/json; charset=UTF-8',
                    'Authorization': 'Bearer '+ self.api
                    } 
            self._data = {
                     "devices": self.disk    
                }    

        else:
            self.url = self.root_url + '{}/{}'.format(self.list_linodes_id[linode_id],self.type[x])
            self.headers = {'Content-Type': 'application/json; charset=UTF-8',
                'Authorization': 'Bearer '+ self.api
                
                }
            # self._data = {
            #  "configs": int(self._config)
            # }

        self.r = requests.post(self.url, headers = self.headers, data= self._data)
        self.data = js.loads(self.r.text)
        if x == 1:
            try:
                print(self.data["errors"][0]["reason"])
            except:
                print(f"VPS {linode_id} dang duoc khoi dong")
            # print(data["errors"][0]["reason"])
        elif x == 2:
            try:
                print(self.data["errors"][0]["reason"])
            except:
                print(f"VPS {linode_id} dang duoc khoi dong lai")
        elif x == 3:
            try:
                print(self.data["errors"][0]["reason"])
            except:
                print(f"VPS {linode_id} dang duoc tat")
        elif x == 5:
            try:
                print(self.data["errors"][0]["reason"])
            except:
                print(f"VPS {linode_id} dang duoc {self.type[5]}")
        else:
            pass
            try:
                # print(self.data["errors"][0]["reason"])
                print(self.data["errors"])
            except:
                print(f"VPS {linode_id} dang duoc xoa")
        # print(f"VPS hien dang duoc {type[x]}")
        return js.dumps(js.loads(self.r.text), indent=4) 

    def menuGetInfoDiskConfigLinode(self):
        self.printListLinodes()
        # print(self.list_linodes_id)
        try:
            self.service = int(input('Vui long nhap STT VPS can lay thong tin disk, config : '))
            print('Config ID: {}'.format(self.getListConfig(self.list_linodes_id[self.service])))
            print('Disk ID: {}'.format(self.getListDisk(self.list_linodes_id[self.service])))
        except:
            print("Ban chon sai.. Tro ve trang chinh")
    
    def getListDisk(self, x):
        self.url = self.root_url + '{}/disks'.format(x)
        self.headers = {'Content-Type': 'application/json; charset=UTF-8',
                'Authorization': 'Bearer '+ self.api
                }
        self.r = requests.get(self.url, headers = self.headers)
        # return js.dumps(js.loads(r.text), indent=4)
        self.data = js.loads(self.r.text)["data"]
        return self.data[0]["id"]
    
    def getListConfig(self, x):
        self.url = self.root_url + '{}/configs'.format(x)
        self.headers = {'Content-Type': 'application/json; charset=UTF-8',
                'Authorization': 'Bearer '+ self.api
                }
        self.r = requests.get(self.url, headers = self.headers)
        # return js.dumps(js.loads(r.text), indent=4)
        self.data = js.loads(self.r.text)["data"]
        return self.data[0]["id"]
    
    def menuCloneLinode(self):
        self.printListLinodes()
        print()
        # try:
        self.service = int(input('Vui long nhap STT VPS can clone : '))
        self.name = input('Vui long nhap ten VPS can clone: ')
        self.count = int(input('Vui long nhap so luong VPS can clone (min 1, max 5): '))
        for select in range(1,self.count+1):
            print(f"Dang clone VPS lan {select}")
            print(self.cloneLinode(self.service, self.list_linodes_id[self.service], self.name))
            
        # except:
        #     print("Ban chon sai.. Tro ve trang chinh")
            
    def cloneLinode(self, x, linode_id, name):
        self._datetime = datetime.datetime.now()
        # self.url = self.root_url + '{}/clone'.format(linode_id)
        self.list_disk = [self.getListDisk(linode_id)]
        self.list_config = [self.getListConfig(linode_id)]
        
        self.headers = {
            "Content-Type": "application/json",
            'Authorization': 'Bearer '+ self.api 
        }
        
        self._body = {
            "region": self.list_linodes_full[x]["region"],
            "type": self.list_linodes_full[x]['type'],
            "backups_enabled": False,
            "label": '{}{}'.format(name,random.randint(10,100)),
            "group": self._datetime.strftime("%d-%m-%Y"),
            "disks": self.list_disk,
            "configs": self.list_config
        }
        print(self._body)
        self.url = self.root_url + '{}/clone'.format(linode_id)
        print(self.url)
        # print(self.list_linodes_full)
        print('{}, {}, {}'.format(self.url, self.headers, self._body))
        self.r = requests.post(self.url, headers = self.headers, data = self._body)
        self.data = js.loads(self.r.text)
        return self.data
        # return 1
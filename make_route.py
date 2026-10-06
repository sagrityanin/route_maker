import json
import subprocess
import re

GW = "10.5.0.27"
LOG_FILE = "route_make.log"

class Ip:
    def get_aws_ip(self, file="ip-ranges.json") -> list:
        ip_list = []
        with open(file) as f:
            d = json.load(f)
        for item in d["prefixes"]:
            ip_list.append(item["ip_prefix"])
        return ip_list
    
    def get_azure_ip(self, file="ServiceTags_Public_20260928.json") -> list:
        ip_list = []
        with open(file) as f:
            d = json.load(f)
        for item in d["values"]:
            ip_list.extend(item["properties"]["addressPrefixes"])
        return ip_list

    def get_arg(self) -> bool:
        print("Для добавления маршрутов введите 'y', для удаления - 'n'")
        s = input()
        if "y" in s.lower() or "n" in s.lower():
            return s
        print("Введеноне правильное значение")
        return False       
 
    def add_route(self, ins: str, ip_list: list) -> bool:
        with open(LOG_FILE, "w") as f:
            for item in ip_list:
                if self.is_valid_ip(item):
                    if ins == "y":
                        command = f"ip route add {item} via {GW}"
                    if ins == "n":
                        command = f"ip route del {item} via {GW}"
                    f.write(f"{command}\n")
                    cp = subprocess.run(command, shell=True, text=True, capture_output=True)
                    if cp.stdout:
                        f.write(f"{cp.stdout}")
                    if cp.stderr:
                        f.write(f"{cp.stderr}")
                    f.write(f"{str(cp.returncode)}\n")
                else:
                    f.write("Not ip v4\n")

    def is_valid_ip(self, ip) -> bool:
        m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})", ip)
        return m

    def handler(self):
        ins = False
        while ins is False:
            ins = self.get_arg()
        all_ip_list = []
        all_ip_list.extend(self.get_aws_ip())
        # all_ip_list.extend( self.get_azure_ip())
        self.add_route(ins, all_ip_list)
    
    
    
if __name__ == "__main__":
    Ip().handler()
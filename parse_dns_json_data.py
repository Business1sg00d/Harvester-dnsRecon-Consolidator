#!/usr/bin/env python3




import json
import sys
import os




def dnsreconp(dnspath, sub_domain):
    for file in os.listdir(dnspath):
        file_path = os.path.join(dnspath, file)
        with open(file_path) as j:
            data = json.load(j)

            for i in range(len(data)):
                try:
                    if data[i]["domain"]:
                        domain = data[i]["domain"]
                        if domain not in sub_domain:
                            sub_domain[domain] = []
                        if ":" not in data[i]["address"] and data[i]["address"][0].isdigit():
                            if data[i]["address"] not in sub_domain[domain]:
                                sub_domain[domain].append(data[i]["address"])
                except KeyError:
                    continue

    return sub_domain




def harvesterp(harvest_path, sub_domain):
    for file in os.listdir(harvest_path):
        if ".json" not in file: continue
        file_path = os.path.join(harvest_path, file)
        with open(file_path) as j:
            data = json.load(j)
            try:
                if data["hosts"]:
                    key_value = data["hosts"]
                    for i in range(len(key_value)):
                        domain = key_value[i].split(":")[0]
                        try:
                            addresses = (key_value[i].split(":")[1]).split(",")
                        except IndexError:
                            continue
                        if domain not in sub_domain:
                            sub_domain[domain] = []
                        for ip in range(len(addresses)):
                            address = addresses[ip].strip()
                            if ":" not in address and address[0].isdigit():
                                if address not in sub_domain[domain]:
                                    sub_domain[domain].append(address)
            except KeyError:
                continue

    return sub_domain




def main():
    dnspath = sys.argv[1]
    harvest_path = sys.argv[2]
    files = []
    sub_domain = {}

    if not os.path.isdir(dnspath):
        print("Error: {} is not a valid directory".format(dnspath))
        sys.exit(1)

    if not os.path.isdir(harvest_path):
        print("Error: {} is not a valid directory".format(harvest_path))
        sys.exit(1)

    harvesterp(harvest_path, sub_domain)
    dnsreconp(dnspath, sub_domain)

    for domain,addresses in sub_domain.items():
        print(domain)
        print('\n'.join(addresses))
        print('\n')




if __name__=="__main__":
    main()

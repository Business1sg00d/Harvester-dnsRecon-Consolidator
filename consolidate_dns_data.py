#!/usr/bin/env python3




from json2html import *
import json
import sys
import os




def nameserver(data, sub_domain):
    try:
        if not data["address"]: return sub_domain
        if ":" not in data["address"] and data["address"][0].isdigit():
            ip_address_ns = data["address"]
        if "ip_address_ns" not in locals(): return sub_domain
        if ip_address_ns not in sub_domain[data["domain"]]:
            combined_name_ip = "NameServer" + " -> " + data["target"] + ":" + ip_address_ns
            sub_domain[data["domain"]].append(combined_name_ip)
    except UnboundLocalError:
        breakpoint()

    return sub_domain




#   Takes json files in dnsrecon directory path and consolidates IPv4 addresses and subdomains into "sub_domain"
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
                        if data[i]["type"] == "NS":
                            nameserver(data[i], sub_domain)
                            continue
                        if ":" not in data[i]["address"] and data[i]["address"][0].isdigit():
                            ip_address = data[i]["address"]
                        if ip_address not in sub_domain[domain]:
                            sub_domain[domain].append(ip_address)
                        if data[i]["name"] and ip_address:
                            combined_name_ip = data[i]["name"] + " : " + ip_address
                            sub_domain[domain].append(combined_name_ip)
                except KeyError:
                    continue

    return sub_domain




#   Takes json files in Harvester directory path and consolidates IPv4 addresses and subdomains into "sub_domain"
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
                            else:
                                cloud_names = ('aws', 'cloudfront')
                                for name in cloud_names:
                                    if name not in address: continue
                                    else:
                                        for key, value in sub_domain.items():
                                            for a_record in value:
                                                if ":" not in a_record: continue
                                                if address in a_record: continue
                                                else: sub_domain[domain].append(address)
            except KeyError:
                continue

    return sub_domain




#   Converts sub_domain into an html files for browser viewing
def json_to_html(sub_domain):
    with open('data.html', 'w') as f:
        html = json2html.convert(json.dumps(sub_domain))
        f.write(html)
        f.close()




def main():
    dnspath = sys.argv[1]
    harvest_path = sys.argv[2]
    sub_domain = {}

    if not os.path.isdir(dnspath):
        print("Error: {} is not a valid directory".format(dnspath))
        sys.exit(1)

    if not os.path.isdir(harvest_path):
        print("Error: {} is not a valid directory".format(harvest_path))
        sys.exit(1)

    harvesterp(harvest_path, sub_domain)
    dnsreconp(dnspath, sub_domain)
    json_to_html(sub_domain)




if __name__=="__main__":
    main()
    exit(0)

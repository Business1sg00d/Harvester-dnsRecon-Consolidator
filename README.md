# Harvester-dnsRecon-Consolidator
Take json files in Harvester output directory and dnsrecon directory; combine into one XML/json file. Work in progress.

Install:
--------
```pip install json2html```

Usage:
------
```./consolidate_dns_data.py /path/to/dnsrecon/json_files /path/to/Harvester/json_files```

Should output "data.html"

```firefox data.html```

Still testing

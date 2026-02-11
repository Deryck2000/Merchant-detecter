# Merchant-detecter
for Sol's RNG  
Uses EasyOCR to read the latest chat message, detect merchants, and trigger Webhook  
<a href="https://blog.codinghorror.com/the-works-on-my-machine-certification-program/"><img src="https://raw.githubusercontent.com/Deryck2000/Merchant-detecter/refs/heads/main/something/works-on-my-machine-v2.webp"></img></a>

i made this for myself, but i also put it on github  
logs only japanese sry  

## Requirement
- Python
- pip

## How to use
1. Download latest release and unzip
1. Edit `config.json`  
   - `webhook_url` : your webhook url  
   - `mention` : user/role id if u use discord
   - `check_interval_seconds` : scan chat interval seconds
   - `scan_area` : scan area, example :  
     <img src="https://raw.githubusercontent.com/Deryck2000/Merchant-detecter/refs/heads/main/something/area-example.png"></img>  
     and u can get params with run `range_check.bat`
1. Run `START.bat` 

 i missed mari twice while writing this

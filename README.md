# GTAV-Image-Downloader

With this Script, you can download all Images for Vehicles, Weapons, and Peds from the alt:V Documentation.

# Usage

```pip3 install -r requirements.txt```<br>
```python3 dump.py```

| Option  | Default           | Other  
| ------- | ------------------ | ------------------ 
| -o | fetch | fetch / zip / both
| -r | alt:V | alt:V / alt:V2 / rage / fivem

Examples:<br>
```python3 dump.py -o both -r rage```<br>
```python3 dump.py -o fetch -r alt:V2```

## Output

The Script will output the Images files in the following structure:<br>
```
/images/ped for the peds
/images/weapon for the weapons
/images/vehicle for the vehicles
```

If you choose the option ```-o zip``` or ```-o both``` then there will be a folder called ```zips``` with the following output:<br>
```
/zips/ped.zip
/zips/weapon.zip
/zips/vehicle.zip
```

# Source
You can choose between these sources:<br>
| Source  | Vehicles           | Peds  | Weapons | type | maintained | link | Downloader Type
| ------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| alt:V (Docs) | :white_check_mark: | :white_check_mark: | :white_check_mark: | png | :white_check_mark: | https://docs.altv.mp | Docs
| alt:V (Wiki) | :white_check_mark: | :white_check_mark: | :white_check_mark: | png | :x: | https://wiki.altv.mp | Wiki
| Rage | :white_check_mark: | :x: | :x: | png | :white_check_mark: | https://wiki.rage.mp | Wiki
| Fivem | :x: | :white_check_mark: | :x: | webp | :white_check_mark: | https://docs.fivem.net | Docs

The Default is alt:V (Docs).

# Downloader Types
| Name  | Speed | Note | 
| ------- | ------------------ | ------------------ |
| Docs | Fast | 
| Wiki | Slow | approximately 100x slower than Docs
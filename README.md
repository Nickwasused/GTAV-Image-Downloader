# GTAV-Image-Downloader

With this Script, you can download all Images for Vehicles, Weapons, and Peds from the alt:V Documentation.

# Usage

```pip3 install -r requirements.txt```<br>
```python3 dump.py```

## Output

The Script will output the Images files in the following structure:<br>
```
/images/ped for the peds
/images/weapon for the weapons
/images/vehicle for the vehicles
```

If you choose option ```-o zip``` or ```-o both``` then there will be a folder called ```zips``` with the following output:<br>
```
/zips/ped.zip
/zips/weapon.zip
/zips/vehicle.zip
```

# Source
You can choose between this sources:<br>
| Source  | Vehicles           | Peds  | Weapons | type | maintained | link
| ------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| alt:V (Docs) | :white_check_mark: | :white_check_mark: | :white_check_mark: | png | :white_check_mark: | https://docs.altv.mp
| alt:V (Wiki) | :white_check_mark: | :white_check_mark: | :white_check_mark: | png | :x: | https://wiki.altv.mp
| Rage | :white_check_mark: | :x: | :x: | png | :white_check_mark: | https://wiki.rage.mp
| Fivem | :x: | :white_check_mark: | :x: | webp | :white_check_mark: | https://docs.fivem.net

The Default is alt:V (Docs).
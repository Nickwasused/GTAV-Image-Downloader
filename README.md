# GTAV-Image-Downloader

With this Script, you can download all Images for Vehicles, Weapons, and Peds from the alt:V Documentation.
After creating the script I noticed you can download the images from here: https://github.com/altmp/altv-docs-assets/tree/master/altv-docs-gta/images

# Usage

```pip3 install -r requirements.txt```<br>
```python3 dump.py```

| Option  | Default           | Other  
| ------- | ------------------ | ------------------ 
| -o | fetch | fetch / zip / both

Examples:<br>
```python3 dump.py -o both```<br>
```python3 dump.py -o fetch```

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

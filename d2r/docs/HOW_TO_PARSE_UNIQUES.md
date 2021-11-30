# How to parse UniqueItems

# Can Mephisto drop Arachnid Mesh?

## UniqueItems.txt

`Arachnid Mesh`
```
lvl == 87
*type == spiderweb sash
```

Check `Weapons.txt` and `Armor.txt` for
```
name == spiderweb sash
```

## Dynamic TC
Now we need to find the dynamic TC this would belong to

if found in `Armor.txt` the string will be `armo##`

if found in `Weapons.txt` the string will be `weap##`

Take the level from THE BASE ITEM TYPE (`spiderweb sash`) and round it to a multiple of 3, starting at 3.

Since `61` rounds up to the nearest multiple of 3 to `63` just put it on the end of the string `armo63`.  Mephisto's TC list must contain this.

## Can [Boss] drop [Item]
**To be able to drop Arachnid mesh the following must be true:**
```
Mephisto's level (87) vs Arachnid Mesh lvl (87)

AND

TC of the Base item level (Spiderweb Sash, 61) rounded to (63) `armo63` must be in Mephisto's TCs.
```
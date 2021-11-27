# Files

## MonStats.txt
Used to get monsters (Bosses) and their TCs

* Id
* NameStr
* Level
* Level (N)
* Level (H)
* TreasureClass#(?)

```
TreasureClass1: the TreasureClass used by this unit as a normal monster on the respective difficulties.

TreasureClass2: the TreasureClass used by this unit as a champion on the respective difficulties.

TreasureClass3: the TreasureClass used by this unit as a unique or superunique on the respective difficulties.

TreasureClass4: the Quest TreasureClass used by this monster. (For example, the act bosses always have better odds of dropping rare, set and unique items the first time you kill them).
```

## SuperUniques.txt
Used to get SuperUnique monsters like `Pindleskin` and `Nihlathak Boss`.

* Superunique
* Name
* Class (corresponds to `Id` from `MonStats.txt`)
* TC, TC(N), TC(H)

## Levels.txt
* Name
* MonLvl1Ex, MonLvl2Ex, MonLvl3Ex
* LevelName

---

## Notes

https://www.diabloii.net/forums/threads/how-has-pindle-changed-since-1-09.428922/
```
Since patch 1.10, the monsters mlvl on NM and Hell are the same as the area level, rather than using their preset mlvl found in monstats.txt.

Pre 1.10, Pindleskin used to be mlvl ** (reanimatedhorde5 = mlvl 85, superunique = +3). Since area levels are now used, the reanimatedhorde creatures found in Niths temple are now mlvl 83 (Act 5 - Temple Entrance = area level 83), which means Pindleskin is now mlvl 86.

Edit: This also applies for patch 1.11, which didn't change anything from 1.10 with regards to this.
```
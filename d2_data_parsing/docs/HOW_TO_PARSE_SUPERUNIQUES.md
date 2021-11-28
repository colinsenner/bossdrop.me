# How to parse SuperUnique monsters

# TODO
* Figure out what area SuperUniques are in automatically
* In levels.txt mon3 contains `fallenshaman1` which Bishibosh is, but there's two rows which have that `Act 1 - Cave 1` and `Act 1 - Wilderness 2`.

---

# Pindleskin
## SuperUniques.txt (Used to get class of the mob)
```
Class == reanimatedhorde5
```

## MonStats.txt (Used to get Normal level)
```
reanimatedhorde5['Level'] == 42
```

*Note levels aren't used for NM and H here, area level is used instead*

## Levels.txt (Used to get NM and H Monster levels)
```
LevelName == Nihlathaks Temple
```

```
MonLevel2Ex = 63
MonLevel3Ex = 83
```

Since `Pindleskin` is a SuperUnique he gets **+3** to this level, so his levels on each difficulty are:

```
Normal: 45
Nightmare: 66
Hell: 86
```

Compared against `https://diablo.fandom.com/wiki/Pindleskin`

---

# Bishibosh
## SuperUniques.txt (Used to get class of the mob)
```
Class == fallenshaman1
```

## MonStats.txt (Used to get Normal level)
```
fallenshaman1['Level'] == 2
```

*Note levels aren't used for NM and H here, area level is used instead*

## Levels.txt (Used to get NM and H Monster levels)
```
LevelName == Cold Plains
```

```
MonLevel2Ex = 36
MonLevel3Ex = 68
```

Since `Bishibosh` is a SuperUnique he gets **+3** to this level, so his levels on each difficulty are:

```
Normal: 5
Nightmare: 39
Hell: 71
```

Compared against `https://diablo.fandom.com/wiki/Bishibosh`

---

# How to calculate drop chances

## Notes on fields
```
Picks: This column has two different functions, depending on the type of values you enter (either positive 0-6 or negative, -1 to -6).
In the first case this is used as the number of loops to run the “pick drop” routine, in the second case it is used to determine exactly which items, and how many of each, to drop (see appendix).
You cannot make the game drop more then 6 items with either method without code editing (there are other txt based methods to drop more then 6 items though).
```

## Corpsefire (normal)

Level: 4
Area: Den of Evil (Act 1 - Cave 1)

Corpsefire drops from TC `Act 1 Super A`

### TreasureClassEx

```
Act 1 Super A
    Picks: -4
    NoDrop: 0

    Item1: Act 1 Uitem A // 2
    Item2: Act 1 Cpot A // 2

    Act 1 Uitem A
        Picks: 1
        NoDrop: 0

        Item1: Act 1 Equip A // 58
        Item2: Act 1 Good // 4

        Act 1 Equip A
            Picks: 1
            NoDrop: 0

            Item1: weap3 // 7
            Item2: armo3 // 7

        Act 1 Good
            Picks: 1
            NoDrop: 0

            Item1: Jewelry A // 5
            Item2: Chipped Gem // 5

        Jewelry A
            Picks: 1
            NoDrop: 0

            Item1: rin // 8
            Item2: amu // 4
            Item3: jew // 2
            Item4: cm3 // 2
            Item5: cm2 // 2
            Item6: cm1 // 2

        Chipped Gem
            Picks: 1
            NoDrop: 0

            Item1: gcv // 3
            Item2: gcy // 3
            Item3: gcb // 3
            Item4: gcg // 3
            Item5: gcr // 3
            Item6: gcw // 3
            Item7: skc // 2

    Act 1 Cpot A
        Picks: 2
        NoDrop: 0

        Item1: Hpotion 1 // 1

        Hpotion 1
            Picks: 1
            NoDrop: 0

            Item1: hp1 // 8
            Item2: hp2 // 3
            Item3: mp1 // 3
            Item4: mp2 // 2
            Item5: rvs // 1
```
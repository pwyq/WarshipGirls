# Extreme Logistics

I only calculate for the oil resource as it is THE most important natural resource in the game.

- Because of the existence of weeekly tasks, we take one week as a calculation cycle for simplicity
- Assume big success rate of expedition is 65% and 4 Tenryus as the flagship of expedition
- Assume no other equipment to boost the outcome
- Assume resources are below the auto restore limit
- 168 hours / week
- we define following formula:

```
BS = 0.65   # big success rate
BG = 1.50   # big success gain
TL = 1.08   # Tenryus effect
NG = 1.00   # normal gain

def single_map(runs, amount):
    x = math.floor(runs * BS)
    y = runs - x
    # big_success_res = x * amount * BG * TL
    # normal_res      = y * amount * NG * TL
    return (x*BG + y*NG) * amount * TL 
```

## OIL

| Map | Time (hr) | Single Run Result | Max Possible Runs | Comments |
|:---:|:----:|:-----------------:|:-----------------:|:--------:|
| 6-1 | 9 | 800 | floor(168/9) = 18 | 6 hours left |
| 2-1 | 2 | 150 | floor(168/2) = 84 | |
| 3-1 | 4 | 350 | floor(168/4) = 42 | |
| 1-3 | 0.5 | 30 | floor(168/0.5) = 336 | |
| 5-3 | 1 | 60 | 6 | reason see below |

To make up the extra 6 hours due to odd running hours of the 6-1, we have following possible plans:  
- 1 * 4-1 + 2 * 5-3
- 6 * 5-3
- 3 * 5-2

Intuitively, we note that given final gain constant, the more expeditions we run, the more resource gain will be.
Therefore, we will choose plan `6 * 5-3` here.

```
For daily tasks, there are three tasks which are randomly chosen as well as their outcomes.
Among the three tasks, only two are awarded resources, the rest is awarded a random ship core.

For oil, the expected value of the discrete case (200,150,100,200,150,0,300,300) is

E[X] = 200 * 1/8 + 150 * 1/8 + 100 * 1/8 + 200 * 1/8 + 150 * 1/8 + 0 * 1/8 + 300 * 1/8 + 300 * 1/8
     = 175
```

### Summary

```
# Expedition
>>> single_map(18,800) + single_map(84,150) + single_map(42,350) + single_map(336,30) + single_map(6,60)
74169.0

# Campaign
>>> 200 * 8 * 7
11200

# Daily auto restore
>>> 60 * 24 * 7
10080

# Daily Tasks
# 击退敌军舰队 + 击破敌军主力 + 击退敌军舰队10次 + 随机两任务 + 常规[演习] + 胜利的滋味 + 常规[远征] + [远征]大成功！ + 舰队休整 + 舰队补给 + [开发]新装备 + [建造]新船只 + [强化]船只 + 食堂开饭
>>> (30 + 50 + 100 + 175 * 2 + 30 + 50 + 30 + 50 + 100 + 100 + 10 + 30 + 30 + 100) * 7
7420

# Weekly Tasks
大获全胜 + 打击敌军 + 7图周常 + 大规模[演习] + 大规模远征作战 + 补充舰队装备 + 补充舰队船只 + 补充舰队船只 + 港区食神
>>> 300 + 200 + (400 + 500 + 1000 + 0 + 0 + 0 + 1000) + 200 + 200 + 200 + 500 + 200 + 500
5200

# Total
>>> 74169 + 11200 + 10080 + 7420 + 5200
108069
```

If we optimize quotidian consumptions, we are able to get an exciting amount of **100k** oil per week!

---

# 量产型最佳装备

(UNDER CONSTRUCTION)

## BB, BC

## CA

## DD

## SS

## CV

## CVL


### 贩卖军火

原制作于16年的目标装备表（待更新）

- 三式弾 0/6; 九一式徹甲弾 10/24; VT引信炮弹 4/N
- 晴嵐 1/12; 紫雲 1/12; 景雲 1/12; Supermarine Seafang 13/24; Wyvern 6/36; B-25 Mitchell 1/72; 流星 21/36； 
- 发烟筒 4/24; 动力系统 改良型15/24, 先进型 5/24; Hedgehog 2/12; Bofors-40mm-gun (quadruple) 55/N, (hexatruple) 10/N.
- 四连533mm磁性鱼雷 16/N; MK17鱼雷 6/N; 61cm三連酸 8/N, 四連酸 17/24, 五連酸 0/N
- MK6 24/N; 早期型MK7 1/N; 德双连406mm炮 3/N; 法四连380mm炮 7/N; 英三联16-inch炮(改) 2/N
- 美三联8-inch重弹炮 13/N; 日20.3cm连装炮 6/N; 苏三联180mm炮 17/N; 超重弹 13/N
- Kriegsmarine: U47 5/12; U81 1/3; U96 1/3; U156 0/6; U505 5/6
- USN: Tang 6/6; Archerfish 7/12; Albacore 13/12
- RN: M1 2/4
- Marine national francaise: Surcouf 1/2

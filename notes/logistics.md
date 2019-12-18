_Resource logistics is one of the most crucial and indispensible factors in the game, which fascinates me the most._

__Content__

- [General Game Plan](#general-game-plan)
- [Extreme Collection of Oil](#extreme-collection-of-oil)
- [Strategic Reserve](#strategic-reserve)

---

# General Game Plan

本提督结合自身经验总结出以下口诀。

二十四字后勤口诀：

> “全力跑油，日常炸鱼。油满偷弹，弹满偷铝。如此往复，无往不利。”

八字收集口诀：

> “先建后捞，先大后小。”

十六字备战口诀：

> “练度为王，霸业次之。肝有余力，请君养殖。”

后勤口诀解释：油是最重要的资源。油生万物。炸鱼可以获得用不完的钢材。铝的自然回复最慢，所以把多余的油弹转化为铝。

收集口诀解释：先建造毕业，后打捞毕业。因为建造比打捞容易很多，而且打捞对于练度要求高。先造大船，后造小船。因为大船公式包含了稀有小船。

备战口诀解释：满级满战术满强化神装白板船可以打十个苏日天。一级稀有船上场和送钱无异。有多余的精力，可以考虑养殖装备。

### 一些要点

- 有活动期间
    - 战利品活动 -> 适度打捞
    - 圣肝 -> 练中大型船（CA, BB, BC, CA, AV）
    - 有出门夜战点 -> 练技能
- 无活动期间
    - 维持油弹铝在低保线下5k-10k
    - 练中小型船（SS, DD, CL, CA, CVL）
- 资源不平衡 -> 大建 / 练大船

---

# Extreme Collection of Oil

I only calculate for the oil resource as it is THE most important natural resource in the game.

- Because of the existence of weekly tasks, we take one week as a calculation cycle for simplicity
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

If we optimize quotidian consumptions, we are able to get an exciting amount of over **100k** oil per week!

---

# Strategic Reserve

- Following resources are per unit
- Last update: 191214

| Name | Total Units | Oil | Ammo | Steel | Aluminium | Others |
|:----:|:------:|:---:|:----:|:-----:|:---------:|:------:|
| 金块箱 | 39 | 450 | 450 | 450 | 120 | |
| 极密货物 | 9 | 235 | | | | |
| 月卡 | 59 | 500 | 500 | 500 | 500 | 舰船蓝图(1) |
| 191213 | 1 | 1000 | 1000 | 1000 | 1000 | 快建(1), 舰船蓝图(1) |
| 180330 | 1 | 1500 | 1500 | 1500 | 1500 | 快建(1), 舰船蓝图(1) |
| 170922 | 1 | 1000 | 1000 | 1000 | 1000 | |
| 170802 | 1 | 810 | 810 | 810 | 810 | 损管(1) |
| 170516 | 1 | 40000 | 30000 | 30000 | 30000 | 快修(100) |

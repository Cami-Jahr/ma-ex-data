import helpers

text = """{{{{Kioku Infobox
|id                  = {id}
|image               = {id}_original.png
|name_en             = {name_en}
|name_jp             = {name_jp}
|character_en        = {character_en}
|character_jp        = {character_jp}
|characterid         = {characterId}
|rarity              = {rarity}
|element             = {element}
|role                = {role}
|date                = {releaseDate}
}}}}
'''{name_en}''' is a [[Kioku]] for [[{character_en}]] obtained from [[Fate Weaves]].

==Kioku Details==
The maxed enhancement values shown reflect the stats and skill effects at max ascension, max level, and max Magic level.

Additional stats from [[Heartphial]]s are not reflected.

===Stats===
====Base====
{{{{Kioku Stats
|hp  = {minHp}
|atk = {minAtk}
|def = {minDef}
|spd = {minSpd}
|ep = {minEp}
|crit rate = {minCritRate}
|crit damage = {minCritDmg}
}}}}
====Max====
{{{{Kioku Stats
|hp  = {maxHp}
|atk = {maxAtk}
|def = {maxDef}
|spd = {maxSpd}
|ep = {maxEp}
|crit rate = {maxCritRate}
|crit damage = {maxCritDmg}
}}}}
"""

# getStyleLevelUpMstList
## Levels from magia lvl 120 and lvl 300?
#  Unsure. Homura 120 has +2700HP, but this lists 4725, includes something more?

# getStyleLimitBreakMstList
## Ascension increase rewards
## Value refers to getStyleLimitBreakEffectMstList whose value fields refer to getPassiveSkillMstList

# getStyleParamUpMstList
## THis is magia level increase rewards and costs
element_map = {1: "Flame", 2: "Aqua", 3: "Forest", 4: "Light", 5: "Dark", 6: "Void"}
role_map = {
    1: "Attacker",
    2: "Breaker",
    3: "Healer",
    4: "Buffer",
    5: "Debuffer",
    6: "Defender",
}


def fix_date(date: str) -> str:
    date = date[:10]
    if date == "2024-01-01":
        return "2024-03-26"
    return date


def create_kioku_pages():
    kiokus = helpers.get_both("getStyleMstList.json", "styleMstId")
    characters = helpers.get_both("getCharacterMstList.json", "characterMstId")

    for kioku_en in kiokus["en"].values():
        if not kioku_en["isCollectionDisp"]:
            # These are tutorial etc characters, only want to make pages for actual collectable characters
            continue
        characterId = int(str(kioku_en["styleMstId"])[:4])
        kioku_jp = kiokus["jp"][kioku_en["styleMstId"]]

        kioku_en["PLACEHOLDER"] = "PLACEHOLDER"
        # TODO Check what these does and add them
        #  "specialAttackMstId": 1150,
        #  "normalAttack": 1148,
        #  "skill1": 1149,
        #  "passiveSkill1": 15009,
        #  "limitBreakPassiveSkill1": 0,
        #  "subPassiveSkill": 95009,
        #  "leaderSkill": 12000,
        # ep (mana?)
        # recoveryEpRate

        # NOTE: There are *Rate fields which currently are all 0 so I ignore them
        #  but might be needed in the future
        with open(
            f"wiki/kioku_pages/{kioku_en["name"]}.txt", "w", encoding="utf-8"
        ) as g:
            print(
                text.format(
                    id=kioku_en["styleMstId"],
                    name_en=kioku_en["name"],
                    name_jp=kioku_jp["name"],
                    characterId=characterId,
                    character_jp=characters["jp"][characterId]["name"],
                    character_en=characters["en"][characterId]["name"],
                    rarity=kioku_en["rarity"],
                    element=element_map[kioku_en["element"]],
                    role=role_map[kioku_en["role"]],
                    releaseDate=fix_date(kioku_en["releaseTime"]),
                    minHp=kioku_en["hp"],
                    minAtk=kioku_en["atk"],
                    minDef=kioku_en["def"],
                    minEp=kioku_en["ep"],
                    minSpd=kioku_en["speed"],
                    minCritRate=kioku_en["criticalRate"],
                    minCritDmg=kioku_en["criticalDamageRate"],
                    maxHp=kioku_en["PLACEHOLDER"],
                    maxAtk=kioku_en["PLACEHOLDER"],
                    maxDef=kioku_en["PLACEHOLDER"],
                    maxEp=kioku_en["PLACEHOLDER"],
                    maxSpd=kioku_en["PLACEHOLDER"],
                    maxCritRate=kioku_en["PLACEHOLDER"],
                    maxCritDmg=kioku_en["PLACEHOLDER"],
                ),
                file=g,
            )


if __name__ == "__main__":
    create_kioku_pages()

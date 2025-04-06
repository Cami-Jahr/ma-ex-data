import helpers
import re
import json

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
|hp           = {minHp}
|atk          = {minAtk}
|def          = {minDef}
|spd          = {minSpd}
|ep           = {minEp}
|crit rate    = {minCritRate}
|crit damage  = {minCritDmg}
}}}}
====Max====
{{{{Kioku Stats
|hp           = {maxHp}
|atk          = {maxAtk}
|def          = {maxDef}
|spd          = {maxSpd}
|ep           = 
|crit rate    = 
|crit damage  = 
}}}}

===Skills===
{{{{Kioku Skills
|skill_name_en               = {skill_name_en}
|skill_name_jp               = {skill_name_jp}
|skill_effect                = {skill_effect}
|skill_image                 = {skill_image}
|skill_progression           = {skill_progression}
|normal_attack_effect        = {normal_attack_effect}
|normal_attack_image         = {normal_attack_image}
|normal_attack_progression   = {normal_attack_progression}
|special_attack_name_en      = {special_attack_name_en}
|special_attack_name_jp      = {special_attack_name_jp}
|special_attack_effect       = {special_attack_effect}
|special_attack_image        = {special_attack_image}
|special_attack_progression  = {special_attack_progression}
|support_name_en             = {support_name_en}
|support_name_jp             = {support_name_jp}
|support_effect              = {support_effect}
|support_image               = {support_image}
|support_progression         = {support_progression}
|extra_support_name_en       = {extra_support_name_en}
|extra_support_name_jp       = {extra_support_name_jp}
|extra_support_effect        = {extra_support_effect}
|extra_support_image         = {extra_support_image}
|extra_support_progression   = {extra_support_progression}
}}}}

===Ascensions===
{{{{Kioku Ascensions
|ascension_1_effect_1 = {ascension_1_effect_1}
|ascension_1_effect_2 = {ascension_1_effect_2}
|ascension_2_effect_1 = {ascension_2_effect_1}
|ascension_2_effect_2 = {ascension_2_effect_2}
|ascension_3_effect_1 = {ascension_3_effect_1}
|ascension_3_effect_2 = {ascension_3_effect_2}
|ascension_4_effect_1 = {ascension_4_effect_1}
|ascension_4_effect_2 = {ascension_4_effect_2}
|ascension_5_effect_1 = {ascension_5_effect_1}
|ascension_5_effect_2 = {ascension_5_effect_2}
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


def read_skill_progression(skills, skill_id):
    values = []
    for i in range(1, 11):
        skill = skills["en"][int(f"{skill_id}{i:02}")]
        value = re.findall(r"(\d+)", skill["description"])
        values.append(value)

    return list(zip(*values))


def read_skill(skills, lang, skill_id, image_path="balloonText"):
    if skill_id == 0:  # For 3* Kioku without ultimates
        return {
            "name": "",
            "description": "",
            "image": "",
            "progression": [],
        }
    skill = skills[lang][int(f"{skill_id}01")]
    return {
        "name": skill["name"],
        "description": skill["description"],
        "image": skill[image_path],
        "progression": read_skill_progression(skills, skill_id),
    }


def create_kioku_pages():
    kiokus = helpers.get_both("getStyleMstList", "styleMstId")
    characters = helpers.get_both("getCharacterMstList", "characterMstId")
    skills = helpers.get_both("getSkillMstList", "skillMstId")
    passives = helpers.get_both("getPassiveSkillMstList", "passiveSkillMstId")
    ascensions = helpers.get_files(
        helpers.SOURCE_EN, "getStyleLimitBreakMstList", "styleLimitBreakMstId"
    )
    ascension_effects = helpers.get_files(
        helpers.SOURCE_EN,
        "getStyleLimitBreakEffectMstList",
        "styleLimitBreakEffectMstId",
    )
    with open("wiki/max_stats.json", "r", encoding="utf-8") as f:
        max_stats = json.load(f)

    for kioku_en in kiokus["en"].values():
        if not kioku_en["isCollectionDisp"]:
            # These are tutorial etc characters, only want to make pages for actual collectable characters
            continue
        characterId = int(str(kioku_en["styleMstId"])[:4])
        kioku_jp = kiokus["jp"][kioku_en["styleMstId"]]
        char_max_stats = max_stats.get(kioku_en["name"], ["", "", "", ""])

        normal_attack_en = read_skill(skills, "en", kioku_en["normalAttack"])

        skill_en = read_skill(skills, "en", kioku_en["skill1"])
        skill_jp_name = skills["jp"][int(f"{kioku_en["skill1"]}01")]["name"]

        special_attack_en = read_skill(skills, "en", kioku_en["specialAttackMstId"])
        special_attack_jp_name = (
            skills["jp"][int(f"{kioku_en["specialAttackMstId"]}01")]["name"]
            if kioku_en["specialAttackMstId"] != 0
            else ""
        )

        support_en = read_skill(
            passives, "en", kioku_en["passiveSkill1"], image_path="skillButtonIcon"
        )
        support_jp_name = passives["jp"][int(f"{kioku_en["passiveSkill1"]}01")]["name"]

        extra_support_en = read_skill(
            passives, "en", kioku_en["subPassiveSkill"], image_path="skillButtonIcon"
        )
        extra_support_jp_name = passives["jp"][int(f"{kioku_en["subPassiveSkill"]}01")][
            "name"
        ]

        ascension_strings = {}

        def find_effect(effect_id):
            effect = ascension_effects[effect_id]
            if effect["name"] != "":
                return effect["name"]
            return passives["en"][effect["value1"]]["description"]

        for i in range(1, 6):
            ascension_keysheet = ascensions[int(f"{kioku_en["styleMstId"]}{i:02}")]
            ascension_strings[f"ascension_{i}_effect_1"] = find_effect(
                ascension_keysheet["styleLimitBreakEffectMstId1"]
            )
            ascension_strings[f"ascension_{i}_effect_2"] = find_effect(
                ascension_keysheet["styleLimitBreakEffectMstId2"]
            )

        kioku_en["PLACEHOLDER"] = "PLACEHOLDER"
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
                    maxHp=char_max_stats[0],
                    maxAtk=char_max_stats[1],
                    maxDef=char_max_stats[2],
                    maxSpd=char_max_stats[3],
                    skill_name_en=skill_en["name"],
                    skill_name_jp=skill_jp_name,
                    skill_effect=skill_en["description"],
                    skill_image=skill_en["image"],
                    skill_progression=skill_en["progression"],
                    normal_attack_effect=normal_attack_en["description"],
                    normal_attack_image=normal_attack_en["image"],
                    normal_attack_progression=normal_attack_en["progression"],
                    special_attack_name_en=special_attack_en["name"],
                    special_attack_name_jp=special_attack_jp_name,
                    special_attack_effect=special_attack_en["description"],
                    special_attack_image=special_attack_en["image"],
                    special_attack_progression=special_attack_en["progression"],
                    support_name_en=support_en["name"],
                    support_name_jp=support_jp_name,
                    support_effect=support_en["description"],
                    support_image=support_en["image"],
                    support_progression=support_en["progression"],
                    extra_support_name_en=extra_support_en["name"],
                    extra_support_name_jp=extra_support_jp_name,
                    extra_support_effect=extra_support_en["description"],
                    extra_support_image=extra_support_en["image"],
                    extra_support_progression=extra_support_en["progression"],
                    **ascension_strings,
                ),
                file=g,
            )


if __name__ == "__main__":
    create_kioku_pages()

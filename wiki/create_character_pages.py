import helpers

text = """{{{{Character Infobox
|id                   = {id}
|image                = {id}_original.png
|name_en              = {name_en}
|name_jp              = {name_jp}
|voice_actor_en       = {voice_actor_en}
|voice_actor_jp       = {voice_actor_jp}
|voice_link           = 
|team1_en             = {team1_en}
|team1_jp             = {team1_jp}
|team2_en             = {team2_en}
|team2_jp             = {team2_jp}
|color                = {color}
|description_en       = {description_en}
|description_jp       = {description_jp}
|school_en            = {school_en}
|school_jp            = {school_jp}
|group                = {series}
|region               = {region}
}}}}
'''{name_en}''' is a [[character]] in ''[[Magia Exedra]]''.
"""

series_map = {
    1: "Puella Magi Madoka Magica",
    2: "Puella Magi Madoka Magica Side Story Magia Record",
    3: "Puella Magi Oriko Magica",
}
region_map = {}


def create_character_pages():
    teams = helpers.get_both("getCharacterTeamMstList.json", "characterTeamMstId")
    profiles = helpers.get_both("getCharacterProfileMstList.json", "characterMstId")
    characters = helpers.get_both("getCharacterMstList.json", "characterMstId")

    for character_en in characters["en"].values():
        profile_en = profiles["en"][character_en["characterMstId"]]
        profile_jp = profiles["jp"][character_en["characterMstId"]]
        character_jp = characters["jp"][character_en["characterMstId"]]
        with open(
            f"wiki/character_pages/{character_en["name"]}.txt",
            "w",
            encoding="utf-8",
        ) as g:
            print(
                text.format(
                    id=character_en["characterMstId"],
                    name_en=character_en["name"],
                    name_jp=character_jp["name"],
                    color=character_en["colorCode"],
                    description_en=profile_en["description"],
                    description_jp=profile_jp["description"],
                    voice_actor_en=profile_en["characterVoice"],
                    voice_actor_jp=profile_jp["characterVoice"],
                    school_en=profile_en["schoolName"],
                    school_jp=profile_jp["schoolName"],
                    series=series_map.get(profile_en["seriesId"], ""),
                    region=region_map.get(profile_en["seriesId"], {}).get(
                        profile_en["regionId"],
                        f"PLACEHOLDER FOR REGION-{profile_en["regionId"]}",  # TODO
                    ),
                    team1_en=teams["en"].get(profile_en["teamId1"], {}).get("name", ""),
                    team1_jp=teams["jp"].get(profile_jp["teamId1"], {}).get("name", ""),
                    team2_en=teams["en"].get(profile_en["teamId2"], {}).get("name", ""),
                    team2_jp=teams["jp"].get(profile_jp["teamId2"], {}).get("name", ""),
                ),
                file=g,
            )


if __name__ == "__main__":
    create_character_pages()

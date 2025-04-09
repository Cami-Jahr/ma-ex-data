import helpers

text = """{{{{Character Infobox
|id                   = {id}
|image                = {id}0101_original.png
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
|story_name_en        = {story_name_en}
|story_name_jp        = {story_name_jp}
|school_en            = {school_en}
|school_jp            = {school_jp}
|group                = {series}
|region               = 
|release_date         = {release_date}
}}}}
'''{name_en}''' is a [[character]] in ''[[Magia Exedra]]''.

==Kiokus==
	
{{{{Kiokus Table|{name_en} Kiokus|hide_character=1}}}}

==Gallery==
	
===Videos===
	
{{Videos Gallery|{name_en} Videos}}
"""

series_map = {
    1: "Puella Magi Madoka Magica",
    2: "Puella Magi Madoka Magica Side Story Magia Record",
    3: "Puella Magi Oriko Magica",
}
region_map = {}


def create_character_pages():
    teams = helpers.get_both("getCharacterTeamMstList", "characterTeamMstId")
    profiles = helpers.get_both("getCharacterProfileMstList", "characterMstId")
    characters = helpers.get_both("getCharacterMstList", "characterMstId")
    stories = helpers.get_both("getAdvMstList", "advMstId")
    story_titles = helpers.get_both("getAdvTitleMstList", "advTitleMstId")
    kiokus = helpers.get_files(helpers.SOURCE_EN, "getStyleMstList", "styleMstId")

    for char_id, character_en in characters["en"].items():
        profile_en = profiles["en"][char_id]
        profile_jp = profiles["jp"][char_id]
        character_jp = characters["jp"][char_id]
        release_dates = [
            v["releaseTime"] for k, v in kiokus.items() if k // 10000 == char_id
        ]

        if char_id == 1000:  # Namae
            story_title_id = None
        else:
            story_title_id = stories["en"][int(f"30{char_id}00")]["advTitleMstId"]
        with open(
            f"wiki/character_pages/{character_en["name"]}.wt",
            "w",
            encoding="utf-8",
        ) as g:
            print(
                text.format(
                    id=char_id,
                    release_date=(
                        helpers.fix_date(min(release_dates))
                        if len(release_dates)
                        else ""
                    ),
                    name_en=character_en["name"],
                    name_jp=character_jp["name"],
                    color=character_en["colorCode"][1:],  # Remove the hash
                    description_en=profile_en["description"],
                    description_jp=profile_jp["description"],
                    voice_actor_en=profile_en["characterVoice"],
                    voice_actor_jp=profile_jp["characterVoice"],
                    school_en=profile_en["schoolName"],
                    school_jp=profile_jp["schoolName"],
                    series=series_map.get(profile_en["seriesId"], ""),
                    # region=region_map.get(profile_en["seriesId"], {}).get(
                    #    profile_en["regionId"],
                    #    f"PLACEHOLDER FOR REGION-{profile_en["regionId"]}",  # TODO Figure out names for these
                    # ),
                    team1_en=teams["en"].get(profile_en["teamId1"], {}).get("name", ""),
                    team1_jp=teams["jp"].get(profile_jp["teamId1"], {}).get("name", ""),
                    team2_en=teams["en"].get(profile_en["teamId2"], {}).get("name", ""),
                    team2_jp=teams["jp"].get(profile_jp["teamId2"], {}).get("name", ""),
                    story_name_en=story_titles["en"]
                    .get(story_title_id, {})
                    .get("title", ""),
                    story_name_jp=story_titles["jp"]
                    .get(story_title_id, {})
                    .get("title", ""),
                ),
                file=g,
            )


if __name__ == "__main__":
    create_character_pages()

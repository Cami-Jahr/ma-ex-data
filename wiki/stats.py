import helpers
from collections import defaultdict


# Trying to figure out how the fuck they calculate max hp and atk

effects = helpers.get_files(
    helpers.SOURCE_EN, "getStyleParamUpEffectMstList", "styleParamUpEffectMstId"
)


heart_vals = defaultdict(int)
heart_effects = helpers.get_files(
    helpers.SOURCE_EN,
    "getCharacterHeartParamUpGroupMstList",
    "characterHeartParamUpGroupMstId",
)

for heart_effect in heart_effects.values():
    lvlup = effects[heart_effect["styleParamUpEffectMstId"]]
    heart_vals[lvlup["abilityEffectType"]] += lvlup["value1"]
print("heart:", heart_vals)


style_vals = defaultdict(int)
style_effects = helpers.get_files(
    helpers.SOURCE_EN, "getStyleParamUpMstList", "styleParamUpMstId"
)
for style_effect in style_effects.values():
    lvlup = effects[style_effect["styleParamUpEffectMstId"]]
    if style_effect["styleMstId"] == 10110101 and style_effect["priority"] <= 198:
        style_vals[lvlup["abilityEffectType"]] += lvlup["value1"] * 0.9
        print(
            style_effect["priority"], lvlup["abilityEffectType"], lvlup["value1"] * 0.9
        )
print("magic:", style_vals)


print((2430 + 4601) * 1.0)
print((131 + 9_00))  # + 2432) * 1.0)
print((8_7 + 9_00))  # + 1544) * 1.0)

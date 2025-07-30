import json



with open("TFT_KO.json", "r") as f:
    unit_data = json.load(f)


def compute_trait_counts(unit_data):
    trait_counts = defaultdict(int)
    for unit_info in unit_data.values():
        for trait in unit_info["traits"]:

            trait = trait.strip()
            trait_counts[trait] += 1
    return dict(trait_counts)


trait_counts = compute_trait_counts(unit_data)


for trait, count in sorted(trait_counts.items(), key=lambda x: -x[1]):
    print(f"{trait}: {count}")


from collections import defaultdict, Counter

#trait thresholds are not correct
trait_thresholds = {
    "Duelist": 2,
    "Juggernaut": 2,
    "Sorcerer": 2,
    "Bastion": 2,
    "Star Guardian": 2,
    "Edgelord": 2,
    "Sniper": 2,
    "Executioner": 2,
    "Soul Fighter": 2,
    "Wraith": 2,
    "Protector": 2,
    "The Crew": 2,
    "Crystal Gambit": 2,
    "Prodigy": 2,
    "Mighty Mech": 2,
    "Luchador": 2,
    "Battle Academia": 2,
    "Mentor": 2,
    "Stance Master": 1,
    "Heavyweight": 2,
    "Supreme Cells": 2,
    "Rosemother": 1,
    "Rogue Captain": 1,
    "Monster Trainer": 2,
    "Luxador": 1,
    "Strategist": 2,
    "The Champ": 1,
    "Crystal Guardian": 1

}

def greedy_trait_maximization(initial_units, unit_data, n, excluded_traits=None):
    if excluded_traits is None:
        excluded_traits = set()

    selected_units = set(initial_units)
    remaining_units = set(unit_data.keys()) - selected_units

    def get_trait_counts(units):
        counts = Counter()
        for u in units:
            for t in unit_data[u]["traits"]:
                t = t.strip()
                counts[t] += 1
        return counts

    def num_active_traits(trait_counts):
        return sum(
            1 for t, c in trait_counts.items()
            if t not in excluded_traits and c >= trait_thresholds.get(t, float('inf'))
        )


    trait_counts = get_trait_counts(selected_units)

    while len(selected_units) < n:
        best_unit = None
        best_gain = -1
        best_trait_counts = None

        for u in remaining_units:
            new_trait_counts = trait_counts.copy()
            for t in unit_data[u]["traits"]:
                new_trait_counts[t.strip()] += 1

            gain = num_active_traits(new_trait_counts) - num_active_traits(trait_counts)
            if gain > best_gain:
                best_gain = gain
                best_unit = u
                best_trait_counts = new_trait_counts

        if best_unit is None:
            break

        selected_units.add(best_unit)
        remaining_units.remove(best_unit)
        trait_counts = best_trait_counts

    return selected_units, trait_counts


initial_units = {}
n = 8

excluded = {"The Champ", "Stance Master", "Rogue Captain", "Rosemother"}

selected, final_trait_counts = greedy_trait_maximization(initial_units, unit_data, n, excluded_traits=excluded)

print("Selected units:")
for u in selected:
    print(f"  {u}: {unit_data[u]['traits']}")

print("\nActivated traits (excluding unique ):")
for trait, count in final_trait_counts.items():
    if trait not in excluded and count >= trait_thresholds.get(trait, float('inf')):
        print(f"  {trait}: {count}")

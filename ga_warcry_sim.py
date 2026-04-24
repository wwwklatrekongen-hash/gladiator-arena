"""
Simplified Gladiator Arena combat sim — same core damage as the HTML game
(calcDmg: dodge from defender AGI, floor(str*multi - def/2) + uniform -2..3).

NOT a full run (no shop, bosses, thrust, defend, etc.). Use as a directional
estimate of how War Cry + Resonance shift win rate in a fixed fair fight.
"""
from __future__ import annotations

import random
from dataclasses import dataclass


def ri(rng: random.Random, a: int, b: int) -> int:
    return rng.randint(a, b)


def calc_dmg(
    rng: random.Random,
    att_str: float,
    def_agi: float,
    def_def: float,
    multi: float = 1.0,
    bonus_dodge: float = 0.0,
) -> int:
    if rng.random() < def_agi * 0.028 + bonus_dodge:
        return -1
    return max(1, int(att_str * multi - def_def * 0.5) + ri(rng, -2, 3))


@dataclass
class Enemy:
    hp: int
    max_hp: int
    str: int
    agi: int
    def_: int


@dataclass
class Player:
    hp: int
    max_hp: int
    str: int
    agi: int
    def_: int
    buff_turns: int = 0
    warcry_cd: int = 0
    resonance: int = 0


def apply_resonance(rng: random.Random, d: int, stacks: int) -> int:
    if d <= 0:
        return d
    s = min(stacks, 5)
    if s <= 0:
        return d
    return max(1, int(d * (1 + s * 0.06)))


def enemy_attack_multi(rng: random.Random) -> float:
    if rng.random() > 0.62:
        return 1.65
    return 1.0


def sim_fight(
    rng: random.Random,
    p: Player,
    e: Enemy,
    warcry_policy: str,
    max_turns: int = 400,
) -> bool:
    """Return True if player wins.

    warcry_policy:
      'none' — slash every player turn
      'greedy' — War Cry whenever CD is 0 (wastes full turns; unrealistic)
      'timed' — slash first turn; later cry on CD only if enemy HP > 22% max
      'refresh' — cry only when CD=0 AND buff expired AND enemy HP > 25% max
                  (no cry while +5 STR still active — closer to good play)
    """
    p = Player(p.hp, p.max_hp, p.str, p.agi, p.def_)
    e = Enemy(e.hp, e.max_hp, e.str, e.agi, e.def_)
    first_player_turn = True
    for _ in range(max_turns):
        if p.hp <= 0:
            return False
        if e.hp <= 0:
            return True

        # --- Player turn ---
        bon = 5 if p.buff_turns > 0 else 0
        do_cry = False
        if warcry_policy == "greedy" and p.warcry_cd == 0:
            do_cry = True
        elif warcry_policy == "timed" and p.warcry_cd == 0 and not first_player_turn:
            if e.hp > 0.22 * e.max_hp:
                do_cry = True
        elif warcry_policy == "refresh" and p.warcry_cd == 0 and p.buff_turns == 0:
            if e.hp > 0.25 * e.max_hp:
                do_cry = True
        if do_cry:
            p.buff_turns = 2
            p.warcry_cd = 4
            p.resonance = min(p.resonance + 1, 5)
        else:
            d = calc_dmg(rng, p.str + bon, e.agi, e.def_, 1.0, 0.0)
            if d > 0:
                d = apply_resonance(rng, d, p.resonance)
                e.hp -= d

        if p.buff_turns > 0:
            p.buff_turns -= 1
        if p.warcry_cd > 0:
            p.warcry_cd -= 1

        if e.hp <= 0:
            return True

        first_player_turn = False

        # --- Enemy turn ---
        mult = enemy_attack_multi(rng)
        d = calc_dmg(rng, e.str, p.agi, p.def_, mult, 0.0)
        if d > 0:
            p.hp -= d

    return e.hp <= 0


def main() -> None:
    # Rough mid-early stats: base + bronze + leather (similar to round 3)
    p0 = Player(hp=72, max_hp=72, str=14, agi=5, def_=6)
    # Legionnaire (round 3)
    e0 = Enemy(hp=68, max_hp=68, str=12, agi=6, def_=6)

    N = 50_000
    cases = [
        ("Never War Cry (slash only)", "none"),
        ("War Cry greedy (cry whenever CD=0)", "greedy"),
        ("War Cry timed (slash T1; cry on CD if enemy >22% HP)", "timed"),
        ("War Cry refresh (cry when buff down, enemy >25% HP)", "refresh"),
    ]
    for label, pol in cases:
        wins = sum(sim_fight(random.Random(i * 7919 + hash(pol) % 997), p0, e0, pol) for i in range(N))
        print(f"{label}: {wins / N:.1%} win ({wins}/{N}) vs Legionnaire")

    # Harder: Champion-like stats vs player who cleared a few rounds
    p1 = Player(hp=100, max_hp=100, str=22, agi=6, def_=12)
    e1 = Enemy(hp=118, max_hp=118, str=20, agi=10, def_=12)
    print()
    for label, pol in cases:
        wins = sum(sim_fight(random.Random(i * 4243 + hash(pol) % 997), p1, e1, pol) for i in range(N))
        print(f"{label}: {wins / N:.1%} win ({wins}/{N}) vs Champion-tier")


if __name__ == "__main__":
    main()

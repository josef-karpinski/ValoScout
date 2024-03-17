This file contains information about the Riot API for retrieving match information. In our program, we must convert the Tracker Network API into this Riot API for much simpler use.

The Riot API can also be found here:

https://developer.riotgames.com/apis#val-match-v1/GET_getMatch

# Get match by id

## Return value: [MatchDto](#matchdto)

### [MatchDto](#matchdto)
| NAME            | DATA TYPE    | DESCRIPTION                                                         |
|-----------------|--------------|---------------------------------------------------------------------|
| matchInfo       | [MatchInfoDto](#matchinfodto) |                                                                     |
| players         | List[[PlayerDto](#playerdto)] |                                                                     |
| coaches         | List[[CoachDto](#coachdto)] |                                                                     |
| teams           | List[[TeamDto](#teamdto)] |                                                                     |
| roundResults    | List[[RoundResultDto](#roundresultdto)] |                                                                     |

### [MatchInfoDto](#matchinfodto)
| NAME                 | DATA TYPE    | DESCRIPTION                                                         |
|----------------------|--------------|---------------------------------------------------------------------|
| matchId              | string       |                                                                     |
| mapId                | string       |                                                                     |
| gameLengthMillis     | int          |                                                                     |
| gameStart      | str          |                                                                     |
| provisioningFlowId  | string       |                                                                     |
| isCompleted          | boolean      |                                                                     |
| customGameName       | string       |                                                                     |
| queueId              | string       |                                                                     |
| gameMode             | string       |                                                                     |
| isRanked             | boolean      |                                                                     |
| seasonId             | string       |                                                                     |

### [PlayerDto](#playerdto)
| NAME            | DATA TYPE    | DESCRIPTION                                                         |
|-----------------|--------------|---------------------------------------------------------------------|
| riotId           | string       |                                                                     |
| gameName        | string       |                                                                     |
| tagLine         | string       |                                                                     |
| teamId          | string       |                                                                     |
| partyId         | string       |                                                                     |
| characterId     | string       |                                                                     |
| stats           | [PlayerStatsDto](#playerstatsdto) |                                                                     |
| competitiveTier | int          |                                                                     |
| playerCard      | string       |                                                                     |
| playerTitle     | string       |                                                                     |

### [PlayerStatsDto](#playerstatsdto)
| NAME           | DATA TYPE    | DESCRIPTION                                                         |
|----------------|--------------|---------------------------------------------------------------------|
| score          | int          |                                                                     |
| roundsPlayed   | int          |                                                                     |
| kills          | int          |                                                                     |
| deaths         | int          |                                                                     |
| assists        | int          |                                                                     |
| playtimeMillis | int          |                                                                     |
| abilityCasts   | [AbilityCastsDto](#abilitycastsdto) |                                                                     |

### [AbilityCastsDto](#abilitycastsdto)
| NAME           | DATA TYPE    | DESCRIPTION                                                         |
|----------------|--------------|---------------------------------------------------------------------|
| grenadeCasts   | int          |                                                                     |
| ability1Casts  | int          |                                                                     |
| ability2Casts  | int          |                                                                     |
| ultimateCasts  | int          |                                                                     |

### [CoachDto](#coachdto)
| NAME           | DATA TYPE    | DESCRIPTION                                                         |
|----------------|--------------|---------------------------------------------------------------------|
| riotId          | string       |                                                                     |
| teamId         | string       |                                                                     |

### [TeamDto](#teamdto)
| NAME           | DATA TYPE    | DESCRIPTION                                                         |
|----------------|--------------|---------------------------------------------------------------------|
| teamId         | string       | This is an arbitrary string. Red and Blue in bomb modes. The puuid of the player in deathmatch. |
| won            | boolean      |                                                                     |
| roundsPlayed   | int          |                                                                     |
| roundsWon      | int          |                                                                     |
| numPoints      | int          | Team points scored. Number of kills in deathmatch.                  |

### [RoundResultDto](#roundresultdto)
| NAME                   | DATA TYPE    | DESCRIPTION                                                         |
|------------------------|--------------|---------------------------------------------------------------------|
| roundNum               | int          |                                                                     |
| roundResult            | string       |                                                                     |
| roundCeremony          | string       |                                                                     |
| winningTeam            | string       |                                                                     |
| bombPlanter            | string       | Riot ID of player                                                     |
| bombDefuser            | string       | Riot ID of player                                                     |
| plantRoundTime         | int          |                                                                     |
| plantPlayerLocations   | List[[PlayerLocationsDto](#playerlocationsdto)] |                                                                     |
| plantLocation          | [LocationDto](#locationdto)  |                                                                     |
| plantSite              | string       |                                                                     |
| defuseRoundTime        | int          |                                                                     |
| defusePlayerLocations  | List[[PlayerLocationsDto](#playerlocationsdto)] |                                                                     |
| defuseLocation         | [LocationDto](#locationdto)  |                                                                     |
| playerStats            | List[[PlayerRoundStatsDto](#playerroundstatsdto)] |                                                                     |
| roundResultCode        | string       |                                                                     |

### [PlayerLocationsDto](#playerlocationsdto)
| NAME           | DATA TYPE    | DESCRIPTION                                                         |
|----------------|--------------|---------------------------------------------------------------------|
| riotId          | string       |                                                                     |
| viewRadians    | float        |                                                                     |
| location       | [LocationDto](#locationdto)  |                                                                     |

### [LocationDto](#locationdto)
| NAME           | DATA TYPE    | DESCRIPTION                                                         |
|----------------|--------------|---------------------------------------------------------------------|
| x              | int          |                                                                     |
| y              | int          |                                                                     |

### [PlayerRoundStatsDto](#playerroundstatsdto)
| NAME           | DATA TYPE    | DESCRIPTION                                                         |
|----------------|--------------|---------------------------------------------------------------------|
| riotId          | string       |                                                                     |
| kills          | List[[KillDto](#killdto)] |                                                                     |
| damage         | List[[DamageDto](#damagedto)] |                                                                     |
| score          | int          |                                                                     |
| economy        | [EconomyDto](#economydto)   |                                                                     |
| ability        | [AbilityDto](#abilitydto)   |                                                                     |

### [KillDto](#killdto)
| NAME                   | DATA TYPE    | DESCRIPTION                                                         |
|------------------------|--------------|---------------------------------------------------------------------|
| timeSinceGameStartMillis | int       |                                                                     |
| timeSinceRoundStartMillis | int      |                                                                     |
| killer                 | string       | Riot Id                                                               |
| victim                 | string       | Riot Id                                                               |
| victimLocation         | [LocationDto](#locationdto)  |                                                                     |
| assistants              | List[string] | List of Riot Ids                                                      |
| playerLocations        | List[[PlayerLocationsDto](#playerlocationsdto)] |                                                                     |
| finishingDamage        | [FinishingDamageDto](#finishingdamagedto) |                                                                     |

### [FinishingDamageDto](#finishingdamagedto)
| NAME           | DATA TYPE    | DESCRIPTION                                                         |
|----------------|--------------|---------------------------------------------------------------------|
| damageType     | string       |                                                                     |
| damageItem     | string       |                                                                     |
| isSecondaryFireMode | boolean |                                                                     |

### [DamageDto](#damageDto)
| NAME       | DATA TYPE | DESCRIPTION |
|------------|-----------|-------------|
| receiver   | string    | Riot Id       |
| damage     | int       |             |
| legshots   | int       |             |
| bodyshots  | int       |             |
| headshots  | int       |             |

### [EconomyDto](#economyDto)
| NAME          | DATA TYPE | DESCRIPTION |
|---------------|-----------|-------------|
| loadoutValue  | int       |             |
| weapon        | string    |             |
| armor         | string    |             |
| remaining     | int       |             |
| spent         | int       |             |

### [AbilityDto](#abilityDto)
| NAME            | DATA TYPE | DESCRIPTION |
|-----------------|-----------|-------------|
| grenadeEffects  | string    |             |
| ability1Effects | string    |             |
| ability2Effects | string    |             |
| ultimateEffects | string    |             |

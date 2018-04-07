#
# Google CodeJam -  Qualification Round
#
# Copyright (c) 2018
# Authors: Szymon Bialkowski
#
# Version 1.0
#

import math

shoot  = 'S'
charge = 'C'


def leastHacks(shieldStrength, robotsProgram):
    totalDamage      = 0
    currentDamage    = 1
    hacksRequired    = 0
    chargeIndexes    = []
    chargeInfo       = {}
    shotsAfterCharge = 0
    firstCharge      = True
    previousCharge   = 0
    stackLength      = 0

    #   Count up damage
    for index, action in enumerate(robotsProgram):
        if action == charge:
            if firstCharge:
                chargeInfo[index] = {'shotsAfter': shotsAfterCharge, 'damage': currentDamage, 'previousShot': None}
                firstCharge = False
            else:
                chargeInfo[previousCharge]['shotsAfter'] = shotsAfterCharge
                chargeInfo[index] = {'shotsAfter': 0, 'damage': currentDamage, 'previousShot': previousCharge}
                shotsAfterCharge = 0
            previousCharge = index
            chargeIndexes.append(index)
            stackLength += 1
            currentDamage *= 2
        else:
            if not firstCharge:
                shotsAfterCharge += 1
            totalDamage += currentDamage

    #  If charges exist
    if not firstCharge:
        chargeInfo[previousCharge]['shotsAfter'] = shotsAfterCharge

    if totalDamage <= shieldStrength:
        return hacksRequired
    elif stackLength == 0:
        return "IMPOSSIBLE"

    damageDifference = totalDamage - shieldStrength

    for i in range(stackLength):
        if stackLength == 0:
            return "IMPOSSIBLE"

        closestCharge = chargeInfo[chargeIndexes.pop()]
        stackLength -= 1
        requiredShots = closestCharge['shotsAfter'] \
                        if damageDifference > (closestCharge['damage'] * closestCharge['shotsAfter']) \
                        else int(math.ceil(damageDifference / closestCharge['damage']))
        totalDamage -= requiredShots * closestCharge['damage']
        damageDifference -= requiredShots * closestCharge['damage']
        hacksRequired += requiredShots

        if totalDamage <= shieldStrength:
            return hacksRequired

        if closestCharge['previousShot'] is not None:
            chargeInfo[closestCharge['previousShot']]['shotsAfter'] += closestCharge['shotsAfter']
    return "IMPOSSIBLE"


def main():
    T     = int(input())
    cases = []
    for _ in range(T):
        temp = input().strip().split(' ')
        temp[0] = int(temp[0])
        cases.append(temp)

    counter = 1
    for shieldStrength, robotsProgram in cases:
        print('Case #{}: {}'.format(counter, leastHacks(shieldStrength, robotsProgram)))
        counter += 1


if __name__ == "__main__":
    main()

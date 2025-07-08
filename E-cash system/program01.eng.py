# -*- coding: utf-8 -*-
'''
An e-cash system allows the registered users to transfer electronic currency
    units between one another. We shall use the following symbol to denote
    the currency unit: Ħ.
    To transfer Ħ’s, the players resort to intermediary agents who manage the
    transactions at the price of a transaction fee. The transaction fees
    are based on varying percentages decided by the intermediary agents.

The aim of this program is to process a log of transactions between the
    players of the e-cash system and compute:
    1) a list with the final balance of every account of the involved
       player’s accounts;
    2) a list with the final amount earned by every intermediary;
    3) a list in which, for every intermediary, a nested list reports the
       remaining debts of the player’s accounts (0 if no debt was accumulated,
       or a negative integer otherwise).
    Results (1), (2) and (3) should be elements of a tuple.

In particular, the following function should be designed:
    ex1(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log)
    where
    – acn1, acn2 and acn3 are the account numbers of player 1, 2 and 3,
      respectively;
    – imd_acn1 and imd_acn2 are the account numbers of intermediaries 1 and 2,
      respectively;
    – init_amount is the initial amount in the accounts of the three players
      (we assume that all players start with the same starting amount);
    – the accounts of intermediaries start with a balance of 0Ħ;
    – transact_log is a list of transactions; every transaction is a tuple,
      which consists of the following elements:
      · a pair of integers indicating the account number of the sender and
        the account number of the receiver;
      · the transferred amount;
      · the account number of the intermediary;
      · the percentage of the transaction fee (to be computed based on the
        transferred amount).

For example, the following tuple:
      ((0x44AE, 0x5B23), 800, 0x1612, 4)
    indicates a transaction transferring 800Ħ from the account number
    0x44AE to the account number 0x5B23, with the help of the intermediary
    who will receive 4% of 800Ħ (thus, 32Ħ) on their account at 0x1612.
    As a result,
    - the balance of the sender (0x44AE) will decrease by
        800 + 32 = 832Ħ,
    - the balance of the recipient (0x5B23) will increase by
        800Ħ,
    - and the intermediary will earn and deposit on their account (0x1612)
        32Ħ.

Notice that if the funds in the sender’s account are insufficient,
    the transaction is declared invalid by the intermediary. The intermediary
    will get the fee anyway from the sender, if there are enough Ħ’s in the
    sender’s account. If the sender’s account cannot pay the transaction fee,
    the intermediary will get all the remaining funds and take its part
    from the next transactions to the sender until the debt is paid.
    In the example above, if there were only 700Ħ in account 0x44AE,
    the intermediary would earn 32Ħ and the amount in 0x44AE would decrease
    to 668Ħ. If there were only 10Ħ in account 0x44AE, the intermediary would
    earn 10Ħ and the amount in 0x44AE would decrease to 0Ħ; also, the
    intermediary would hold a credit of 22Ħ from the sender. The sender would be
    obliged to repay the 22Ħ getting the due amount from the transactions
    received later until the debt is extinguished.

    If a debt is accumulated towards two intermediary agents, funds go to the
    intermediary having the highest credit first, and the remainder goes to
    the other intermediary, for as much as is left. For instance, let player 1
    owe 300Ħ to intermediary 1 and 200Ħ to intermediary 2; as player 1
    receives 400Ħ, 300Ħ are paid to intermediary 1 and 100Ħ are paid to
    intermediary 2. If the same amount is due to both intermediary agents,
    the payback is evenly split. For instance, let player 2 owe 100Ħ to
    intermediary 1 and 100Ħ to intermediary 2; as player 2 receives 100Ħ,
    50Ħ go to each intermediary.

As an example,
    ex1(0x5B23, 0xC78D, 0x44AE, 0x1612, 0x90FF, 1000,
        [ ((0x44AE, 0x5B23),  800, 0x1612,  4),
          ((0x44AE, 0xC78D),  800, 0x90FF, 10),
          ((0xC78D, 0x5B23),  400, 0x1612,  8),
          ((0x44AE, 0xC78D), 1800, 0x90FF, 12),
          ((0x5B23, 0x44AE),  100, 0x1612,  2)
        ]
    returns
    ( [2098, 568, 0], [66, 268], [ [0, 0, 0], [0, 0, -28] ] )
    because all players start with 1000Ħ in their account and, at the end,
    – the balance of player 1 amounts to 2098Ħ,
    – the balance of player 2 amounts to 568Ħ,
    – the balance of player 3 amounts to 0Ħ,
    – intermediary 1 earned 66Ħ,
    – intermediary 2 earned 268Ħ,
    – player 3 still owes 28Ħ to intermediary 2.

NOTE: the timeout for this exercise is of 2 seconds for each test.

WARNING: Make sure that the uploaded file is UTF8-encoded
    (to that end, we recommend you edit the file with Spyder)

'''


def ex1(acn1, acn2, acn3, imd_acn1, imd_acn2, init_amount, transact_log):
    log = {acn1: [init_amount, 1], acn2: [init_amount, 2], acn3: [init_amount, 3], imd_acn1: [0, 0, 0, 0],
           imd_acn2: [0, 0, 0, 0]}

    for el in transact_log:

        sender, recepient = el[0]
        payment, agent, percent = el[1:]

        if log[sender][0] >= (payment + payment * percent / 100):

            log[sender][0] -= (payment + payment * percent / 100)
            log[recepient][0] += payment
            log[agent][0] += payment * percent / 100
            taxpayer_idx = log[recepient][1]

            a1_debt = log[imd_acn1][taxpayer_idx]
            a2_debt = log[imd_acn2][taxpayer_idx]

            if a1_debt + a2_debt == 0:
                pass
            elif log[recepient][0] + a1_debt + a2_debt >= 0:

                log[recepient][0] += (a1_debt + a2_debt)
                log[imd_acn1][0] += abs(a1_debt)
                log[imd_acn1][taxpayer_idx] = 0
                log[imd_acn2][0] += abs(a2_debt)
                log[imd_acn2][taxpayer_idx] = 0

            elif a1_debt < a2_debt:
                c = log[recepient][0] + a1_debt
                if c >= 0:
                    log[imd_acn1][0] += abs(a1_debt)
                    log[imd_acn1][taxpayer_idx] = 0
                    log[imd_acn2][0] += c
                    log[imd_acn2][taxpayer_idx] += c
                    log[recepient][0] = 0
                else:
                    log[imd_acn1][0] += log[recepient][0]
                    log[imd_acn1][taxpayer_idx] += log[recepient][0]
                    log[recepient][0] = 0

            elif a1_debt > a2_debt:
                c = log[recepient][0] + a2_debt
                if c >= 0:
                    log[imd_acn2][0] += abs(a2_debt)
                    log[imd_acn2][taxpayer_idx] = 0
                    log[imd_acn1][0] += c
                    log[imd_acn1][taxpayer_idx] += c
                    log[recepient][0] = 0

                else:
                    log[imd_acn2][0] += log[recepient][0]
                    log[imd_acn2][taxpayer_idx] += log[recepient][0]
                    log[recepient][0] = 0
            else:
                log[imd_acn1][0] += log[recepient][0] / 2
                log[imd_acn1][taxpayer_idx] += log[recepient][0] / 2
                log[imd_acn2][0] += log[recepient][0] / 2
                log[imd_acn2][taxpayer_idx] += log[recepient][0] / 2
                log[recepient][0] = 0
        else:
            if log[sender][0] >= payment * percent / 100:
                log[sender][0] -= payment * percent / 100
                log[agent][0] += payment * percent / 100

            elif log[sender][0] > 0:
                i = log[sender][1]
                log[agent][0] += log[sender][0]
                log[agent][i] -= (payment * percent / 100 - log[sender][0])
                log[sender][0] = 0
            else:
                idx_sender = log[sender][1]
                log[agent][idx_sender] -= payment * percent / 100

    result = ([log[acn1][0], log[acn2][0], log[acn3][0]], [log[imd_acn1][0], log[imd_acn2][0]],
              [log[imd_acn1][1:], log[imd_acn2][1:]])

    return result

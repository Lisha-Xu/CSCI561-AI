import copy
import time

numOfQuery = 0
numOfSentences = 0
queries = []
startTime = 0


class KB:
    def __init__(self):
        self.predicates = set()
        self.neg = {}
        self.pos = {}
        self.checked = {}
        self.sentences = []

    def add(self, predicate, index):
        if '~' not in predicate[0]:
            if predicate[0] not in self.predicates:
                self.predicates.add(predicate[0])
                self.pos[predicate[0]] = []
            self.pos[predicate[0]].append(index)
        else:
            if predicate[0] not in self.predicates:
                self.predicates.add(predicate[0])
                self.neg[predicate[0]] = []
            self.neg[predicate[0]].append(index)

    def addSentences(self, sentence):
        self.sentences.append(sentence)


def negative(sentence):
    if sentence[0] == '~':
        sentence = sentence[1:]
    else:
        sentence = '~' + sentence
    return sentence


def getPredicate(sentence):
    predicate = []
    action = sentence.split('(')
    if ',' in action[1]:
        variables = action[1].split(')')[0].split(',')
        predicate.append(action[0])
        predicate.extend(variables)
    else:
        variables = action[1].split(')')[0]
        predicate.append(action[0])
        predicate.append(variables)

    return predicate


def isVariable(variable):
    if variable.islower():
        return True


def standard(predicate, index):
    for i in range(1, len(predicate)):
        if isVariable(predicate[i]):
            predicate[i] = predicate[i] + str(index)
    return predicate[0] + '(' + ','.join(predicate[1:]) + ')'


def transfer(sentence, index, knowledgeBase):
    if '=>' in sentence:
        require, conclusion = sentence.split('=>')
        # remove the space
        require = require.strip()
        conclusion = conclusion.strip()
        if '&' in require:
            soloParts = require.split('&')
            for i in range(0, len(soloParts)):
                soloParts[i] = soloParts[i].strip()
                soloParts[i] = negative(soloParts[i])
                predicate = getPredicate(soloParts[i])
                knowledgeBase.add(predicate, index)
                soloParts[i] = standard(predicate, index)
            result = ' | '.join(soloParts)
        else:
            require = negative(require)
            predicate = getPredicate(require)
            knowledgeBase.add(predicate, index)
            result = standard(predicate, index)
        predicate = getPredicate(conclusion)
        knowledgeBase.add(predicate, index)
        conclusion = standard(predicate, index)
        result = result + ' | ' + conclusion
        knowledgeBase.addSentences(result)
    else:
        predicate = getPredicate(sentence)
        knowledgeBase.add(predicate, index)
        sentence = standard(predicate, index)
        knowledgeBase.addSentences(sentence)


def firstResolve(predicates, KB):
    actionNeg = negative(predicates[0])
    if '~' in predicates[0] and actionNeg in KB.pos:
        return KB.pos[actionNeg]
    elif '~' not in predicates[0] and actionNeg in KB.neg:
        return KB.neg[actionNeg]


def unify(KBpre, Querypre):
    matchDict = {}
    KBpredicates = getPredicate(KBpre)
    Querypredicates = getPredicate(Querypre)
    numVKB = len(KBpredicates)
    numVQ = len(Querypredicates)
    if numVKB != numVQ:
        return matchDict
    for i in range(1, numVKB):
        if isVariable(KBpredicates[i]) and isVariable(Querypredicates[i]):
            if (KBpredicates[i] not in matchDict) and (Querypredicates[i] not in matchDict):
                matchDict[KBpredicates[i]] = Querypredicates[i]
        elif isVariable(KBpredicates[i]) and not isVariable(Querypredicates[i]):
            if KBpredicates[i] not in matchDict:
                matchDict[KBpredicates[i]] = Querypredicates[i]
            elif matchDict[KBpredicates[i]] != Querypredicates[i]:
                return {}
        elif (not isVariable(KBpredicates[i])) and isVariable(Querypredicates[i]):
            if Querypredicates[i] not in matchDict:
                matchDict[Querypredicates[i]] = KBpredicates[i]
            elif matchDict[Querypredicates[i]] != KBpredicates[i]:
                return {}
        else:
            if KBpredicates[i] == Querypredicates[i]:
                matchDict[KBpredicates[i]] = Querypredicates[i]
            else:
                return {}
    return matchDict


def getSentence(predicate, possibleValue, dictionary):
    newSentence = ''
    predicate.pop(possibleValue)
    for i in range(0, len(predicate)):
        pre = getPredicate(predicate[i])
        for j in range(1, len(pre)):
            if pre[j] in dictionary:
                pre[j] = dictionary[pre[j]]
        newSentence = newSentence + pre[0] + '(' + ','.join(pre[1:]) + ')' + ' | '
    return newSentence


def resolution(knowledgeBase, query, depth):
    if depth >= 150 or time.time() - startTime > 10:
        return False
    # if depth > 120:
    #     return False
    actionIndex = {}
    queryPart = query.split('|')
    for i in range(0, len(queryPart)):
        queryPart[i] = queryPart[i].strip()
        predicate = getPredicate(queryPart[i])
        tempValue = firstResolve(predicate, knowledgeBase)
        if tempValue:
            actionIndex[predicate[0]] = tempValue
    if actionIndex:
        for action in actionIndex.keys():
            for index in actionIndex[action]:
                findFlag = False
                KBSentence = knowledgeBase.sentences[index]
                negAction = negative(action)
                preKBSentence = KBSentence.split('|')
                preQuery = query.split('|')
                KBpossible = []
                Querypossible = []
                # remove the space
                for i in range(0, len(preKBSentence)):
                    preKBSentence[i] = preKBSentence[i].strip()
                    predicateKB = getPredicate(preKBSentence[i])
                    if predicateKB[0] == negAction:
                        KBpossible.append(i)
                for i in range(0, len(preQuery)):
                    preQuery[i] = preQuery[i].strip()
                    predicateQuery = getPredicate(preQuery[i])
                    if predicateQuery[0] == action:
                        Querypossible.append(i)
                for i in range(0, len(KBpossible)):
                    for j in range(0, len(Querypossible)):
                        matchDict = unify(preKBSentence[KBpossible[i]], preQuery[Querypossible[j]])
                        if matchDict:
                            KBindex = i
                            Qindex = j
                            findFlag = True
                            break
                if not findFlag:
                    resSentence = "NotFind"
                else:
                    tempSentence = getSentence(preKBSentence, KBpossible[KBindex], matchDict)
                    tempSentence += getSentence(preQuery, Querypossible[Qindex], matchDict)
                    if tempSentence == '':
                        return True
                    else:
                        res = []
                        tempSentence = tempSentence[:-3]
                        resPredicate = tempSentence.split('|')
                        for i in range(0, len(resPredicate)):
                            resPredicate[i] = resPredicate[i].strip()
                        resPredicate = set(resPredicate)
                        for element in resPredicate:
                            if negative(element) not in resPredicate:
                                res.append(element)

                        if not res:
                            resSentence = "NotFind"
                        else:
                            resSentence = ' | '.join(sorted(res))
                print(resSentence)
                if resSentence in knowledgeBase.checked and knowledgeBase.checked[resSentence] >= 20:
                    continue
                if resSentence == "NotFind":
                    continue
                result = resolution(knowledgeBase, resSentence, depth + 1)
                if result:
                    return True
                if resSentence not in knowledgeBase.checked:
                    knowledgeBase.checked[resSentence] = 0
                knowledgeBase.checked[resSentence] += 1
    return False


if __name__ == "__main__":
    knowledgeBase = KB()
    inputFile = open("input.txt")
    fileData = inputFile.readlines()
    numOfQuery = int(fileData.pop(0).rstrip())
    for i in range(0, numOfQuery):
        queries.append(fileData.pop(0).rstrip())
    numOfSentences = int(fileData.pop(0).rstrip())
    for i in range(0, numOfSentences):
        sentence = fileData.pop(0).rstrip()
        transfer(sentence, i, knowledgeBase)
    # print(knowledgeBase.sentences)

    output = open("output.txt", "w")
    for i in range(0, numOfQuery):
        copyKB = copy.deepcopy(knowledgeBase)
        queries[i] = negative(queries[i])
        copyKB.addSentences(queries[i])
        predicate = getPredicate(queries[i])
        copyKB.add(predicate, len(copyKB.sentences) - 1)
        startTime = time.time()
        result = resolution(copyKB, queries[i], 0)
        if result:
            print(result)
            if i != numOfQuery - 1:
                output.write("TRUE\n")
            else:
                output.write('TRUE')
        else:
            if i != numOfQuery - 1:
                output.write("FALSE\n")
            else:
                output.write('FALSE')

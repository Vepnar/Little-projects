#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    Author: Arjan de Haan (Vepnar)
#   
#    The bigfive.json is stored in ../Assets/bigfive.json
#    Questions are based on the examples on wikipedia
#    See: https://en.wikipedia.org/wiki/Big_Five_personality_traits
#
#    requirements: colorama
#

import os
import json
import random
from colorama import init, Fore, Style

# Static messages used for displaying infomation

QUESTION_INFO = 'Give a score how much you agree with the \
    following statement'.format(fore=Fore, style=Style)

QUESTION_SCORE = '{style.BRIGHT}Possible answers:{style.RESET_ALL} \
    {fore.GREEN}10{fore.RESET} Agree, {fore.YELLOW}5{fore.RESET} \
    Neutral, {fore.RED}1{fore.RESET} \
    Disagree{style.RESET_ALL}'.format(
    fore=Fore, style=Style)

INPUT_MESSAGE = '{style.BRIGHT}Your answer >> '.format(
    fore=Fore, style=Style)

TRAIT_STRING = '{style.BRIGHT}{name}: \
    {style.RESET_ALL}{score}%\n{style.DIM}{desc}{style.RESET_ALL}'

# Store different trait types
class Trait:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.value = 50

    def update(self,score):
        self.value+=score
        self.value/=2

    def __str__(self):
        return (TRAIT_STRING.format(
            fore=Fore, style=Style, name=self.name,
            desc=self.description,score=int(self.value)
        ))

# Store questions as class with specified information about the questions
class Question:
    def __init__(self, question, trait, reversed_question=False):
        self.question = question
        self.trait = trait
        self.reversed_question = reversed_question

    def ask(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(QUESTION_INFO)
        print(QUESTION_SCORE)
        print(self.question)

        while True:
            answer = input(INPUT_MESSAGE)
            
            if not answer.isdigit()or int(answer) > 10 or 1 > int(answer):
                print('Invalid answer\n')  
                continue

            value = int(answer)*10

            if self.reversed_question:
                value = abs(value - 100)
                
            self.trait.update(value)
            break

# Parse traits from a json file
def parse_traits(json_data):
    data = json_data['traits']

    traits = []

    for trait in data:
        trait_object = Trait(trait['name'],trait['description'])
        traits.append(trait_object)

    return traits

# Parse questions from a json file with a possiblity to randomize the questions
def parse_questions(json_data,traits,randomize=True):
    data = json_data['questions']

    questions = []

    for question in data:
        trait = traits[question['trait']]
        q = Question(question['question'], trait, reversed_question=question['reversed'])
        questions.append(q)

    if randomize:
        random.shuffle(questions)

    return questions

if __name__ == '__main__':
    with open('bigfive.json', 'r+') as f:
        data = json.load(f)
    
    traits = parse_traits(data)
    questions = parse_questions(data,traits)

    for question in questions:
        question.ask()

    os.system('cls' if os.name == 'nt' else 'clear')

    for trait in traits:
        print(trait)    

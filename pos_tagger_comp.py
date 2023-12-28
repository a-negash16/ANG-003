#!/usr/bin/env python
""" 
    Enhanced Tagger Comparision Program

    A comparative analysis by cross-referencing outputs from NLTK, Stanford, and CLAWS taggers

    Author: Abrham Negash Gelan.
    Date:  07 November 2023
"""
################################################################

def parse_sentpos(filename):
    """
    Purpose: Parses the sentpos output from any of the three taggers.

    Input: filename of output file to be parsed

    Returns: A list of sentences, where each sentence is a list of (word, tag) tuples.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Output initialization
    tags_compiled = []

    for line in lines:
        # Only tag containing lines
        if ' B ' not in line:
            continue
        
        # Strip unnecessary items, split word-tag couple with a space,
        tagged_words_str = line.split(' B ')[1].strip()
        word_tags = tagged_words_str.split()

        # Create a tuple of (word,tag)
        tag = [(wt.split('_')[0], wt.split('_')[1]) for wt in word_tags if '_' in wt]
        tags_compiled.append(tag)
    return tags_compiled

 


def compare_taggings(parsed1, parsed2):
    """
    Purpose: Compare two lists of word-tag tuples to find discrepancies accounting for tokenization differences.

    Input:
        parsed1, parsed2: Lists of sentences, where each sentence is a list of (word, tag) tuples.
        
    Returns:
        tag_discrepancy: A dictionary with words as keys and sets of tags as the values.
        tag_match: A dictionary with words as keys and a tag as the value. 
        tokenization_issue: A dictionary with line number as key and a set of tuples that could not be determined
                            due to tokenization discrepancies
    """

    tag_discrepancy = {}
    tag_match = {}
    tokenization_issue = {}

    # dictionary adder helper
    def add_to_dict(dictionary, key, value):
        if key in dictionary:
            dictionary[key].add(value)
        else:
            dictionary[key] = {value}

    for sentence_index, (sentence1, sentence2) in enumerate(zip(parsed1, parsed2)):
        # Iterate through both sentences simultaneously
        for (word1, tag1), (word2, tag2) in zip(sentence1, sentence2):
            if word1.lower() == word2.lower():
                if tag1 != tag2:
                    # Case 1: Words match, tags don't --> tag_discrepancy
                    add_to_dict(tag_discrepancy, word1.lower(), (tag1, tag2))
                else:
                    # Case 2: Words match, tags do as well --> tag_match
                    add_to_dict(tag_match, word1.lower(), tag1)
            else:
                # Case 3: Words don't match --> tokenization_issue
                tokenization_issue[sentence_index] = tokenization_issue.get(sentence_index, []) + [(word1, tag1), (word2, tag2)]

    return tag_discrepancy, tag_match, tokenization_issue
####################################################################################


####################################################################################
#---------------- Step 01: File initialization ----------------#

#Add sentpos output txt files here
claws_filepath = ""
nltk_filepath = "" 
stanford_filepath = ""


#---------------- Parsing ----------------#

parsed_claws = parse_sentpos(claws_filepath)
parsed_nltk = parse_sentpos(nltk_filepath)
parsed_stanford = parse_sentpos(stanford_filepath)

#print(parsed_claws)
#print(parsed_nltk)
#print(parsed_stanford)

#---------------- Discrepancies ----------------#

#tag_discrepancies, tokenization_issues = compare_taggings(parsed_nltk, parsed_stanford)
#print(tag_discrepancies)
#print("------------------------------------------------")
#print(tokenization_issues)
##############################################################


##############################################################
def main():                                                     
    tag_discrepancies,tag_match, tokenization_issues = compare_taggings(parsed_claws, parsed_stanford)
    # Personal naming prefrence:tagger1Vtagger2_type.txt'
    with open('clawsVstan_inagural.txt', 'w', encoding='utf-8') as f:
        
        # Tag Discrepancies
        f.write("----------------- Tag Discrepancies ------------------------\n")
        for word, tag_pairs in tag_discrepancies.items():
            f.write(f"Word: {word}, Tags: {tag_pairs}\n")

        #Doc divider
        f.write("---------------------------------------------------\n\n\n")

        # Tag Matches
        f.write("----------------- Tag Matches ------------------------\n")
        for word2, tag_pairs2 in tag_match.items():
            f.write(f"Word: {word2}, Tag: {tag_pairs2}\n")

        #Doc divider
        f.write("---------------------------------------------------\n\n\n")

        # Tokenization issues
        f.write("----------------- Tokenization issues ------------------------\n")
        if len(tokenization_issues)==0:
            f.write("No tokenization issues found with the two taggers")
        else:
            for line_num, issues in tokenization_issues.items():
                f.write(f"Line number: {line_num}, Issues: {issues}\n")

if __name__ == "__main__":
    main()
##############################################################

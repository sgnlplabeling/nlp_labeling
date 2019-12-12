
from config import Config

config = Config()

def build_data():

    train_word_list, train_pumsa_list, train_char_list, train_rel_list = get_vocab(config.train_filename)
    test_word_list, test_pumsa_list, test_char_list, test_rel_list = get_vocab(config.test_filename)

    word_list = list(set(train_word_list + test_word_list))
    pumsa_list = list(set(train_pumsa_list + test_pumsa_list))
    char_list = list(set(train_char_list + test_char_list))
    rel_list = list(set(train_rel_list + test_rel_list))


    write_vocab(word_list, config.words_filename)
    write_vocab(pumsa_list, config.pumsas_filename)
    write_vocab(char_list, config.chars_filename)
    write_vocab(rel_list, config.rels_filename)

def write_vocab(token_list, file_path):
    with open(file_path, "w") as f:
        for token in token_list:
            f.write(token+"\n")



def get_vocab(file_path):
    word_list, pumsa_list, char_list, rel_list = [], [], [], []

    with open(file_path) as f:
        for line in f.readlines():
            line = line.strip()
            if line == "" or line[0] == ";":
                continue
            M, H, REL, _, EOJEOL = line.split()

            rel_list.append(REL)

            morphs = EOJEOL.split("|")
            string = ""
            for morph in morphs:
                m_idx = morph.rfind("/")
                word = morph[:m_idx]
                pumsa = morph[m_idx+1:]
                string += word

                word_list.append(morph)
                pumsa_list.append(pumsa)

            for char in string:
                char_list.append(char)

    word_list = list(set(word_list))
    char_list = list(set(char_list))
    pumsa_list = list(set(pumsa_list))
    rel_list = list(set(rel_list))

    return word_list, pumsa_list, char_list, rel_list




if __name__ == "__main__":
    build_data()
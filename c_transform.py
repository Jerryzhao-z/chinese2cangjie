#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import argparse
import os
import json

isascii = lambda s: len(s) == len(s.encode())
isponctuation = lambda c: (ord(c)>32 and ord(c)<48) or (
    ord(c)>57 and ord(c)<65) or (
        ord(c)>90 and ord(c)<97) or (
            ord(c)>122 and ord(c)<127)

class c_transform():

    def __init__(self):
        self.__ch2cj = None
        self.__cj2ch = None
        self.__ponctuation_ch2en = {ord(f):ord(t) \
                                 for f,t in zip('，。！？【】（）％＃＠＆１２３４５６７８９０；：'\
                                                ,',.!?[]()%#@&1234567890;:')}
        self.__ponctuation_en2ch = {ord(f):ord(t) \
                                 for f,t in zip(',.!?[]()%#@&1234567890;:'\
                                                ,'，。！？【】（）％＃＠＆１２３４５６７８９０；：')}

    def __check_prepare(self, infile, mode, mapfile):

        if not os.path.isfile(infile):
            print ('input file not a readable file')
            return False
        elif self.__ch2cj == None and self.__cj2ch == None:
            self.__cj2ch = dict()
            self.__ch2cj = dict()
            mapfunction = json.load(open(mapfile), encoding="utf8")
            keys = list(mapfunction.keys())
            keys.sort()
            for k in keys:
                v = mapfunction[k]
                if v in self.__cj2ch:
                    index = 0
                    while v+str(index) in self.__cj2ch:
                        index += 1
                    v += str(index)
                    print (v)
                
                self.__ch2cj[k] = v
                self.__cj2ch[v] = k

        return True

    def __get_real_word(self,str):
        ret = ''
        _index = 0
        for char in str:
            if not char.isalpha():
                break
            _index += 1
            ret+=char
        return [ret,str[_index:]]

    def __m_t(self, instr='', mode=0):
        if mode == 0:
            # chinese to cangjie, the cangjie code will be separated with space
            re = ''
            num_of_teshuzifu = 0
            for word in instr:
                try:
                    a = self.__ch2cj[word]
                    if len(re) == 0 or re[-1] == " ":
                        re += a+" "
                    else:
                        re += " "+a+" "
                except:
                    if isascii(word) and not isponctuation(word):
                        re += word
                    else:
                        re += word+" "
            if re[-1] == ' ':
                return re[:-1]
            else:
                return re
        if  mode == 1:
            # cangjie to chinese
            re = ''
            for _word in instr.split(' '):
                if _word=='':
                    re += ' '
                try:
                    re += self.__cj2ch[_word]
                except :
                    re += _word
            return re.translate(self.__ponctuation_en2ch)

    def __m_translate(self, infile, outfile, mode):
        if outfile=='':
            outfile = infile + '.out'
        outfile_ = open(outfile,'w', encoding="utf8")
        with open(infile,'r', encoding="utf8") as infile:
            i = 1
            for line in infile.readlines():
                i+=1
                #line = line.decode('utf-8')
                a = line.translate((self.__ponctuation_ch2en))

                a = self.__m_t(a, mode)
                outfile_.write(a)
                if(i%1000==0):
                    outfile_.flush()
        outfile_.close()
        return outfile

    def chinese2cangjie(self, infile, outfile, mapfile):
        mode = 0
        self.__check_prepare(infile, mode, mapfile)
        return self.__m_translate(infile, outfile, mode)

    def cangjie2chinese(self, infile, outfile, mapfile):
        mode = 1
        self.__check_prepare(infile, mode, mapfile)
        return self.__m_translate(infile, outfile, mode)

#terminal
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='test.txt', help=' input file path')
    parser.add_argument('--output', type=str, default='', help=' output file path')
    parser.add_argument('--map', type=str, default='./char2cangjie.json', help=' chinese character to cangjie code map file')
    parser.add_argument('--mode', type=int, default=0, help='0: from chinese character to cangjie; 1: from cangjie to chinese character')
    args = parser.parse_args()
    assert os.path.isfile(args.input), 'input must be a readable file'
    assert args.mode in [0,1], "mode (0: from chinese character to cangjie; 1: from cangjie to chinese character)"
    c_trans = c_transform()

    if args.mode == 0:
        outfile = c_trans.chinese2cangjie(infile = args.input, outfile = args.output, mapfile = args.map)
    else:
        outfile = c_trans.cangjie2chinese(infile = args.input, outfile = args.output, mapfile = args.map)

    print ('file saved in '+outfile)

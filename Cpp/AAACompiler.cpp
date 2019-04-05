// ./AAACompiler *.cpp newfile.cpp
// Author: Arjan de Haan (Vepnar)
// Todo: Multiline comments parsing, float/double parsing & Multiline string parsing

#include <fstream>
#include <iostream>
#include <sstream>
#include <regex> 
#include <string>

typedef std::string String; 
typedef std::vector<std::string> Lines;


Lines Types = {};
std::vector<int> Defines = {};
String Operators[] = {"::","==","!=","||","+=","-=","&&","<<",">>","++","--","<",">","(",")","{","}","+","-","*","/","&","^","=","!",";",".",","};


Lines SplitString(String SplitAble, char delimeter)
{
    std::stringstream ss(SplitAble);
    String item;
    Lines splittedStrings;
    while (std::getline(ss, item, delimeter))
    {
       splittedStrings.push_back(item);
    }
    return splittedStrings;
}

String ReplaceAll(String str, const String& from, const String& to)
{
    int start_pos = 0;
    while((start_pos = str.find(from, start_pos)) != String::npos)
    {
        str.replace(start_pos, from.length(), to);
        start_pos += to.length();
    }
    return str;
}

String GenerateA(int AmountA)
{
    String AOutput = "";
    for(int AmountOfA=0;AmountOfA<AmountA+1;AmountOfA++)
    {
        AOutput+='a';
    }
    return AOutput;
}

bool isA(String SingleWord)
{
    for(int CharIndex=0; CharIndex<SingleWord.size();CharIndex++){
        if(SingleWord[CharIndex] != 'a')
        {
            return false;
        }
    }
    return true;
}

int GetOrCreateNewType(String TypeString)
{
    for(int TypeIndex=0;TypeIndex<Types.size();TypeIndex++){
        if(Types[TypeIndex] == TypeString)
        {
            return TypeIndex;
        }
    }

    Types.push_back(TypeString);
    return Types.size()-1;

}

void InitCompiler()
{
    int OperatorSize = sizeof(Operators)/sizeof(*Operators);
    for(int OperatorIndex=0;OperatorIndex<OperatorSize;OperatorIndex++)
    {
        GetOrCreateNewType(Operators[OperatorIndex]);
    }
}

String StringDetect(String Line)
{
    int state = 0;
    String StringValue = "";
    Lines replaceItems = {};

    for (int LineIndex=0; LineIndex < Line.size(); LineIndex++)
    {
        if(Line[LineIndex] == '\'' && state == 0)
        {
            state=1;
        }
        else if(Line[LineIndex] == '"' && state == 0)
        {
            state=2;
        }
        else if(Line[LineIndex] == '\'' && Line[LineIndex-1] != '\\' && state == 1)
        {
            String TmpString = '\'' +StringValue+ '\'';
            replaceItems.push_back(TmpString);
            StringValue = "";
            state=0;
        }
        else if(Line[LineIndex] == '"' && Line[LineIndex-1] != '\\' && state == 2)
        {
            String TmpString = '"' + StringValue + '"';
            replaceItems.push_back(TmpString);
            StringValue = "";
            state=0;
        }
        else if(state > 0)
        {
            StringValue += Line[LineIndex];
        }
    } 

    for(int NewType=0;NewType<replaceItems.size();NewType++)
    {
        int AmountA = GetOrCreateNewType(replaceItems[NewType]);
        String As = GenerateA(AmountA);
        Line = ReplaceAll(Line,replaceItems[NewType],As);
    }
    return Line;
}
//TODO Implement digit detection
String DigitDetect(String Line)
{
    return Line;
}

String CommentDetect(String Line)
{
    bool last=false;
    String out = "";
    for(int CharIndex=0;CharIndex<Line.size();CharIndex++)
    {
        char Target = Line[CharIndex];

        if(Target == '/' && last)
        {
            return out.substr(0, out.size()-1);
            break;
        }else if(Target == '/')
        {
            last=true;
            out+=Target;
        }
        else
        {
            last=false;
            out+=Target;
        }
    }
    return Line;
    
}

String OperatorDetect(String Line)
{
    int OperatorSize = sizeof(Operators)/sizeof(*Operators) + Defines.size();
    for(int OperatorIndex=0; OperatorIndex<OperatorSize;OperatorIndex++)
    {
       Line = ReplaceAll(Line,Types[OperatorIndex],' ' + GenerateA(OperatorIndex) + ' ');
    }
    return Line;
}

String WordDetect(String wordLine)
{
    String output = "";
    Lines words = SplitString(wordLine, ' ');
    for(int wordIndex=0; wordIndex<words.size();wordIndex++)
    {
        if(!isA(words[wordIndex]))
        {
            int wordID = GetOrCreateNewType(words[wordIndex]);
            words[wordIndex] = GenerateA(wordID);
        }
        if(words[wordIndex].size() != 0)
        {
        output += words[wordIndex] + " ";
        }
    }

    return output + '\n';
}
String RemoveGarbage(String Line)
{
    String Garbage[] = {"\n","\r","\t","\r\n","    ","   ","  "};
    int GarbageSize = sizeof(Garbage)/sizeof(*Garbage);
    for(int GarbageIndex=0;GarbageIndex<GarbageSize;GarbageIndex++)
        Line = ReplaceAll(Line,Garbage[GarbageIndex]," ");
    return Line;
}
String generateDefine()
{
    String output = "";
    for(int TypeIndex=0; TypeIndex<Types.size();TypeIndex++)
    {
        bool stop = false;
        for(int DefineIndex=0; DefineIndex<Defines.size();DefineIndex++)
        {
            if(Defines[DefineIndex] == TypeIndex)
            {
                stop=true;
                continue;
            }
        }
        if(stop) continue;
        output += "#define " + GenerateA(TypeIndex) + " " + Types[TypeIndex]+ "\n";
    }
    return output+'\n';
}

bool detectDefine(String Line)
{
    return Line.rfind("#define ", 0) == 0;
}
bool detectInclude(String Line)
{
    return Line.rfind("#include ",0) == 0;
}

String ProcessDefine(String Line)
{
    Lines RawDefine = SplitString(Line,' ');
    int Amount = GetOrCreateNewType(RawDefine[1]);
    Defines.push_back(Amount);
    String output = "#define " + GenerateA(Amount) + ' ';
    
    for(int DefineIndex=2;DefineIndex<RawDefine.size();DefineIndex++)
        output+=RawDefine[DefineIndex] + ' ';
    return output;
}

int main(int argc, char* argv[])
{
    if(argc != 3){
        printf("./AAACompiler <input> <output>\n");
        return 1;
    }
    InitCompiler();
    std::ifstream infile(argv[1]);
    std::ofstream outfile(argv[2]);
    String readLine;
    String Coutput = "";
    while (std::getline(infile, readLine))
    {
        if(detectDefine(readLine))
        {
            outfile << ProcessDefine(readLine) << '\n';
            continue;
        }
        else if (detectInclude(readLine))
        {
            outfile << readLine << '\n';
            continue;
        }
        readLine = CommentDetect(readLine);
        readLine = StringDetect(readLine);
        readLine = DigitDetect(readLine);
        readLine = OperatorDetect(readLine);
        readLine = RemoveGarbage(readLine);
        readLine = WordDetect(readLine);
        Coutput += readLine;

    }
    String tmp = generateDefine();
    outfile << tmp;
    outfile << Coutput;
    outfile.close();

    return 0;
}

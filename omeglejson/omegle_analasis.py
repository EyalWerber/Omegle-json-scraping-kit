import os
import json
import re

#it is HIGHLY advised to place this file in the conversation json directory

def flatten(t):
        return [item for sublist in t for item in sublist]

class Conversation(dict):
    def __init__(self, chatlog):
        self.date = chatlog['dt']
        self.messeges = chatlog['cnv']
        self.who_disconnected = chatlog['dis']

        


    def flatten(self,t):
        return [item for sublist in t for item in sublist]

         
    #Reverses hebrew sentences reversed by unicode formatting
    def reverse_hebrew_messege(self,messege):
        if(self.hebrew_checker(messege[:])):    
            return messege[::-1]
        else:
            return messege
    
    #checks if conv is in hebrew
    def hebrew_checker(self,word):
        #the long line below check the words for hebrew letters, which are orderes>1487 in unicode
        return any(map(lambda x: x>1487,[ord(char) for char in word]))
    
    #Turn 'S' back to "Stranger" and 'Y' to "You"
    def noun_fix(self,noun):
        if noun == 'S':
            return 'Stranger'
        else:
            return 'You'
    
    #Returns a string containing the conversation itself
    def message_log(self):
        chat_string = ''
        for messege in self.messeges:
            chat_string+=f"{self.noun_fix(messege['w'])}: {self.reverse_hebrew_messege(messege['m'])}\n"
        return chat_string

    def get_words(self):
        return self.flatten([self.reverse_hebrew_messege(messege['m']).split(' ') for messege in self.messeges])
        
    
    #Returns the string representation of whole Conversation
    def __str__(self):
        return f'''date: {self.date[0]} {self.date[1]} {self.date[2]} {self.date[3]} \n{self.message_log()}{self.noun_fix(self.who_disconnected)} Disconnected'''

    def __len__(self):
        return len(self.messeges)

#Conversation list class        
class ConversationList(list):
    def __init__(self):
        self.conversations=self.get_conv_list(self.get_file_name_list())

    def get_file_name_list(self,):    
        return os.listdir(os.getcwd())
    
    def get_conv_list(self,file_names):
        conv_list =[]

        for name in file_names:
            with open(name,'r',encoding="utf8") as f:
                try:
                    conv_list.append(Conversation(json.load(f))) #appends conversations as Conversation object
                except:
                    f.close() #There is a wierd error, maybe it is the extra data of a js object. closed f for saftey                    
        return conv_list
    
    #Removes none alpha numerics
    def remove_signs(self,words):
        return [re.sub(r'[^\w]', ' ', word) for word in words]
    
    #This method get all of the words of the conversation list
    def get_all_words(self):       
        return self.remove_signs(flatten([conv.get_words() for conv in self.conversations]))
    
    def get_conv_byWord(self,word):
        new_conv_list=[]
        for conv in self.conversations:
            for messege in conv.messeges:            
                if word in messege['m']:                   
                    new_conv_list.append(conv)
                    pass
        return new_conv_list

    def get_conv_byDisconnected(self,dis):
        new_conv_list=[]
        for conv in self.conversations:        
            if dis.upper() == conv.who_disconnected:                   
                new_conv_list.append(conv)
                pass
        return new_conv_list

        



    



# conv_list=get_conv_list(get_file_name_list())




# print(conv_list[-1]['cnv'][0]['m'][::-1]) #First message  reversed to normal
# print(f"conversation length: {len(conv_list[-1]['cnv'])}")

if __name__ == '__main__':

    def get_word_histogram(conv_list):
        onv_list= ConversationList()
        # print(([len(conv) for conv in conv_list.conversations]))
        all_words = conv_list.get_all_words()
        word_histogram = {}
        for word in all_words:
            if word not in word_histogram:
                word_histogram[word]=1
            else:
                word_histogram[word]+=1
        return dict(sorted(word_histogram.items(),key= lambda item: item[1]))



    conv_list= ConversationList()
    # print(([len(conv) for conv in conv_list.conversations]))
    
    word_convs= conv_list.get_conv_byWord('מכות')


    print(word_convs[0])
   
    
    
    # get_all_messeges(conv_list)   
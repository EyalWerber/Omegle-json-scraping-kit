
chrome.runtime.onMessage.addListener(gotMessage);

function gotMessage(messgae,sender,sendRespons){
    //Get messeges of chat in an arrey
    function getMesseges(){
        msgs = document.querySelectorAll('.logitem') //Collect all querys of class logitem(chat prompt and messeges)
        msgTexts =[] //array for contents
        var i=1 //to skip first two messeges(they are very heavy)
        while(!msgs[i].innerText.includes('disconnected.')) 
        {
            i++;    
            msgTexts.push(msgs[i].innerText) // Store all cnversation contents
                // break at conv end
        }
        return msgTexts 
    }

    //Turns 'You' to 'Y' and 'Stranger' to 'S'
    function nameShorter(contentArr){
        i =0
        newLine=[]
        while(!contentArr[i].includes('disconnected.')){   
            wordList = contentArr[i].split(' ') 
            wordList[0]= wordList[0][0] //Make firt word the capital letter
            // contentArr[i]=wordList.join(' ') 
            contentArr[i]={w:wordList.shift(),m:wordList.join(' ')}
            i++;       
        }
        contentArr.pop() // Remove disconnect messege
        return contentArr
    }

    function whoDisconnected(contentArr){
        return contentArr[contentArr.length-1].split(' ')[0][0]
    }


    //Arrage datetime object and chat content in and object
    function getChatObject(){ //returns date+content object for storage
        return {dt:Date().split(' ').slice(1,5), cnv:nameShorter(getMesseges()), dis:whoDisconnected(getMesseges())} //dt = DateTime, cnv  = Conversation, dis = Disonnected by (S/Y)
    }


    //Saving chats as json file!!!!
    function download(content, fileName, contentType) {
        var a = document.createElement("a"); //The function creates  an Anchor tag to be used as a download link
        var file = new Blob([content], {type: contentType}); // A blob is a file-like object of immutable raw data, args are content and type, is this case json.
        a.href = URL.createObjectURL(file);
        a.download = fileName;
        a.click();
    }



    //download function call, formats name with datetime
    download(JSON.stringify(getChatObject()), 'chats'+Date().split(' ').slice(1,5).join('')+'.json', 'json'); //Stringify turns the whole object into a string!!!!
}
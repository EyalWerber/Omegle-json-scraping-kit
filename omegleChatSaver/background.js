console.log('Background is running');
chrome.browserAction.onClicked.addListener(buttonclicked);

function buttonclicked(tab){
    console.log(tab)
    let msg = {
        txt:"hello"
    }
    chrome.tabs.sendMessage(tab.id,msg)
}
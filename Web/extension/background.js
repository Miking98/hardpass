chrome.runtime.onInstalled.addListener(function() {
	console.log("HardPass extension is installed!");
});

function grey_browser_icon() {
	chrome.browserAction.setIcon({
		path : {
			"16": "images/greyicon16.png",
			"32": "images/greyicon32.png",
			"48": "images/greyicon48.png",
			"128": "images/greyicon128.png"
		}
	});
}
function color_browser_icon() {
	chrome.browserAction.setIcon({
		path : {
			"16": "images/icon16.png",
			"32": "images/icon32.png",
			"48": "images/icon48.png",
			"128": "images/icon128.png"
		}
	});
}
chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
    if (msg === "colorIcon") {
    	color_browser_icon();
    }
    else if (msg === "greyIcon") {
        grey_browser_icon();
    }
});
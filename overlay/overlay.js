//--------------------------
// Variables
//--------------------------
var serviceUrl = "ws://127.0.0.1:3337/streamlabs";
var socket = new WebSocket(serviceUrl);
var s = document.styleSheets[1];

function changeStylesheetRule(stylesheet, selector, property, value) {
	selector = selector.toLowerCase();
	property = property.toLowerCase();
	value = value.toLowerCase();

	for(var i = 0; i < stylesheet.cssRules.length; i++) {
		var rule = stylesheet.cssRules[i];
		if(rule.selectorText === selector) {
			rule.style[property] = value;
			return;
		}
	}

	stylesheet.insertRule(selector + " { " + property + ": " + value + "; }", 0);
}

changeStylesheetRule(s, "body", "color", "rebeccapurple");

//--------------------------
// Open Event
//--------------------------
socket.onopen = function () {
    // Format your Auth info
    var auth = {
        author: "mi_thom + mathiasAC",
        website: "https://www.twitch.tv/mi_thom",
        api_key: API_Key, //this is defined by right click insert api key
        events: [
            "EVENT_START_HANGMAN",
            "EVENT_END_HANGMAN",
            "EVENT_GUESSED_WRONG",
            "EVENT_RELOAD_SETTINGS"
        ]
    };
    socket.send(JSON.stringify(auth));
};

//--------------------------
// Error Event
//--------------------------
socket.onerror = function (error) {
    console.log("Error: " + error)
};

//--------------------------
// Message Event
//--------------------------
socket.onmessage = function (message) {
    var data = JSON.parse(message.data);
    switch (data["event"]) {
        case "EVENT_RELOAD_SETTINGS":
            // TODO: reload settings
            break;
    }
};

//--------------------------
// Close Event
//--------------------------
socket.onclose = function () {
    console.log("Connection closed")
};
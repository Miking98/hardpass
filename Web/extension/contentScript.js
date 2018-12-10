let LOGIN_URL = 'https://hardpass.herokuapp.com/login_extension';
let LOGOUT_URL = 'https://hardpass.herokuapp.com/logout_extension';
let MAPPING_URL = 'https://hardpass.herokuapp.com/get_mapping';

function load_keyboard_mapping(token, website) {
	// Load keyboard map for this user for this website
	$.ajax({
		type: "POST",
		url: MAPPING_URL,
		data: {
			website: website,
			token: token
		},
		dataType: "json",
		success: function(r) {
		 	console.log("Mapping request went through");
		 	if (r['error'] == 0) {
		 		// Success!
		 		chrome.storage.local.set({'mapping': r['mapping']}, function() {
					console.log('Mapping saved for '+website);
				});
		 	}
		 	else {
		 		// Error
		 		console.log(r['errorMsg']);
		 	}
		},
		error: function(r) {
		 	console.log("Error with extension login");
		 	console.log(r);
		}
	});
}

function get_website_domain() {
	var url = new URL(document.URL);
	var domain = url.hostname;
	return domain;
}

// Check if HardPass is disabled for this website
// Returns True if disabled, False otherwise
function check_if_disabled_for_site(result) {
	var disabled_websites_obj = result.disabled_websites;
	if (disabled_websites_obj != undefined) {
		if (get_website_domain() in disabled_websites_obj) {
			return true;
		}
	}
	return false;
}


//
// Detect tab focus
function handleVisibilityChange() {
	if (document.hidden) {
		// Ignore if blur event
		return;
	}
    // Adjust browser icon to be active or inactive
	chrome.storage.local.get(['mapping','km_active','disabled_websites'], function(result) {
		if (chrome.runtime.lastError) {
			console.log("Error getting mapping for website");
			return;
		}
		var active = result.km_active;
    	if (active == undefined || active == false) {
			// HardPass is paused
			chrome.runtime.sendMessage('greyIcon', function(r) { });
			return;
		}
		if (check_if_disabled_for_site(result)) {
			// HardPass is disabled for this website
			chrome.runtime.sendMessage('greyIcon', function(r) { });
			return;
		}
		chrome.runtime.sendMessage('colorIcon', function(r) { });
	});
}
document.addEventListener("visibilitychange", handleVisibilityChange, false);

$(document).ready(function() {

	// 
	// Get user token
	chrome.storage.local.get('user_token', function (result) {
		console.log("Get user token");
		if (chrome.runtime.lastError) {
			// User token isn't set yet, so no logged in user
			console.log("Not logged in");
			return;
		}
	    var token = result.user_token;
		if (token == undefined) {
			// No user loggged in
			console.log("Not logged in");
			return;
		}
	    var website = get_website_domain();

	    console.log("Token: "+token);
	    console.log("Website: "+website);
		load_keyboard_mapping(token, website);
	});

	// Bind keyboard mapping event to password field
	var last_val = '';
	$(document).on("keyup", "input[type=password]", function(e) {
		let $elem = $(this);
		// Get mapping from local storage
		chrome.storage.local.get(['mapping','km_active','disabled_websites'], function(result) {
			if (chrome.runtime.lastError) {
				console.log("Error getting mapping for website");
				return;
			}

			var mapping = result.mapping;
			var active = result.km_active;

			if (active == undefined || active == false) {
				// HardPass is paused
				return;
			}
			if (check_if_disabled_for_site(result)) {
				// HardPass is disabled for this website
				return;
			}
			if (mapping == undefined) {
				// Still waiting for AJAX request...
				return;
			}
			let current_val = $elem.val();
			// Make sure keyboard char hit has actually altered contents of this password field
			if (last_val == current_val) {
				// User hit a Command key or the Shift key, hasn't actually entered anything into password field
				// Ignore this
				return;
			}
			// Special keys
			/// Command+A to clear field contents, then typed a char
			if (current_val.length < last_val.length && current_val.length == 1) {
				
			}
			/// Backspace
			else if (current_val.length < last_val.length) {
				// Clear out entire field's contents
				$elem.val('');
				last_val = '';
				return;
			}
			// Get current input
			let char_pressed = $elem.val().slice(-1); // Get last character entered into this input field
			let mapped_keys = mapping[char_pressed];
			// Map char typed to HardPass mapping
			//// New val = Current val - last typed char + mapping of last typed char
			let new_val = current_val.substring(0, current_val.length - 1) + mapped_keys.join('');
			$elem.val(new_val);
			last_val = new_val;


			console.log(char_pressed);
			console.log(current_val);
			console.log(new_val);
		});
	});

})
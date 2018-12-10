let LOGIN_URL = 'https://hardpass.herokuapp.com/login_extension';
let LOGOUT_URL = 'https://hardpass.herokuapp.com/logout_extension';
let MAPPING_URL = 'https://hardpass.herokuapp.com/get_mapping';

var website_domain = null;
chrome.tabs.getSelected(null, function (tab) {
	var url = new URL(tab.url);
	var domain = url.hostname;
	website_domain = domain;
});

function get_website_domain() {
	return website_domain;
}

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
		 		console.log("Mapping:");
		 		console.log(r['mapping']);

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

function header_disable() {
	$("#loggedin-container-header").text('HardPass is Disabled for '+get_website_domain());
	$("#loggedin-container-header").removeClass('text-success').removeClass('text-warning');
	$("#loggedin-container-header").addClass('text-danger');
	$("#loggedin-unpause").hide();
	$("#loggedin-disable").hide();
	$("#loggedin-disable-message").hide();
	$("#loggedin-pause").show().removeClass("d-none");
	$("#loggedin-enable").show().removeClass("d-none");
	// Grey out browser toolbar icon
	console.log("JKJ");
	grey_browser_icon();
}
function header_enable() {
	header_unpause();
}

function header_pause() {
	$("#loggedin-container-header").text('HardPass is Inactive');
	$("#loggedin-container-header").removeClass('text-success').removeClass('text-danger');
	$("#loggedin-container-header").addClass('text-warning');
	$("#loggedin-pause").hide();
	$("#loggedin-enable").hide();
	$("#loggedin-disable").hide();
	$("#loggedin-unpause").show().removeClass("d-none");
	$("#loggedin-disable-message").show().removeClass("d-none");
	// Grey out browser toolbar icon
	grey_browser_icon();
}

function header_unpause() {
	$("#loggedin-container-header").text('HardPass is Active');
	$("#loggedin-container-header").removeClass('text-warning').removeClass('text-danger');
	$("#loggedin-container-header").addClass('text-success');
	$("#loggedin-unpause").hide();
	$("#loggedin-enable").hide();
	$("#loggedin-disable-message").hide();
	$("#loggedin-pause").show().removeClass("d-none");
	$("#loggedin-disable").show().removeClass("d-none");
	// Add color to browser toolbar icon
	color_browser_icon();
}

$(document).ready(function() {
	//
	// Popup.html header
	chrome.storage.local.get(['km_active', 'disabled_websites'], function(result) {
		if (chrome.runtime.lastError) {
			header_pause();
			return;
		}
		// (1) Check if HardPass is active in general
		var km_active = result.km_active;
		if (km_active == undefined || km_active == false) {
			header_pause();
			return;
		}
		// (2) Check if HardPass is enabled on this site
		if (check_if_disabled_for_site(result)) {
			header_disable();
			return;
		}
		// (3) If not paused and not disabled on website, then ACTIVE!
		header_unpause();
	});

	//
	// Log out
	$("#loggedin-logout").click(function() {
		chrome.storage.local.remove("user_token", function() {
			chrome.storage.local.remove("mapping", function() {
			    // Data successfully saved
			    console.log("Successfully logged out");
		 		// Close extension pop-up window
		 		window.close();
		 	});
		});
		// $.ajax({
		// 	type: "POST",
		// 	url: LOGIN_URL,
		// 	data: {
		// 		email: email,
		// 		password: password
		// 	},
		// 	dataType: "json",
		// 	success: function(r) {
		// 	 	console.log("Extension logout went through");
		// 	 	if (r['error'] == 0) {
		// 	 		console.log("Successful logout");
		// 	 	}
		// 	 	else {
		// 	 		console.log(r['errorMsg']);
		// 	 	}
		// 	},
		// 	error: function(r) {
		// 	 	console.log("Error with extension logout");
		// 	 	console.log(r);
		// 	}
		// });
	})

	//
	// Check if user is logged in/get user token
	chrome.storage.local.get('user_token', function (result) {
		if (chrome.runtime.lastError) {
			// User token isn't set yet, so no logged in user
			console.log("Not logged in");
			return;
		}
	    var token = result.user_token;
	    if (token == undefined) {
	    	// User is not logged in
			console.log("Not logged in");
			return;
	    }
	    console.log("Token: "+token);
	    // Hide "Login Form"
	    $("#login-container").hide();
	    $("#loggedin-container").show();
	});

	//
	// Log user in
	$("#popup-login-form").submit(function(e) {
		// Button loading icon
		var l = Ladda.create( document.querySelector( '#popup-login-form button' ) );
		l.start();
		// Ignore form submit
		e.preventDefault();
		// Get user input
		const email = $("#popup-login-email").val();
		const password = $("#popup-login-password").val();
		// Send login request to server
		$.ajax({
			type: "POST",
			url: LOGIN_URL,
			data: {
				email: email,
				password: password
			},
			dataType: "json",
			success: function(r) {
				l.stop();
			 	console.log("Extension login went through");
			 	if (r['error'] == 0) {
			 		// Success!
			 		let token = r['token'];
			 		console.log("Token: "+r['token']);
			 		// Store user's token in browser storage
			 		chrome.storage.local.set({ "user_token": token }, function() {
					    // Data successfully saved
					    console.log("Successfully saved data");
				 		// If currently on webpage, load mapping for it
				 		let website = get_website_domain();
				 		load_keyboard_mapping(token, website);
				 		// Close extension pop-up window
				 		window.close();
					});
			 	}
			 	else {
			 		// Error
			 		if (r['error'] == 1) {
			 			console.log(r['errorMsg']);
			 		}
			 		if (r['error'] == 2) {
			 			console.log(r['errorMsg']);
			 		}
			 	}
			},
			error: function(r) {
				l.stop();
			 	console.log("Error with extension login");
			 	console.log(r);
			}
		});
	});

	//
	// Pause/unpause HardPass
	$("#loggedin-pause").click(function() {
		chrome.storage.local.set({ "km_active": false }, function() { });
		header_pause();
	});
	$("#loggedin-unpause").click(function() {
		chrome.storage.local.set({ "km_active": true }, function() { });
		chrome.storage.local.get('disabled_websites', function(result) {
			if (check_if_disabled_for_site(result)) {
				header_disable();
				return;
			}
			header_unpause();
		})
	});

	//
	// Disable HardPass for site
	$("#loggedin-disable").click(function() {
		chrome.storage.local.remove("mapping", function() { });
		// Save that this website is disabled
		chrome.storage.local.get("disabled_websites", function(result) {
			var disabled_websites_obj = result.disabled_websites;
			if (disabled_websites_obj == undefined) {
				// If not previously set, define dictionary
				disabled_websites_obj = {};
			}
			disabled_websites_obj[get_website_domain()] = 1;
			chrome.storage.local.set({ "disabled_websites" : disabled_websites_obj }, function() { });
		});
		header_disable();
	});
	$("#loggedin-enable").click(function() {
		chrome.storage.local.remove("mapping", function() { });
		// Remove this website from disabled list
		chrome.storage.local.get("disabled_websites", function(result) {
			var disabled_websites_obj = result.disabled_websites;
			if (disabled_websites_obj == undefined) {
				// If not previously set, ignore
				return;
			}
			// Delete dictionary entry for this website
			delete disabled_websites_obj[get_website_domain()];
			chrome.storage.local.set({ "disabled_websites" : disabled_websites_obj }, function() { });
		});
		chrome.storage.local.get('user_token', function(result) {
			var token = result.user_token;
			if (token == undefined) {
				return;
			}
			let website = get_website_domain();
			load_keyboard_mapping(token, website);
		});
		header_enable();
	});

})
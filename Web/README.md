# Chrome Extension Installation Instructions

Note: This browser extension only works in **Google Chrome.**

1) Open Google Chrome
2) Navigate to the URL ```chrome://extensions/```
3) Enabled "Developer Mode" by toggling the switch in the top-right of the screen
4) Aftering turning ON developer mode, click the "Load unpacked" button in the top-left of the screen.
5) Select the directory that was created after unzipping ```extension.zip```

You should now be all set! The HardPass icon will appear in the top-right of your Chrome browser. Click on the icon and login to your HardPass account to activate the extension.

# Extension Information

## Possible States

The HardPass extension can be in 1 of 3 possible states:

1. **Active** - Will generate and inject the appropriate keyboard mappings into all password fields for this user (unless the browser tab is currently on a webpage where HardPass had been explicitly disabled).
2. **Inactive** - Will not generate or inject keyboard mappings into any password field.
3. **Disabled for this Site** - Will not generate or inject keyboard mappings into any password field for this domain.


## Controls

The HardPass extension accepts user input through 6 primary buttons:

- **Resume** - Re-activates HardPass so that it will now continue generating keyboard mappings for every domain and injecting those mappings into password fields. Note: If a domain had specifically been disabled by the user prevoiusly, HardPass will still be disabled for that domain until explicitly re-enabled for it by clicking the **Enable for this Site** button. Opposite of **Pause for all Sites**.
- **Pause for all Sites** - Deactivates HardPass. No password fields will be autofilled until the user re-activates HardPass by clicking the **Resume** button. Opposite of **Resume**.
- **Enable for this Site** - Enables HardPass for the current domain. Opposite of **Disable for this Site**.
- **Disable for this Site** - Disables HardPass for the current domain. It will not autofill any password fields on webpages located at this domain until it is explicitly re-enabled by clicking the **Enable for this Site** button after the user has navigated to this domain again. Opposite of **Enable for this Site**.
- **Login** - Logs the user into HardPass (you must have already created an account at [https://hardpass.herokuapp.com/signup](https://hardpass.herokuapp.com/signup). Opposite of **Logout**
- **Logout** - Logs the extension out of HardPass, deletes all keyboard mappings previously stored in Chrome's local memory. Opposite of **Login**.
# LinkedIn Profile Picture Scraper

This project automates the process of logging into LinkedIn and retrieving profile pictures from specified LinkedIn profiles. The tool minimizes CAPTCHA appearances by imitating human behavior with random delays, cookies, and randomized user agents.

## Features

- **Automated Login to LinkedIn**: Logs in with provided credentials, storing session cookies to avoid repeated logins.
- **Profile Picture Retrieval**: Navigates to a LinkedIn profile and retrieves the profile picture URL.
- **Image Downloading and Saving**: Downloads and saves the profile picture locally, generating a filename based on the profile username.

- **Anti-Bot Measures**:
  - **Randomized User-Agent**: Simulates various devices and browsers.
  - **Session Cookies Management**: Saves cookies to reuse them, minimizing CAPTCHA on future logins.
  - **Randomized Delays**: Adds delays between actions to emulate human interaction.

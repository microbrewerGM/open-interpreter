# Roadmap

## Documentation

- [ ] **Easy 🟢** Add more hosted model instructions from from [LiteLLM's docs](https://docs.litellm.ai/docs/) to [our docs](https://github.com/KillianLucas/open-interpreter/tree/main/docs/language-model-setup/hosted-models).
  - [ ] Find a model that's [on LiteLLM's docs](https://docs.litellm.ai/docs/providers), but isn't [on ours](https://docs.openinterpreter.com/language-model-setup/hosted-models/openai)
  - [ ] Duplicate [one of our hosted model's `.mdx` file](https://github.com/KillianLucas/open-interpreter/tree/main/docs/language-model-setup/hosted-models)
  - [ ] Swap out the information with information from LiteLLM
  - [ ] Repeat with other models
- [ ] **Easy 🟢** Require documentation for PRs
- [ ] Work with Mintlify to translate docs. How does Mintlify let us translate our documentation automatically? I know there's a way.
- [ ] Better comments throughout the package (they're like docs for contributors)
- [ ] Document the New Computer Update
- [x] Make a migration guide for the New Computer Update (whats different in our new streaming structure (below) vs. [our old streaming structure](https://docs.openinterpreter.com/usage/python/streaming-response)) thanks ty!

## New features

- [ ] Add new `computer` modules like `browser`* and `files`*
- [ ] Add anonymous, opt-in data collection → open-source dataset, like `--contribute_conversations`
  - [ ] Make that flag send each message to server
  - [ ] Set up receiving replit server
  - [ ] Add option to send previous conversations
  - [ ] There should be a function that just renders messages to the terminal, so we can revive conversation navigator, and let people look at their conversations
    - [ ] This should also render their convos once input() is about to be run, so we don't get those weird stuttering `rich` artifacts
  - [ ] Make the messaging really strong re: "We will be saving this, we will redact PII, we will open source the dataset so we (and others) can train code interpreting models"
- [ ] Let OI use OI. Add `interpreter.chat(async=True)` bool. OI can use this to open OI on a new thread
  - [ ] Also add `interpreter.await()` which waits for `interpreter.running` (?) to = False, and `interpreter.result()` which returns the last assistant messages content.
- [ ] Allow for limited functions (`interpreter.functions`) using regex
  - [ ] If `interpreter.functions != []`:
    - [ ] set `interpreter.computer.languages` to only use Python
    - [ ] Use regex to ensure the output of code blocks conforms to just using those functions + other python basics
- [x] Allow for custom llms (to be stored in `interpreter.llm`) which conform to some class
  - [x] Has attributes `.supports_functions`, `.supports_vision`, and `.context_window`
- [ ] (Maybe) Allow for a custom embedding function (`interpreter.embed` or `computer.ai.embed`) which will let us do semantic search
- [ ] (Maybe) if a git is detected, switch to a mode that's good for developers, like showing nested file structure in dynamic system message, searching for relevant functions (use computer.files.search)
- [x] Allow for custom languages (`interpreter.computer.languages.append(class_that_conforms_to_base_language)`)
  - [x] Make it so function calling dynamically uses the languages in interpreter.computer.languages
- [ ] Add a skill library, or maybe expose post processing on code, so we can save functions for later & semantically search docstrings. Keep this minimal!
  - [ ] If `interpreter.skill_library == True`, we should add a decorator above all functions, then show OI how to search its skill library
  - [ ] Use computer.files.search over a folder that decorator saves functions (and import statements to)
  - [ ] Then use dynamic system message to show relevant functions
- [x] Allow for integrations somehow (you can replace interpreter.llm.completions with a wrapped completions endpoint for any kind of logging. need to document this tho)
  - [ ] Document this^
- [ ] Expand "safe mode" to have proper, simple Docker support, or maybe Cosmopolitan LibC
- [ ] Make it so core can be run elsewhere from terminal package — perhaps split over HTTP (this would make docker easier too)

## Future-proofing

- [ ] Really good tests / optimization framework, to be run less frequently than Github actions tests
  - [x] Figure out how to run us on [GAIA](https://huggingface.co/gaia-benchmark)
    - [x] How do we just get the questions out of this thing?
    - [x] How do we assess whether or not OI has solved the task?
  - [ ] Loop over GAIA, use a different language model every time (use Replicate, then ask LiteLLM how they made their "mega key" to many different LLM providers)
  - [ ] Loop over that ↑ using a different prompt each time. Which prompt is best across all LLMs?
  - [ ] (For the NCU) might be good to use a Google VM with a display
  - [ ] (Future future) Use GPT-4 to assess each result, explaining each failure. Summarize. Send it all to GPT-4 + our prompt. Let it redesign the prompt, given the failures, rinse and repeat
- [ ] Use Anthropic function calling
- [ ] Implement Plausible*
- [ ] Stateless (as in, doesn't use the application directory) core python package. All `appdir` stuff should be only for the TUI
  - [ ] `interpreter.__dict__` = a dict derived from config is how the python package should be set, and this should be from the TUI. `interpreter` should not know about the config
  - [ ] Move conversation storage out of the core and into the TUI. When we exit or error, save messages same as core currently does
- [ ] Local and vision should be reserved for TUI, more granular settings for Python
  - [x] Rename `interpreter.local` → `interpreter.offline`
  - [x] Implement custom LLMs with a `.supports_vision` attribute instead of `interpreter.vision`
- [ ] Further split TUI from core (some utils still reach across)
- [ ] Remove `procedures` (there must be a better way)
- [ ] Better storage of different model keys in TUI / config file. All keys, to multiple providers, should be stored in there. Easy switching
  - [ ] Automatically migrate users from old config to new config, display a message of this
- [ ] On update, check for new system message and ask user to overwrite theirs, or only let users pass in "custom instructions" which adds to our system message
  - [ ] I think we could have a config that's like... system_message_version. If system_message_version is below the current version, ask the user if we can overwrite it with the default config system message of that version

## Completed

- [x] **Split TUI from core — two seperate folders.** (This lets us tighten our scope around those two projects. See "What's in our scope" below.)
- [x] Add %% (shell) magic command
- [x] Support multiple instances
- [x] Split ROADMAP into sections
- [x] Connect %% (shell) magic command to shell interpreter that `interpreter` runs
- [x] Expose tool (`interpreter.computer.run(language, code)`)
- [x] Generalize "output" and "input" — new types other than text: HTML, Image (see below)
- [x] Switch core code interpreter to be Jupyter-powered
- [x] Make sure breaking from generator during execution stops the execution

# What's in our scope?

Open Interpreter contains two projects which support eachother, whose scopes are as follows:

1. `core`, which is dedicated to figuring out how to get LLMs to safely control a computer. Right now, this means creating a real-time code execution environment that language models can operate.
2. `terminal_interface`, a text-only way for users to direct the code-running LLM running inside `core`. This includes functions for connecting the `core` to various local and hosted LLMs (which the `core` itself should not know about).

# What's not in our scope?

Our guiding philosphy is minimalism, so we have also decided to explicitly consider the following as **out of scope**:

1. Additional functions in `core` beyond running code.
2. Advanced memory or planning. We consider these to be the LLM's responsibility, and as such OI will remain single-threaded.
3. More complex interactions with the LLM in `terminal_interface` beyond text (but file paths to more complex inputs, like images or video, can be included in that text).

---

This roadmap gets pretty rough from here. More like working notes.

# Working Notes

## * Roughly, how to build `computer.browser`:

First I think we should have a part, like `computer.browser.ask(query)` which just hits up [perplexity](https://www.perplexity.ai/) for fast answers to questions.

Then we want these sorts of things:
- `browser.open(url)`
- `browser.screenshot()`
- `browser.click()`

It should actually be based closely on Selenium. Copy their API so the LLM knows it.

Other than that, basically should be = to the computer module itself, at least the IO / keyboard and mouse parts.

However, for non vision models, `browser.screenshot()` can return the accessibility tree, not an image. And for `browser.click(some text)` we can use the HTML to find that text.

**Here's how GPT suggests we implement the first steps of this:**

Creating a Python script that automates the opening of Chrome with the necessary flags and then interacts with it to navigate to a URL and retrieve the accessibility tree involves a few steps. Here's a comprehensive approach:

1. **Script to Launch Chrome with Remote Debugging**:
   - This script will start Chrome with the `--remote-debugging-port=9222` flag.
   - It will handle different platforms (Windows, macOS, Linux).

2. **Python Script for Automation**:
   - This script uses `pychrome` to connect to the Chrome instance, navigate to a URL, and retrieve the accessibility tree.

### Step 1: Launching Chrome with Remote Debugging

You'll need a script to launch Chrome. This script varies based on the operating system. Below is an example for Windows. You can adapt it for macOS or Linux by changing the path and command to start Chrome.

```python
import subprocess
import sys
import os

def launch_chrome():
    chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"  # Update this path for your system
    url = "http://localhost:9222/json/version"
    subprocess.Popen([chrome_path, '--remote-debugging-port=9222'], shell=True)
    print("Chrome launched with remote debugging on port 9222.")

if __name__ == "__main__":
    launch_chrome()
```

### Step 2: Python Script to Navigate and Retrieve Accessibility Tree

Next, you'll use `pychrome` to connect to this Chrome instance. Ensure you've installed `pychrome`:

```bash
pip install pychrome
```

Here's the Python script:

```python
import pychrome
import time

def get_accessibility_tree(tab):
    # Enable the Accessibility domain
    tab.call_method("Accessibility.enable")

    # Get the accessibility tree
    tree = tab.call_method("Accessibility.getFullAXTree")
    return tree

def main():
    # Create a browser instance
    browser = pychrome.Browser(url="http://127.0.0.1:9222")

    # Create a new tab
    tab = browser.new_tab()

    # Start the tab
    tab.start()

    # Navigate to a URL
    tab.set_url("https://www.example.com")
    time.sleep(3)  # Wait for page to load

    # Retrieve the accessibility tree
    accessibility_tree = get_accessibility_tree(tab)
    print(accessibility_tree)

    # Stop the tab (closes it)
    tab.stop()

    # Close the browser
    browser.close()

if __name__ == "__main__":
    main()
```

This script will launch Chrome, connect to it, navigate to "https://www.example.com", and then print the accessibility tree to the console.

**Note**: The script to launch Chrome assumes a typical installation path on Windows. You will need to modify this path according to your Chrome installation location and operating system. Additionally, handling different operating systems requires conditional checks and respective commands for each OS.

## * Roughly, how to build `computer.files`:

Okay I'm thinking like, semantic filesystem or something. We make a new package that does really simple semantic search over a filesystem, then expose it via `computer.files.search("query")`.

## * Plausible

```python
import requests
import json

def send_event_to_plausible(domain, event_name):
    url = f'https://plausible.io/api/event'
    headers = {'Content-Type': 'application/json', 'User-Agent': 'YourAppName/Version'}
    payload = {
        'domain': domain,
        'name': event_name,
        'url': 'https://yourapp.com/path',  # URL where the event occurred
        'referrer': '',
        'props': {'prop1': 'value1', 'prop2': 'value2'}
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.status_code, response.text

# Usage example
send_event_to_plausible('yourdomain.com', 'event_name')
```

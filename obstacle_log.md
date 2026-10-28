# Obstacle Log - AI Support Desk Challenge

## 1. Issue: Accidental API Key Exposure Risk
- **Problem:** Hardcoding the Gemini API key directly into Python source code risks accidental exposure if pushed to GitHub.
- **Solution:** Implemented `python-dotenv` to read the key securely from a local `.env` file and configured a `.gitignore` file to block `.env` from version control.

## 2. Issue: Model Returning Unstructured Text Instead of JSON
- **Problem:** Early test prompts occasionally returned conversational filler around the JSON payload, breaking `json.loads()`.
- **Solution:** Enforced strict output formatting by setting `response_mime_type="application/json"` in the `GenerateContentConfig` and explicitly instructing the model in the prompt to return *only* a valid JSON object.

## 3. Issue: Network or Parsing Failures Crashing the Batch Script
- **Problem:** A single bad API response or formatting glitch could halt the entire loop processing multiple support tickets.
- **Solution:** Wrapped the LLM request and parsing blocks in robust `try/except` statements (`json.JSONDecodeError` and generic `Exception`), ensuring error states are gracefully captured into the final report without crashing the application.
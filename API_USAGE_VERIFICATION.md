# OpenAI API Usage Verification

## How to Verify API is Being Used

### 1. Check if API Key is Set

```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Or test with Python
python3 -c "import os; print('API Key set:', bool(os.environ.get('OPENAI_API_KEY')))"
```

### 2. Run Without --skip-llm Flag

The `--skip-llm` flag bypasses AI generation. Make sure you're NOT using it:

```bash
# ❌ This SKIPS AI (uses basic generator)
python3 -m cmd.reposentinel.main --skip-llm /path/to/repo

# ✅ This USES AI (makes API calls)
python3 -m cmd.reposentinel.main /path/to/repo
```

### 3. Check Logs for API Calls

When API calls are made, you'll see logs like:

```
🤖 LLM Client initialized with model: gpt-4o-mini
   API Key: ✅ Set
🤖 Making OpenAI API call for design category using gpt-4o-mini
✅ API call successful for design: 1234 tokens used
✅ Generated design instructions (2345 chars)
```

### 4. Verify in OpenAI Dashboard

1. Go to https://platform.openai.com/usage
2. Check your API usage
3. You should see requests for `gpt-4o-mini` model
4. Each category generates one API call (6-7 calls total)

### 5. Test API Connection

```bash
# Test if API key works
python3 << 'EOF'
import os
from openai import OpenAI

key = os.environ.get('OPENAI_API_KEY')
if not key:
    print("❌ OPENAI_API_KEY not set")
    exit(1)

client = OpenAI(api_key=key)
try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'test'"}],
        max_tokens=10
    )
    print("✅ API key works!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ API error: {e}")
EOF
```

## Troubleshooting

### API Usage is 0

**Possible causes:**

1. **Using --skip-llm flag**
   - Solution: Remove the flag or don't use it

2. **API key not set**
   - Solution: `export OPENAI_API_KEY="your-key"`

3. **API key invalid**
   - Solution: Check key at https://platform.openai.com/api-keys

4. **Quota exceeded**
   - Solution: Check billing at https://platform.openai.com/account/billing

5. **Errors being silently caught**
   - Solution: Check logs for error messages

### Check What's Happening

Run with verbose logging:

```bash
# Set log level to DEBUG
export REPOSENTINEL_LOG_LEVEL=DEBUG

# Run analysis
python3 -m cmd.reposentinel.main /path/to/repo
```

Look for:
- `🤖 LLM Client initialized` - Client created
- `🤖 Making OpenAI API call` - API call being made
- `✅ API call successful` - Call succeeded
- `⚠️` or `❌` - Errors occurred

## Expected Behavior

**With API Key (no --skip-llm):**
- ✅ Makes 6-7 API calls (one per category)
- ✅ Uses ~1000-2000 tokens per call
- ✅ Shows "AI-powered" in output
- ✅ Logs show API calls

**Without API Key or with --skip-llm:**
- ⚠️ Uses basic generator (no API calls)
- ⚠️ Shows "basic" in output
- ⚠️ No API usage in dashboard

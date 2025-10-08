# 🚨 SECURITY WARNING - READ BEFORE PUSHING TO GITHUB

## ⚠️ CRITICAL: API Keys Have Been Removed

**The template files in this repository have been sanitized and DO NOT contain real API keys.**

### 🔐 What You Need to Do:

1. **DO NOT commit your actual `.env` or `.env.local` files**
   - These are already in `.gitignore`
   - They contain your real secrets

2. **Before deploying, get fresh API keys from:**
   - **Supabase:** https://supabase.com/dashboard/project/pcktfzshbxaljkbedrar/settings/api
   - **OpenAI:** https://platform.openai.com/api-keys
   - **Friendli AI:** Your Friendli dashboard

3. **NEVER commit files with:**
   - ❌ `sk-proj-...` (OpenAI keys)
   - ❌ `flp_...` (Friendli tokens)
   - ❌ JWT tokens starting with `eyJh...`
   - ❌ Database passwords
   - ❌ Service role keys

### ✅ What's Safe to Commit:

- ✅ Template files with `[PLACEHOLDER]` text
- ✅ Supabase project URL (public)
- ✅ Configuration files (railway.json, vercel.json)
- ✅ Code without hardcoded secrets

### 🔒 Security Best Practices:

1. **Use environment variables** - Never hardcode secrets in code
2. **Rotate exposed keys immediately** if accidentally committed
3. **Use `.gitignore`** - Ensure `.env` files are never committed
4. **Review before push** - Always check `git diff` before pushing
5. **Use secret scanning** - Enable GitHub secret scanning

### 🆘 If You Accidentally Exposed Keys:

1. **Immediately rotate ALL exposed keys:**
   - Supabase: Generate new keys in dashboard
   - OpenAI: Revoke and create new key
   - Friendli: Regenerate token

2. **Remove from git history:**
   ```bash
   git filter-branch --force --index-filter \
   "git rm --cached --ignore-unmatch FILENAME" \
   --prune-empty --tag-name-filter cat -- --all
   ```

3. **Force push** (only if repository is private and you're the only user):
   ```bash
   git push origin --force --all
   ```

### 📋 Current Status:

- ✅ `.gitignore` configured correctly
- ✅ Template files sanitized
- ✅ No secrets in railway.json or vercel.json
- ✅ Environment files excluded from git

### 🎯 Before Each Deployment:

- [ ] Get fresh keys from service dashboards
- [ ] Copy to Railway/Vercel environment variables
- [ ] NEVER commit the actual keys to git
- [ ] Use the template files as reference only

---

**Remember: Template files are for REFERENCE only. Get fresh keys for actual deployment!**


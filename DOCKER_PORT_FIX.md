# 🐛 Docker $PORT Variable Fix

## ❌ **The Problem**

Railway was failing with:
```
Error: Invalid value for '--port': '$PORT' is not a valid integer.
```

## 🔍 **Root Cause**

**Before (WRONG):**
```dockerfile
CMD sh -c "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"
```

This uses Docker's **shell form** without proper exec syntax. Docker doesn't expand environment variables correctly in this format, causing `$PORT` to be treated as a literal string `"$PORT"` instead of the actual port number.

---

## ✅ **The Fix**

**After (CORRECT):**
```dockerfile
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

### Why This Works:

1. **Exec Form (JSON Array)**: `["sh", "-c", "..."]` uses Docker's exec form, which is the recommended syntax
2. **Explicit Shell Invocation**: `sh -c` explicitly tells Docker to use a shell for variable expansion
3. **Proper Variable Expansion**: The shell now correctly expands `${PORT:-8000}`:
   - If `PORT` is set by Railway → uses that value
   - If `PORT` is not set → defaults to `8000`

---

## 📋 **Docker CMD Forms Explained**

| Form | Syntax | Variable Expansion | Example |
|------|--------|-------------------|---------|
| **Exec Form** ✅ | `CMD ["executable", "param"]` | ❌ No (unless using shell) | `CMD ["sh", "-c", "echo $VAR"]` |
| **Shell Form** ⚠️ | `CMD command param` | ✅ Yes | `CMD echo $VAR` |
| **Shell Form (Wrong)** ❌ | `CMD sh -c "..."` | ❌ Unreliable | `CMD sh -c "echo $VAR"` |

---

## 🧪 **Testing**

### Local Docker Test:
```bash
# Build
docker build -f Dockerfile.backend -t backend-test .

# Run with PORT set
docker run -p 8000:8000 -e PORT=8000 backend-test

# Run with PORT unset (should default to 8000)
docker run -p 3000:8000 backend-test
```

### Railway Deployment:
Railway automatically sets `PORT` as an environment variable. The container will now correctly read and use this value.

---

## ✅ **Changes Made**

1. ✅ Fixed `CMD` directive to use exec form
2. ✅ Fixed `HEALTHCHECK` directive to use exec form
3. ✅ Ensured proper shell variable expansion for `${PORT:-8000}`

---

## 🚀 **Ready to Deploy**

After committing these changes, Railway will:
1. Build the Docker image successfully ✅
2. Start the container with the correct PORT ✅
3. Uvicorn will listen on Railway's assigned port ✅

**Your backend is now fixed and ready for Railway! 🎉**


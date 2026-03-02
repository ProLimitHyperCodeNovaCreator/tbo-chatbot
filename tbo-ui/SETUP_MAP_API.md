# 🗺️ Quick Setup: Google Maps API Key

## The Issue
The map shows "Loading..." indefinitely because the Google Maps API key is not configured.

## ✅ Solution: 3 Steps

### Step 1: Get Your Google Maps API Key

1. Open [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing one)
3. Enable the **Maps JavaScript API**:
   - Click "Enable APIs and Services"
   - Search for "Maps JavaScript API"
   - Click and select "ENABLE"
4. Go to **Credentials** → **Create Credentials** → **API Key**
5. Copy the generated key

### Step 2: Create `.env.local` File

In your `tbo-ui` folder, create a new file named `.env.local`:

```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-api-key-here
```

Replace `your-api-key-here` with the key you just copied.

**Example:**
```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIzaSyDqVs7aRoB5S3Z9x8kL2mN4pQ6rT7uV8wX
```

### Step 3: Restart Your Dev Server

```bash
npm run dev
```

## ✅ You'll See:
- ✅ Animated spinning loader (while map loads)
- ✅ Interactive Google Map with marker
- ✅ Location info card (Patna Airport)
- ✅ Works on mobile & desktop

## ❌ If Map Still Doesn't Load:

1. **API key missing?** → Check `.env.local` file exists
2. **Wrong key?** → Verify it's from Google Cloud Console
3. **API not enabled?** → Go to Google Cloud Console and enable "Maps JavaScript API"
4. **Check browser console** → Open DevTools (F12) → Console tab for error messages

## 🛡️ Security Note

After testing, restrict your API key in Google Cloud Console:
1. Go to **Credentials** → Click your API key
2. Under "Application restrictions" → Select "HTTP referrers (web sites)"
3. Add your domain (e.g., `example.com`, `example.com/*`)

This prevents others from using your API key.

## 📝 What's Different Now?

The updated component:
- ✅ Shows spinning loader while map loads
- ✅ Shows error message if API key missing (instead of infinite loading)
- ✅ 8-second timeout (doesn't wait forever)
- ✅ Location info always visible
- ✅ Better error messages in browser console

---

**Need help?** Check the browser console (F12) for detailed error messages!

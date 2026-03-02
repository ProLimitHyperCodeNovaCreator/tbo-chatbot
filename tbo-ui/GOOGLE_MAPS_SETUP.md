# Google Maps Integration Setup

## 📋 Prerequisites

The Sidebar component now uses **Google Maps API** for better scalability and advanced mapping features.

## 🔧 Configuration Steps

### 1. Get Your Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Maps JavaScript API
   - Maps Embed API
   - Maps Static API (optional)

4. Go to **Credentials** → **Create Credentials** → **API Key**
5. Copy your API key

### 2. Add to Your Environment

Create a `.env.local` file in the root of your `tbo-ui` project (next to `package.json`):

```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-api-key-here
```

**Important:** 
- The `NEXT_PUBLIC_` prefix makes it available to the browser
- Do NOT commit `.env.local` to version control
- Add `.env.local` to your `.gitignore` if not already present

### 3. Verify Setup

The map will automatically load when the Sidebar component mounts. You should see:
- Interactive Google Map centered on Patna, India
- Marker on Jay Prakash International Airport
- Info window with location details
- Zoom and pan controls

## 🚀 Features

- **Responsive Design**: Works on all screen sizes
- **Interactive Controls**: Click, zoom, drag, and pan
- **Info Windows**: Click markers for location details
- **Custom Styling**: Map styles optimized for your UI
- **Error Handling**: Graceful fallback if API is unavailable

## 🛡️ Security

- API key is public (NEXT_PUBLIC_) - this is intentional for frontend usage
- Restrict API key in Google Cloud Console:
  1. Go to Credentials → Your API Key
  2. Click on it to edit
  3. Under "API restrictions" → Select "Maps JavaScript API"
  4. Under "Application restrictions" → Select "HTTP referrers (web sites)"
  5. Add your domain(s)

## 🔄 Dynamic Location Updates

To change the map location dynamically, update the coordinates in `components/Sidebar.tsx`:

```typescript
// Change these coordinates
const patnaLocation = { lat: 25.5941, lng: 85.1376 };
```

## 📱 Mobile Responsive

The map is fully responsive:
- Desktop: 12 rem height
- Mobile: Adjusts to container width
- Touch-friendly zoom and pan controls

## ❓ Troubleshooting

### Map Not Loading?
1. Check browser console for errors
2. Verify API key is set in `.env.local`
3. Ensure API is enabled in Google Cloud Console
4. Check that HTTP referrer restrictions don't block your domain

### API Key Errors?
- "This API project is not authorized" → Enable Maps JavaScript API
- "Invalid API key" → Verify key is correct in `.env.local`
- "Billing required" → Enable billing in Google Cloud Console

### Performance Issues?
- Map loads asynchronously via script tag
- No page blocking
- Lazy initialization on component mount
- Efficient cleanup on unmount

## 📊 API Quota & Billing

- **Free tier**: 25,000 map loads/day
- **Paid**: $0.007 per additional map load after free tier
- Set budget alerts in Google Cloud Console

## 🎨 Customization

Modify map appearance in the component:

```typescript
const mapOptions: google.maps.MapOptions = {
  zoom: 13,                    // Adjust zoom level
  mapTypeControl: true,        // Show map type selector
  fullscreenControl: true,     // Show fullscreen button
  zoomControl: true,           // Show zoom controls
  scrollwheel: true,           // Enable scroll to zoom
};
```

## ✅ Production Checklist

- [ ] `.env.local` file created with valid API key
- [ ] `.env.local` added to `.gitignore`
- [ ] API key restricted in Google Cloud Console
- [ ] Billing enabled for production usage
- [ ] Budget alerts configured
- [ ] Map appears correctly on your domain
- [ ] Mobile responsiveness tested
- [ ] Performance verified with network throttling

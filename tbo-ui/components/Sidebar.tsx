'use client';

import React, { useRef, useEffect } from 'react';
import { Clock, Star, FileText, MapPin } from 'lucide-react';
import { HistoryItem, SavedPlan, Report, Agent } from '@/lib/types';

interface SidebarProps {
  history: HistoryItem[];
  savedPlans: SavedPlan[];
  reports?: Report[];
  agent?: Agent;
  isOpen?: boolean;
}

export default function Sidebar({
  history,
  savedPlans,
  reports,
  agent,
  isOpen = true,
}: SidebarProps) {
  const [activeTab, setActiveTab] = React.useState<'history' | 'plans' | 'reports'>('history');
  const [mapLoaded, setMapLoaded] = React.useState(false);
  const [mapError, setMapError] = React.useState(false);
  const [userLocation, setUserLocation] = React.useState<{ lat: number; lng: number } | null>(null);
  const [locationName, setLocationName] = React.useState<string>('Your Location');
  const [locationError, setLocationError] = React.useState(false);
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<google.maps.Map | null>(null);
  const mapInitialized = useRef(false);
  const userMarker = useRef<google.maps.Marker | null>(null);

  // Get user's live location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setUserLocation({ lat: latitude, lng: longitude });
        },
        (error) => {
          console.warn('Geolocation error:', error.message);
          setLocationError(true);
          // Fallback to Patna if geolocation fails
          setUserLocation({ lat: 25.5941, lng: 85.1376 });
        },
        {
          enableHighAccuracy: true,
          timeout: 5000,
          maximumAge: 0,
        }
      );
    } else {
      console.warn('Geolocation not supported');
      // Fallback to Patna
      setUserLocation({ lat: 25.5941, lng: 85.1376 });
    }
  }, []);

  // Initialize Google Map with user location
  useEffect(() => {
    if (!mapContainer.current || mapInitialized.current || !userLocation) return;

    const initializeMap = async () => {
      try {
        // Load Google Maps API
        const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;
        if (!apiKey) {
          console.warn('Google Maps API key not configured.');
          setMapError(true);
          return;
        }

        // Create script element
        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}`;
        script.async = true;
        script.defer = true;

        script.onload = () => {
          if (!mapContainer.current || !window.google || !userLocation) return;

          try {
            const google = window.google;

            // Create map centered on user's location
            map.current = new google.maps.Map(mapContainer.current, {
              zoom: 14,
              center: userLocation,
              mapTypeControl: true,
              fullscreenControl: true,
              zoomControl: true,
              streetViewControl: false,
              scrollwheel: true,
              disableDoubleClickZoom: false,
              styles: [
                {
                  featureType: 'poi',
                  elementType: 'labels',
                  stylers: [{ visibility: 'off' }],
                },
              ],
            });

            // Add marker for user's current location
            userMarker.current = new google.maps.Marker({
              position: userLocation,
              map: map.current,
              title: 'Your Location',
              icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
            });

            // Reverse geocode to get place name
            // @ts-ignore
            const geocoder = new google.maps.Geocoder();
            geocoder.geocode({ location: userLocation }, (results: any, status: string) => {
              if (status === 'OK' && results && results[0]) {
                const placeName = results[0].formatted_address.split(',')[0];
                setLocationName(placeName);
              }
            });

            // Add info window for user location
            const userInfoWindow = new google.maps.InfoWindow({
              content: `
                <div style="padding: 4px 8px; font-size: 11px; white-space: nowrap;">
                  <div style="font-weight: 600;">📍 ${locationName}</div>
                </div>
              `,
              position: userLocation,
              maxWidth: 150,
            });
            userInfoWindow.open(map.current);

            // Add click listener to user marker to show info window
            userMarker.current.addListener('click', () => {
              userInfoWindow.open(map.current, userMarker.current);
            });

            mapInitialized.current = true;
            setMapLoaded(true);
          } catch (err) {
            console.error('Error creating map:', err);
            setMapError(true);
          }
        };

        script.onerror = () => {
          console.error('Failed to load Google Maps API');
          setMapError(true);
        };

        // Set timeout for API loading (8 seconds)
        const timeout = setTimeout(() => {
          if (!mapInitialized.current) {
            console.warn('Google Maps API loading timeout');
            setMapError(true);
          }
        }, 8000);

        script.addEventListener('load', () => clearTimeout(timeout));
        script.addEventListener('error', () => clearTimeout(timeout));

        document.head.appendChild(script);
      } catch (error) {
        console.error('Error initializing map:', error);
        setMapError(true);
      }
    };

    initializeMap();

    return () => {
      // Cleanup if needed
      if (map.current) {
        map.current = null;
      }
    };
  }, [userLocation]);

  return (
    <div className={`
      hidden md:flex flex-col flex-shrink-0 w-64 lg:w-72 bg-gradient-to-b from-blue-50 to-white border-r border-gray-200
      ${isOpen ? 'block' : 'hidden'}
      transition-all duration-300 h-full
    `}>
      {/* Agent Profile */}
      {agent && (
        <div className="px-4 py-3 border-b border-gray-200 flex-shrink-0">
          <div className="flex flex-col items-center">
            <img
              src={agent.image}
              alt={agent.name}
              className="w-20 h-20 rounded-full object-cover mb-2 border-2 border-blue-500"
            />
            <h3 className="font-semibold text-gray-900 text-center text-sm">{agent.name}</h3>
            <p className="text-xs text-gray-600 text-center">{agent.title}</p>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="flex justify-around border-b border-gray-200 px-2 flex-shrink-0">
        <button
          onClick={() => setActiveTab('history')}
          className={`flex items-center gap-1 px-2 py-2 text-xs font-medium rounded-t transition-colors ${activeTab === 'history'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-900'
            }`}
        >
          <Clock size={16} />
          <span className="hidden sm:inline">History</span>
        </button>
        <button
          onClick={() => setActiveTab('plans')}
          className={`flex items-center gap-1 px-2 py-2 text-xs font-medium rounded-t transition-colors ${activeTab === 'plans'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-900'
            }`}
        >
          <Star size={16} />
          <span className="hidden sm:inline">Plans</span>
        </button>
        <button
          onClick={() => setActiveTab('reports')}
          className={`flex items-center gap-1 px-2 py-2 text-xs font-medium rounded-t transition-colors ${activeTab === 'reports'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-900'
            }`}
        >
          <FileText size={16} />
          <span className="hidden sm:inline">Reports</span>
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto px-3 py-4 max-h-fit">
        {activeTab === 'history' && (
          <div className="space-y-1">
            {history.length > 0 ? (
              history.map((item) => (
                <div
                  key={item.id}
                  className="p-2 rounded-lg hover:bg-blue-50 cursor-pointer transition-colors group"
                >
                  <p className="text-xs font-medium text-gray-900 group-hover:text-blue-600">
                    {item.destination}
                  </p>
                  <p className="text-xs text-gray-500">{item.date}</p>
                </div>
              ))
            ) : (
              <p className="text-xs text-gray-500 text-center py-4">No history yet</p>
            )}
          </div>
        )}

        {activeTab === 'plans' && (
          <div className="space-y-1">
            {savedPlans.length > 0 ? (
              savedPlans.map((plan) => (
                <div
                  key={plan.id}
                  className="p-2 rounded-lg hover:bg-yellow-50 cursor-pointer transition-colors group"
                >
                  <div className="flex items-start gap-2">
                    <Star size={14} className="text-yellow-500 flex-shrink-0 mt-0.5" />
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-medium text-gray-900 group-hover:text-blue-600 truncate">
                        {plan.name}
                      </p>
                      <p className="text-xs text-gray-500">{plan.destination}</p>
                      <p className="text-xs font-semibold text-blue-600">{plan.price}</p>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-xs text-gray-500 text-center py-4">No saved plans</p>
            )}
          </div>
        )}

        {activeTab === 'reports' && (
          <div className="space-y-1">
            {reports && reports.length > 0 ? (
              reports.map((report) => (
                <div
                  key={report.id}
                  className="p-2 rounded-lg hover:bg-purple-50 cursor-pointer transition-colors group"
                >
                  <div className="flex items-start gap-2">
                    <span className="text-base flex-shrink-0">{report.icon}</span>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-medium text-gray-900 group-hover:text-blue-600">
                        {report.title}
                      </p>
                      <p className="text-xs text-gray-500">{report.date}</p>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-xs text-gray-500 text-center py-4">No reports</p>
            )}
          </div>
        )}
      </div>

      {/* Map Section */}
      <div className="px-3 py-4 border-t border-gray-200 flex-shrink-0">
        {/* Google Maps Container */}
        <div className="rounded-lg overflow-hidden h-48 bg-gray-100 shadow-md border border-gray-300 relative">
          <div
            ref={mapContainer}
            className="w-full h-full absolute inset-0"
          />

          {/* Loading State */}
          {!mapLoaded && !mapError && (
            <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 animate-pulse z-10">
              <div className="text-center">
                <div className="w-8 h-8 border-2 border-blue-300 border-t-blue-600 rounded-full animate-spin mx-auto mb-2"></div>
                <p className="text-xs text-gray-600">Loading map...</p>
              </div>
            </div>
          )}

          {/* Error State */}
          {mapError && (
            <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 z-10">
              <div className="text-center px-3">
                <MapPin size={24} className="text-gray-400 mx-auto mb-2" />
                <p className="text-xs font-medium text-gray-700 mb-1">Map Unavailable</p>
                <p className="text-xs text-gray-600">Check if API key is configured in .env.local</p>
              </div>
            </div>
          )}
        </div>

        {/* Location Info */}
        <div className="mt-3 p-3 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-lg border border-blue-200">
          <div className="flex items-start gap-2">
            <MapPin size={16} className="text-blue-600 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              {userLocation && !locationError ? (
                <>
                  <p className="text-xs font-semibold text-gray-900">📍 {locationName}</p>
                  <p className="text-xs text-green-600 mt-1 font-medium">✓ Live Location</p>
                </>
              ) : locationError ? (
                <>
                  <p className="text-xs font-semibold text-gray-900">Location Access</p>
                  <p className="text-xs text-orange-600 mt-0.5">Using fallback location</p>
                  <p className="text-xs text-gray-600 mt-1">Enable location in browser settings</p>
                </>
              ) : (
                <>
                  <p className="text-xs font-semibold text-gray-900">Getting Location...</p>
                  <p className="text-xs text-gray-600 mt-0.5">Please allow location access</p>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
